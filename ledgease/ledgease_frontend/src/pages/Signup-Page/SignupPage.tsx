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

type FieldErrors = {
    username?: string[];
    email?: string[];
    password?: string[];
    non_field_errors?: string[];
};

export default function SignupPage() {
    const nav = useNavigate();
    const [username, setUsername] = React.useState('');
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [fieldErrors, setFieldErrors] = React.useState<FieldErrors>({});
    const [error, setError] = React.useState<FieldErrors>({});
    const [loading, setLoading] = React.useState(false);
    const isClientValid = !error.username && !error.email && !error.password;
    
    async function handleSignup(event: React.FormEvent) {
        event.preventDefault();
        setLoading(true);
        setError({});
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
        } catch (err : any) { 
            console.error('Signup failed', err);
            if (err && typeof err === 'object'){
                setFieldErrors(err as FieldErrors);
                
            }
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
                    <input type="text" id="username" name="username" value={username} onChange={(e) => {setUsername(e.target.value); }} />
                    {fieldErrors.username?.map((msg, i) => (
                        <p key={i} className="field-error">{msg}</p>
                    ))}

                    <label htmlFor="email">Email:</label>   
                    <input type="email" id="email" name="email" value={email} onChange={(e) => {setEmail(e.target.value); }} />
                    {fieldErrors.email?.map((msg, i) => (
                        <p key={i} className="field-error">{msg}</p>
                    ))}

                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" value={password} onChange={(e) => {setPassword(e.target.value); }} />
                    {fieldErrors.password?.map((msg, i) => (
                        <p key={i} className="field-error">{msg}</p>
                    ))}
                    {fieldErrors.non_field_errors?.map((msg, i) => (
                        <p key={i} className="field-error">{msg}</p>
                    ))} 
                    <button type="submit" className="signup-button" disabled={!isClientValid||loading}>{loading ? "Creating..." : "Create Account"}</button>
                    
                </form>
            </div>
        </div>
    );
}