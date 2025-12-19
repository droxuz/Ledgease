import './LoginPage.css';

export default function LoginPage(){
    return (
        <div className="login-page">
            <div className="login-container">
                <h2>Login to Your Account</h2>
                <form className="login-form">
                    <label htmlFor="email">Email:</label>
                    <input type="email" id="email" name="email" required />

                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" required />
                    
                    <button type="submit" className="login-button">Login</button>      
                </form>
            </div>
        </div>
    );
}
