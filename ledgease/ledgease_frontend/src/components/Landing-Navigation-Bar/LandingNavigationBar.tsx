import './LandingNavigationBar.css';
import placeholderLogo from '../../assets/agmasen.jpg';
import { Link } from 'react-router-dom';

export default function NavigationBar() {
    return (
    <div className="nav-bar-container">
        <nav className="nav-bar">
            <div className="nav-logo">
                <img className="logo" src={placeholderLogo} alt="Logo" />
            </div> 
                <ul className="nav-links">
                    <li><a href="#features">Features</a></li>  
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            <div className='nav-cta-container'>
                <a className='nav-cta' href="/login">
                    <span className='nav-cta-a'>
                    LOGIN
                    </span>
                </a>

                <a className='nav-cta-alt' href="/signup">
                    <span className='nav-cta-a'>
                        SIGN UP
                    </span>
                </a>
            </div>
        </nav>

            
    </div>
    );
}