import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./Home";
import UrlPhishing from "./UrlPhishing";
import EmailPhishing from "./EmailPhishing";  // Import Email Page
import SmsPhishing from "./SmsPhishing";  // Import SMS Page
import "./styles.css";

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">🏠 Home</Link>
        <Link to="/url-phishing">🌍 URL Phishing</Link>
        <Link to="/email-phishing">📧 Email Phishing</Link>
        <Link to="/sms-phishing">📱 SMS Phishing</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/url-phishing" element={<UrlPhishing />} />
        <Route path="/email-phishing" element={<EmailPhishing />} />
        <Route path="/sms-phishing" element={<SmsPhishing />} />
      </Routes>
    </Router>
  );
}

export default App;


