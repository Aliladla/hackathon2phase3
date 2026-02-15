/**
 * Task Item component for displaying individual tasks
 */
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import apiClient from '@/lib/api';
import type { Task } from '@/types/task';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: number) => void;
}

export const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskUpdated, onTaskDeleted }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({ title: task.title, description: task.description });
  const [loading, setLoading] = useState(false);

  const handleToggleComplete = async () => {
    setLoading(true);
    try {
      const response = await apiClient.patch<Task>(`/api/tasks/${task.id}/complete`);
      onTaskUpdated(response.data);
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditData({ title: task.title, description: task.description });
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditData({ title: task.title, description: task.description });
  };

  const handleSaveEdit = async () => {
    if (!editData.title.trim()) {
      return;
    }

    setLoading(true);
    try {
      const response = await apiClient.put<Task>(`/api/tasks/${task.id}`, {
        title: editData.title,
        description: editData.description,
        completed: task.completed,
      });
      onTaskUpdated(response.data);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setLoading(true);
    try {
      await apiClient.delete(`/api/tasks/${task.id}`);
      onTaskDeleted(task.id);
    } catch (error) {
      console.error('Failed to delete task:', error);
    } finally {
      setLoading(false);
    }
  };

  if (isEditing) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 border-2 border-primary-500">
        <div className="space-y-3">
          <Input
            type="text"
            value={editData.title}
            onChange={(e) => setEditData({ ...editData, title: e.target.value })}
            placeholder="Task title"
          />
          <textarea
            value={editData.description}
            onChange={(e) => setEditData({ ...editData, description: e.target.value })}
            placeholder="Description"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            rows={3}
          />
          <div className="flex gap-2">
            <Button onClick={handleSaveEdit} loading={loading} className="flex-1">
              Save
            </Button>
            <Button onClick={handleCancelEdit} variant="secondary" className="flex-1">
              Cancel
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-4 transition-all ${task.completed ? 'opacity-75' : ''}`}>
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          disabled={loading}
          className="mt-1 h-5 w-5 text-primary-600 rounded focus:ring-primary-500 cursor-pointer"
        />
        <div className="flex-1 min-w-0">
          <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
          <div className="mt-2 flex items-center gap-2 text-xs text-gray-500">
            <span>ID: {task.id}</span>
            <span>•</span>
            <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
          </div>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleEdit} variant="secondary" className="text-sm px-3 py-1">
            Edit
          </Button>
          <Button onClick={handleDelete} variant="danger" className="text-sm px-3 py-1" loading={loading}>
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
};
