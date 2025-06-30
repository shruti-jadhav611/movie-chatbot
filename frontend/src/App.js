import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
    const [chat, setChat] = useState([
    { sender: 'bot', text: 'Hi I am your Bot,Ask me anything about your favorite movie—its story, cast, recommendations, etc.' }
  ]);
  const [loading, setLoading] = useState(false);

  const sendQuery = async () => {
    if (query.trim() === '') return;
  
    const userMessage = { sender: 'user', text: query };
    setChat(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });

      const data = await res.json();
      const botMessage = { sender: 'bot', text: data.response || "Sorry, something went wrong." };
      setChat(prev => [...prev, botMessage]);
    } catch (error) {
      console.error("Fetch error:", error);
      setChat(prev => [...prev, { sender: 'bot', text: "Failed to connect to the server." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') sendQuery();
  };

  return (
    <div className="chat-container">
      <h2>Movie Chatbot</h2>
      <div className="chat-box">

        {chat.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
  <strong>{msg.sender === 'user' ? 'You' : 'Bot'}:</strong>
  {msg.text.includes('\n') ? (
    msg.text.split('\n').map((line, i) => (
      <div key={i}>{line}</div>
    ))
  ) : (
    <span> {msg.text}</span>
  )}
      </div>
        ))}
        {loading && <div className="message bot">Bot: <i>Typing...</i></div>}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about a movie..."
        />
        <button onClick={sendQuery} disabled={loading}>Send</button>
      </div>
    </div>
  );
}

export default App;
