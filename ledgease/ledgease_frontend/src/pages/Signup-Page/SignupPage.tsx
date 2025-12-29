import './SignupPage.css'
import {useNavigate} from 'react-router-dom';
import {apiFetch, setToken} from '../../lib/api';
import React from 'react';

type RegisterResponse = {
    ALERT?: string;
};
type LoginResponse = {
    accessToken: string;
    refreshToken: string;
};

export default function SignupPage() {
    const nav = useNavigate();
    const [username, setUsername] = React.useState('');
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [error, setError] = React.useState('');
    const [loading, setLoading] = React.useState(false);

    async function handleSignup(event: React.FormEvent) {
        event.preventDefault();
        setLoading(true);
        setError('');
        // Handle signup logic here (e.g., API call)
        try {
            //Register
            await apiFetch<RegisterResponse>('/api/users/register/', {
                method: 'POST',
                body: JSON.stringify({username, email, password}),
            });
            const tokens = await apiFetch<LoginResponse>('/api/users/login/', {
                method: 'POST',
                body: JSON.stringify({username, password}),   
            });
            setToken(tokens.refreshToken, tokens.accessToken);
            console.log('Signup successful');
            nav('/dashboard');
        } catch (event) {
            setError(event instanceof Error ? event.message : 'Signup failed');
        } finally {
            setLoading(false);
        }
    }
    return (
        <div className="signup-page">  
            <div className="signup-container">
                <h2>Create Your Account</h2>
                <form className="signup-form" onSubmit={handleSignup}>

                    <label htmlFor="username">Username:</label>
                    <input type="text" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} required />

                    <label htmlFor="email">Email:</label>   
                    <input type="email" id="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} required />

                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    
                    <button type="submit" className="signup-button" disabled={loading}>{loading ? "Creating..." : "Create Account"}</button>      

                </form>
            </div>
        </div>
    );
}