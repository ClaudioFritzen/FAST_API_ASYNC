import api from './api';

export const login = async (username: string, password: string) => {
  // FastAPI OAuth2PasswordRequestForm requires form-urlencoded data
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const response = await api.post('/auth/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  
  if (response.data.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
  }
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('access_token');
};

export const register = async (username: string, email: string, password: string) => {
  const response = await api.post('/users/', {
    username,
    email,
    password,
  });
  return response.data;
};
