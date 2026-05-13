import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../services/auth';
import { Lock, User, Mail } from 'lucide-react';
import '../components.css';

const Login = () => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const navigate = useNavigate();

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      if (isRegistering) {
        // Create user
        await register(username, email, password);
        setSuccess('Conta criada com sucesso! Aguarde o login...');
        
        // Auto login right after
        await login(email, password);
        navigate('/board');
      } else {
        // Normal Login (Wait, backend requires email to be passed on the username field!)
        await login(email, password);
        navigate('/board');
      }
    } catch (err: any) {
      if (isRegistering) {
        setError(err.response?.data?.detail || 'Erro ao criar conta.');
      } else {
        setError(err.response?.data?.detail || 'Erro ao realizar login.');
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsRegistering(!isRegistering);
    setError('');
    setSuccess('');
  };

  return (
    <div className="flex-center animate-fade-in" style={{ minHeight: '100vh', padding: '1rem' }}>
      <div className="glass-panel" style={{ width: '100%', maxWidth: '400px', padding: '2.5rem' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1.75rem', fontWeight: '700', color: 'white', marginBottom: '0.25rem' }}>
            {isRegistering ? 'Criar Nova Conta' : 'Welcome Back'}
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            {isRegistering 
              ? 'Insira seus dados para começar no Kanban' 
              : 'Faça login para acessar o Quadro Kanban'}
          </p>
        </div>

        {error && (
          <div style={{ padding: '0.75rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger-color)', borderRadius: 'var(--border-radius-sm)', marginBottom: '1rem', fontSize: '0.875rem', textAlign: 'center' }}>
            {error}
          </div>
        )}

        {success && (
          <div style={{ padding: '0.75rem', backgroundColor: 'rgba(34, 197, 94, 0.1)', color: 'var(--success-color)', borderRadius: 'var(--border-radius-sm)', marginBottom: '1rem', fontSize: '0.875rem', textAlign: 'center' }}>
            {success}
          </div>
        )}

        <form onSubmit={handleAuth}>
          {isRegistering && (
            <div className="input-group">
              <label className="input-label">Username</label>
              <div style={{ position: 'relative' }}>
                <User size={18} className="input-icon" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} />
                <input 
                  type="text" 
                  className="input-field" 
                  style={{ paddingLeft: '2.5rem' }}
                  placeholder="Seu nome (ex: admin)" 
                  value={username} 
                  onChange={(e) => setUsername(e.target.value)} 
                  required={isRegistering}
                />
              </div>
            </div>
          )}

          <div className="input-group">
            <label className="input-label">Email Principal</label>
            <div style={{ position: 'relative' }}>
              <Mail size={18} className="input-icon" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} />
              <input 
                type="email" 
                className="input-field" 
                style={{ paddingLeft: '2.5rem' }}
                placeholder="seu@email.com" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                required 
              />
            </div>
          </div>

          <div className="input-group" style={{ marginBottom: '1.5rem' }}>
            <label className="input-label">Password</label>
            <div style={{ position: 'relative' }}>
              <Lock size={18} className="input-icon" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} />
              <input 
                type="password" 
                className="input-field" 
                style={{ paddingLeft: '2.5rem' }}
                placeholder="••••••••" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                required 
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginBottom: '1rem' }} disabled={loading}>
            {loading ? <div className="spinner"></div> : (isRegistering ? 'Criar Conta' : 'Entrar na Plataforma')}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1rem' }}>
          <button 
            type="button" 
            onClick={toggleMode}
            disabled={loading}
            style={{ 
              background: 'none', border: 'none', 
              color: 'var(--text-secondary)', fontSize: '0.875rem', 
              cursor: 'pointer', textDecoration: 'underline' 
            }}
          >
            {isRegistering ? 'Já possui uma conta? Fazer Login' : 'Não tem uma conta? Registre-se aqui'}
          </button>
        </div>

      </div>
    </div>
  );
};

export default Login;
