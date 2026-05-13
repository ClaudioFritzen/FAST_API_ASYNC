import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, Plus, Search, X, Trash2, Edit3 } from 'lucide-react';
import { fetchTodos, updateTodoState, createTodo, updateTodo, deleteTodo } from '../services/todos';
import type { Todo } from '../services/todos';
import '../components.css';

const columns = [
  { id: 'draft', title: 'Rascunho', color: 'var(--text-tertiary)' },
  { id: 'todo', title: 'A Fazer', color: 'var(--todo-color)' },
  { id: 'doing', title: 'Em Andamento', color: 'var(--doing-color)' },
  { id: 'done', title: 'Concluído', color: 'var(--success-color)' },
  { id: 'trash', title: 'Lixeira', color: 'var(--danger-color)' },
];

const Board = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [draggedItem, setDraggedItem] = useState<number | null>(null);
  
  // New task form state
  const [showNewTask, setShowNewTask] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDesc, setNewTaskDesc] = useState('');

  // Editing task state
  const [editingTask, setEditingTask] = useState<Todo | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDesc, setEditDesc] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      setLoading(true);
      const data = await fetchTodos();
      setTodos(data);
    } catch (err: any) {
      console.error(err);
      if (err.response?.status === 401) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDragStart = (e: React.DragEvent, id: number) => {
    setDraggedItem(id);
    e.dataTransfer.effectAllowed = 'move';
    setTimeout(() => {
      (e.target as HTMLElement).style.opacity = '0.5';
    }, 0);
  };

  const handleDragEnd = (e: React.DragEvent) => {
    (e.target as HTMLElement).style.opacity = '1';
    setDraggedItem(null);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = async (e: React.DragEvent, stateId: string) => {
    e.preventDefault();
    if (!draggedItem) return;

    // Optimistic UI update
    setTodos(prev => prev.map(t => t.id === draggedItem ? { ...t, state: stateId as any } : t));

    try {
      await updateTodoState(draggedItem, stateId);
    } catch (err) {
      console.error("Erro ao mover tarefa", err);
      loadTodos();
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      await createTodo({ title: newTaskTitle, description: newTaskDesc, state: 'draft' });
      setNewTaskTitle('');
      setNewTaskDesc('');
      setShowNewTask(false);
      loadTodos();
    } catch (err) {
      console.error(err);
    }
  };

  const openEditModal = (todo: Todo) => {
    setEditingTask(todo);
    setEditTitle(todo.title);
    setEditDesc(todo.description || '');
  };

  const closeEditModal = () => {
    setEditingTask(null);
    setEditTitle('');
    setEditDesc('');
  };

  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTask || !editTitle.trim()) return;

    // Optimistic UI Component updates
    setTodos(prev => prev.map(t => 
      t.id === editingTask.id ? { ...t, title: editTitle, description: editDesc } : t
    ));
    
    const targetId = editingTask.id;
    closeEditModal();

    try {
      await updateTodo(targetId, { title: editTitle, description: editDesc });
    } catch (err) {
      console.error("Erro ao atualizar tarefa", err);
      loadTodos(); // rollback
    }
  };

  const handleDeleteTask = async () => {
    if (!editingTask) return;
    const targetId = editingTask.id;
    
    if(!window.confirm("Certeza que deseja excluir permanentemente esta tarefa?")) return;

    setTodos(prev => prev.filter(t => t.id !== targetId));
    closeEditModal();

    try {
      await deleteTodo(targetId);
    } catch (err) {
      console.error("Erro ao deletar tarefa", err);
      loadTodos();
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  const filteredTodos = todos.filter(t => 
    t.title.toLowerCase().includes(search.toLowerCase()) || 
    (t.description && t.description.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div style={{ padding: '2rem', height: '100vh', display: 'flex', flexDirection: 'column' }} className="animate-fade-in">
      
      {/* Header Area */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ color: 'var(--primary-color)' }}>❖</span> Kanban Board
          </h1>
        </div>
        
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ position: 'relative' }}>
            <Search size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} />
            <input 
              type="text" 
              className="input-field" 
              style={{ paddingLeft: '2.5rem', width: '250px', marginBottom: 0 }}
              placeholder="Buscar tarefas..." 
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
          <button className="btn btn-primary" onClick={() => setShowNewTask(true)}>
            <Plus size={16} /> Nova Tarefa
          </button>
          
          <button className="btn" onClick={handleLogout} style={{ border: '1px solid var(--danger-color)', color: 'var(--danger-color)', backgroundColor: 'transparent' }}>
            <LogOut size={16} style={{ marginRight: '0.25rem' }} /> Sair
          </button>
        </div>
      </header>

      {/* New Task Inline Panel */}
      {showNewTask && (
        <div className="glass-panel animate-fade-in" style={{ padding: '1.5rem', marginBottom: '2rem', display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <input 
              autoFocus
              type="text" 
              className="input-field" 
              placeholder="Título da nova tarefa" 
              value={newTaskTitle}
              onChange={e => setNewTaskTitle(e.target.value)}
              style={{ marginBottom: 0 }}
            />
            <textarea 
              className="input-field" 
              placeholder="Descrição ou detalhes..." 
              value={newTaskDesc}
              onChange={e => setNewTaskDesc(e.target.value)}
              style={{ minHeight: '60px', resize: 'vertical', marginBottom: 0 }}
            />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <button className="btn btn-primary" onClick={handleCreateTask}>Salvar Tarefa</button>
            <button className="btn" onClick={() => setShowNewTask(false)}>Cancelar</button>
          </div>
        </div>
      )}

      {/* Loading Spinner */}
      {loading ? (
        <div className="flex-center" style={{ flex: 1 }}>
          <div className="spinner" style={{ width: '40px', height: '40px', borderWidth: '4px' }}></div>
        </div>
      ) : (
        /* Kanban Columns */
        <div className="kanban-board">
          {columns.map(col => {
            const colTodos = filteredTodos.filter(t => t.state === col.id);
            return (
              <div 
                key={col.id} 
                className="kanban-column"
                onDragOver={handleDragOver}
                onDrop={(e) => handleDrop(e, col.id)}
              >
                <div className="column-header">
                  <div className="column-title">
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: col.color }} />
                    {col.title}
                  </div>
                  <span className="badge">{colTodos.length}</span>
                </div>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', flex: 1 }}>
                  {colTodos.map(todo => (
                    <div 
                      key={todo.id} 
                      className="task-card"
                      draggable
                      onDragStart={(e) => handleDragStart(e, todo.id)}
                      onDragEnd={handleDragEnd}
                      onClick={() => openEditModal(todo)}
                    >
                      <div className="task-title" style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span>{todo.title}</span>
                      </div>
                      {todo.description && <div className="task-desc">{todo.description}</div>}
                    </div>
                  ))}
                  {colTodos.length === 0 && (
                    <div style={{ padding: '1.5rem', textAlign: 'center', color: 'var(--text-tertiary)', border: '1px dashed var(--glass-border)', borderRadius: 'var(--border-radius-md)', fontSize: '0.875rem' }}>
                      Solte as tarefas aqui
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Edit Task Modal Overlay */}
      {editingTask && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.6)', backdropFilter: 'blur(4px)',
          display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000,
          padding: '1rem'
        }}>
          <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '500px', padding: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h3 style={{ fontSize: '1.25rem', color: 'white', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Edit3 size={20} color="var(--primary-color)" /> Editando Tarefa
              </h3>
              <button 
                onClick={closeEditModal} 
                style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
              >
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleUpdateTask}>
              <div style={{ marginBottom: '1rem' }}>
                <label className="input-label">Título da Tarefa</label>
                <input 
                  type="text" 
                  className="input-field" 
                  autoFocus
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  style={{ marginBottom: 0 }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <label className="input-label">Descrição</label>
                <textarea 
                  className="input-field" 
                  value={editDesc}
                  onChange={(e) => setEditDesc(e.target.value)}
                  style={{ minHeight: '100px', resize: 'vertical', marginBottom: 0 }}
                />
              </div>

              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', alignItems: 'center' }}>
                <button type="button" onClick={handleDeleteTask} style={{ 
                  marginRight: 'auto', background: 'none', border: 'none', 
                  color: 'var(--danger-color)', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer',
                  fontSize: '0.875rem'
                }}>
                  <Trash2 size={16} /> Excluir permanentemente
                </button>
                <button type="button" className="btn" onClick={closeEditModal} style={{ border: '1px solid var(--glass-border)' }}>Cancelar</button>
                <button type="submit" className="btn btn-primary">Salvar Alterações</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Board;
