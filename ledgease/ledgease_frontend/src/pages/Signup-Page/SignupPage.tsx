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
    username?: string;
    email?: string;
    password?: string;
};


export default function SignupPage() {
    const nav = useNavigate();
    const [username, setUsername] = React.useState('');
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [error, setError] = React.useState<FieldErrors>({});
    const [loading, setLoading] = React.useState(false);
    const [touched, setTouched] = React.useState<{[key: string]: boolean}>({});
    const isClientValid = !error.username && !error.email && !error.password;
    
    function extractErrorMessages(err: any): string[] {
    if (!err || typeof err !== "object") return ["An unexpected error occurred."];

    if (Array.isArray(err.non_field_errors)) return err.non_field_errors;

    const out: string[] = [];
    for (const v of Object.values(err)) {
        if (Array.isArray(v)) out.push(...v);
    }
    return out.length ? out : ["An unexpected error occurred."];
    }
    
    function validateUsername(username: string): string | undefined{
        if (!username.trim()) {
            return "Username is required.";
        }
        if (username.length < 6 || username.length > 20) {
            return "Username must be between 6 and 20 characters.";
        }
        return undefined;
    }
    
    function validateEmail(email: string): string | undefined{
        if (!email.trim()) {
            return "Email is required.";
        }
        if (!/\S+@\S+\.\S+/.test(email)) {
            return "Email is invalid.";
        }
        return undefined;
    }

    function validatePassword(password: string): string | undefined{
        if (!password) {
            return "Password is required.";
        }
        if (password.length < 8) {
            return "Password must be at least 8 characters long.";
        }
        if (/^\d+$/.test(password)) {
            return "Password must contain at least one uppercase letter.";
        }
        return undefined;
    }

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
        } catch (err) {
            console.error('Signup failed', err);
            const messages = extractErrorMessages(err);
            setError({ ...error, ...messages });
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
                    <input type="text" id="username" name="username" value={username} 
                    onChange={(e) => {
                        const v = e.target.value; 
                        setUsername(v); 
                        setError((prev) => ({ ...prev, username: validateUsername(v) }));
                    }}
                        onBlur={() => {
                        setTouched({...touched, username: true});
                        setError((prev) => ({ ...prev, username: validateUsername(username) }));
                    }}/>
                    {touched.username && error.username && (<p className="form-error">{error.username}</p>)}

                    <label htmlFor="email">Email:</label>   
                    <input type="email" id="email" name="email" value={email} 
                    onChange={(e) => {
                        const v = e.target.value; 
                        setEmail(v); 
                        setError((prev) => ({ ...prev, email: validateEmail(v) }));
                    }} 
                    onBlur={() => {
                        setTouched({...touched, email: true});
                        setError((prev) => ({ ...prev, email: validateEmail(email) }));
                    }}/>
                    {touched.email && error.email && (<p className="form-error">{error.email}</p>)}

                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" value={password} 
                    onChange={(e) => {
                        const v = e.target.value; 
                        setPassword(v); 
                        setError((prev) => ({ ...prev, password: validatePassword(v) }));
                    }} 
                    onBlur={() => {
                        setTouched({...touched, password: true});
                        setError((prev) => ({ ...prev, password: validatePassword(password) }));
                    }}
                    />
                    {touched.email && error.password && (<p className="form-error">{error.password}</p>)}
                    
                    <button type="submit" className="signup-button" disabled={!isClientValid||loading}>{loading ? "Creating..." : "Create Account"}</button>
                      
                </form>
            </div>
        </div>
    );
}