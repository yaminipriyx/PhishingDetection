import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-container">
      <h1>🔍 Phishing Detector</h1>
      <p>Select what you want to analyze:</p>
      <Link to="/url-phishing">
        <button>🌍 Check URL</button>
      </Link>
      <Link to="/email-phishing">
        <button>📧 Check Email</button>
      </Link>
      <Link to="/sms-phishing">
        <button>📱 Check SMS</button>
      </Link>
    </div>
  );
}

export default Home;
