"""OpenAI agent for natural language task management."""
import json
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from chatbot.config import settings
from chatbot.api.client import APIClient
from chatbot.mcp.schemas import ALL_TOOLS, MCPToolResult
from chatbot.mcp.executor import MCPToolExecutor
from chatbot.conversation.context import ConversationContext
from chatbot.agent.prompts import SYSTEM_PROMPT


class TodoAgent:
    """AI agent for conversational task management."""

    def __init__(self, jwt_token: str, context: ConversationContext):
        """
        Initialize the Todo agent.

        Args:
            jwt_token: JWT token for Phase 2 backend authentication
            context: Conversation context for this session
        """
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.api_client = APIClient(jwt_token=jwt_token)
        self.executor = MCPToolExecutor(api_client=self.api_client)
        self.context = context
        self.model = settings.OPENAI_MODEL

    async def process_message(self, user_message: str) -> str:
        """
        Process a user message and return the agent's response.

        Args:
            user_message: Natural language input from user

        Returns:
            Agent's conversational response
        """
        # Add user message to context
        self.context.add_message(role="user", content=user_message)

        # Prepare system prompt with context
        system_prompt = SYSTEM_PROMPT.format(
            context=self.context.get_context_summary()
        )

        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": system_prompt}
        ] + self.context.get_messages_for_openai()

        # Prepare tools for function calling
        tools = [tool.to_openai_function() for tool in ALL_TOOLS]

        try:
            # Initial API call
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # Check if the model wants to call tools
            if assistant_message.tool_calls:
                # Execute tool calls
                tool_results = await self._execute_tool_calls(
                    assistant_message.tool_calls
                )

                # Add assistant message with tool calls to context
                self.context.add_message(
                    role="assistant",
                    content=assistant_message.content or "",
                    tool_calls=[
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                )

                # Prepare messages with tool results
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })

                # Add tool results to messages
                for tool_call, result in zip(assistant_message.tool_calls, tool_results):
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })

                # Get final response from model
                final_response = await self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )

                final_content = final_response.choices[0].message.content or ""

                # Update context with task information from tool results
                self._update_context_from_results(tool_results)

                # Add final assistant response to context
                self.context.add_message(
                    role="assistant",
                    content=final_content,
                    tool_results=tool_results
                )

                return final_content

            else:
                # No tool calls, just return the response
                content = assistant_message.content or ""
                self.context.add_message(role="assistant", content=content)
                return content

        except Exception as e:
            error_message = f"I encountered an error: {str(e)}. Please try again."
            self.context.add_message(role="assistant", content=error_message)
            return error_message

    async def _execute_tool_calls(self, tool_calls) -> List[Dict[str, Any]]:
        """
        Execute multiple tool calls.

        Args:
            tool_calls: List of tool calls from OpenAI

        Returns:
            List of tool execution results
        """
        results = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Execute the tool
            result = await self.executor.execute(function_name, function_args)

            # Convert MCPToolResult to dict for JSON serialization
            result_dict = {
                "tool_name": result.tool_name,
                "success": result.success,
                "result": result.result,
                "error": result.error,
                "execution_time": result.execution_time
            }

            results.append(result_dict)

        return results

    def _update_context_from_results(self, tool_results: List[Dict[str, Any]]) -> None:
        """
        Update conversation context based on tool execution results.

        Args:
            tool_results: List of tool execution results
        """
        for result in tool_results:
            if not result["success"]:
                continue

            tool_name = result["tool_name"]
            tool_data = result["result"]

            # Extract task ID and operation type
            if tool_name == "create_task" and "id" in tool_data:
                self.context.update_task_context(
                    task_id=tool_data["id"],
                    operation="create"
                )
            elif tool_name == "get_task" and "id" in tool_data:
                self.context.update_task_context(
                    task_id=tool_data["id"],
                    operation="view"
                )
            elif tool_name == "update_task" and "id" in tool_data:
                self.context.update_task_context(
                    task_id=tool_data["id"],
                    operation="update"
                )
            elif tool_name == "delete_task":
                # Extract task_id from the success message or keep last_task_id
                self.context.update_task_context(
                    task_id=None,
                    operation="delete"
                )
            elif tool_name == "toggle_complete" and "id" in tool_data:
                self.context.update_task_context(
                    task_id=tool_data["id"],
                    operation="complete"
                )
