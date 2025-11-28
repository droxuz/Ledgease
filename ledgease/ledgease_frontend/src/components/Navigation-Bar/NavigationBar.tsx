import './navigationbar.css';

export default function NavigationBar() {
    return (
        <nav className="navigation-bar">
            <div className="nav-logo">Ledgease</div>
            <ul className="nav-links">
                <li><a href="#features">Features</a></li>  
                <li><a href="#pricing">Pricing</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    );
}