import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import "@canva/app-ui-kit/styles.css";
import './App.css'
import Home from './Home';
import UserEntry from './UserEntry';
import { AppUiProvider } from "@canva/app-ui-kit";

function App() {
  
  return (
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/userEntry" element={<UserEntry/>} />
        </Routes>
      </Router>
  );
}

export default App;
