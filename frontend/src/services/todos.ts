import api from './api';

export interface Todo {
  id: number;
  title: string;
  description: string;
  state: 'draft' | 'todo' | 'doing' | 'done' | 'trash';
  user_id: number;
  created_at: string;
  updated_at: string;
}

export const fetchTodos = async (): Promise<Todo[]> => {
  const response = await api.get('/todos/');
  return response.data.todos;
};

export const createTodo = async (todo: { title: string; description: string; state: string }): Promise<Todo> => {
  const response = await api.post('/todos/', todo);
  return response.data;
};

export const updateTodoState = async (id: number, state: string): Promise<Todo> => {
  const response = await api.patch(`/todos/${id}`, { state });
  return response.data;
};

export const updateTodo = async (id: number, data: Partial<Todo>): Promise<Todo> => {
  const response = await api.patch(`/todos/${id}`, data);
  return response.data;
};

export const deleteTodo = async (id: number): Promise<void> => {
  await api.delete(`/todos/${id}`);
};
