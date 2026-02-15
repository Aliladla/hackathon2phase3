'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { TaskForm } from '@/components/tasks/TaskForm';
import { TaskList } from '@/components/tasks/TaskList';
import apiClient from '@/lib/api';
import type { Task, TaskListResponse } from '@/types/task';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<TaskListResponse>('/api/tasks');
      setTasks(response.data.tasks);
    } catch (error: any) {
      console.error('Failed to fetch tasks:', error);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleTaskCreated = (newTask: Task) => {
    setTasks((prev) => [newTask, ...prev]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks((prev) =>
      prev.map((task) => (task.id === updatedTask.id ? updatedTask : task))
    );
  };

  const handleTaskDeleted = (taskId: number) => {
    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  return (
    <div className="px-4 py-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">My Tasks</h1>
          <p className="text-gray-600">
            {tasks.length === 0
              ? 'No tasks yet. Create your first task below.'
              : `You have ${tasks.filter((t) => !t.completed).length} incomplete task${
                  tasks.filter((t) => !t.completed).length !== 1 ? 's' : ''
                } and ${tasks.filter((t) => t.completed).length} completed task${
                  tasks.filter((t) => t.completed).length !== 1 ? 's' : ''
                }.`}
          </p>
        </div>

        <div className="mb-8">
          <Card>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Task</h2>
            <TaskForm onTaskCreated={handleTaskCreated} />
          </Card>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">All Tasks</h2>
          {loading ? (
            <div className="flex justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-600">{error}</p>
              <button
                onClick={fetchTasks}
                className="mt-2 text-sm text-red-700 hover:text-red-800 font-medium"
              >
                Try again
              </button>
            </div>
          ) : (
            <TaskList
              tasks={tasks}
              onTaskUpdated={handleTaskUpdated}
              onTaskDeleted={handleTaskDeleted}
            />
          )}
        </div>
      </div>
    </div>
  );
}
