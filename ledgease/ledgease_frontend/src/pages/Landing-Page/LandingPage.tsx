import './landingpage.css';
import NavigationBar from '../../components/Navigation-Bar/NavigationBar';



export default function LandingPage(){
    return (
        <div className="landing-page">
            <NavigationBar />
        <div className="landing-content">
            
            <h1>Welcome to Ledgease</h1>
            <p>Your ultimate solution for managing ledgers with ease and efficiency.</p>
            <button className="get-started-button">Get Started</button>
        </div>
        </div>
        
    );
}