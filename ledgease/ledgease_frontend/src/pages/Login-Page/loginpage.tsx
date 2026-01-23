import './LoginPage.css';
import { useNavigate } from 'react-router-dom';
import React from 'react';
import { apiFetch, setToken } from '../../lib/api';

type LoginResponse = {
        accessToken: string;
        refreshToken: string;
    };

export default function LoginPage(){
    const nav = useNavigate();
    const [username, setUsername] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [error, setError] = React.useState('');
    const [loading, setLoading] = React.useState(false);

    async function handleLogin(event: React.FormEvent) {
        // Using only username login for now will change later *****
        event.preventDefault();

        setLoading(true);
        setError('');

        try {
            const tokens = await apiFetch<LoginResponse>('/api/users/login/', {
                method: 'POST',
                body: JSON.stringify({username, password}),
            });
            setToken(tokens.refreshToken, tokens.accessToken);
            console.log('Login successful');
            nav("/dashboard");
        } catch (event) {
            setError(event instanceof Error ? event.message : 'Username or password incorrect');
            
        } finally {
            setLoading(false);
        }

    }
    return (
        <div className="login-page">
            <div className="login-container">
                <h2>Login to Your Account</h2>
                <form className="login-form" onSubmit={handleLogin}>

                    <label htmlFor="username">Username:</label>
                    <input type="username" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                    

                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    
                    {error && <div className="field-error">{error}</div>}
                    <button type="submit" className="login-button" disabled={loading}>{loading ? "Logging In": "Login"}</button> 
                    
                </form>
            </div>
        </div>
    );
}
