import './navigationbar.css';
import placeholderLogo from '../../assets/agmasen.jpg';
export default function NavigationBar() {
    return (
        <div className="navigation-bar-container">
        <nav className="navigation-bar">
            <div className="nav-logo">
                <img className="logo" src={placeholderLogo} alt="Logo" />
                </div> 
            <ul className="nav-links">
                <li><a href="#features">Features</a></li>  
                <li><a href="#pricing">Pricing</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
            
        </nav>
        </div>
    );
}