/**
 * Task type definitions
 */

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  limit: number;
  offset: number;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title: string;
  description: string;
  completed: boolean;
}

export interface PatchTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}
