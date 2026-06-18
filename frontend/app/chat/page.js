'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import ChatMessage from '@/components/ChatMessage';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const SUGGESTIONS = {
  doctor: [
    'What are the infection control precautions?',
    'Explain the medication administration policy',
    'What is the patient discharge protocol?',
  ],
  nurse: [
    'What are the infection outbreak precautions?',
    'Explain hand hygiene guidelines',
    'What is the patient safety protocol?',
  ],
  billing_executive: [
    'How many claims are pending?',
    'What is the claim submission process?',
    'Show the top rejected claim reasons',
  ],
  technician: [
    'What is the equipment maintenance schedule?',
    'How to calibrate the ventilator?',
    'What are the safety checks for MRI?',
  ],
  admin: [
    'How many claims are pending?',
    'What are the infection control precautions?',
    'Show the billing summary',
  ],
};

export default function ChatPage() {
  const router = useRouter();
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Load session from sessionStorage
  useEffect(() => {
    const stored = sessionStorage.getItem('medibot_session');
    if (!stored) {
      router.push('/');
      return;
    }
    setSession(JSON.parse(stored));
  }, [router]);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Focus input on mount
  useEffect(() => {
    if (session) inputRef.current?.focus();
  }, [session]);

  const handleLogout = () => {
    sessionStorage.removeItem('medibot_session');
    router.push('/');
  };

  const sendMessage = async (text) => {
    if (!text.trim() || loading || !session) return;

    const userMessage = { role: 'user', text: text.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: text.trim(),
          role: session.role,
        }),
      });

      const data = await res.json();

      const botMessage = {
        role: 'bot',
        answer: data.answer,
        sources: data.sources || [],
        retrieval_type: data.retrieval_type,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = {
        role: 'bot',
        answer: '**Connection Error** — Could not reach the MediBot server. Please make sure the backend is running on `localhost:8000`.',
        sources: [],
        retrieval_type: null,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
  };

  const handleSuggestion = (text) => {
    sendMessage(text);
  };

  if (!session) {
    return (
      <div className="login-page">
        <div style={{ color: 'var(--text-secondary)' }}>Loading...</div>
      </div>
    );
  }

  const roleSuggestions = SUGGESTIONS[session.role] || SUGGESTIONS.admin;

  return (
    <div className="chat-layout">
      {/* Sidebar */}
      <Sidebar session={session} onLogout={handleLogout} />

      {/* Main Chat Area */}
      <main className="chat-main">
        {/* Header */}
        <header className="chat-header">
          <h3>Chat with MediBot</h3>
          <div className="chat-header-status">
            <span className="status-dot" />
            Online
          </div>
        </header>

        {/* Messages */}
        <div className="messages-area">
          {messages.length === 0 ? (
            <div className="messages-empty">
              <div className="messages-empty-icon">🏥</div>
              <h4>Welcome to MediBot</h4>
              <p>
                Ask any question about hospital policies, procedures, or data.
                Your answers are scoped to your role&apos;s accessible collections.
              </p>
              <div className="suggestion-chips">
                {roleSuggestions.map((s, i) => (
                  <button
                    key={i}
                    className="suggestion-chip"
                    onClick={() => handleSuggestion(s)}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <ChatMessage key={idx} message={msg} />
            ))
          )}

          {/* Typing indicator */}
          {loading && (
            <div className="message bot">
              <div className="message-avatar">🏥</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <div className="typing-dots">
                    <span />
                    <span />
                    <span />
                  </div>
                  <span className="typing-label">MediBot is thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="chat-input-area">
          <form className="chat-input-wrapper" onSubmit={handleSubmit}>
            <input
              ref={inputRef}
              id="chat-input"
              className="chat-input"
              type="text"
              placeholder="Ask MediBot a question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
              autoComplete="off"
            />
            <button
              id="send-btn"
              className="send-btn"
              type="submit"
              disabled={loading || !input.trim()}
              aria-label="Send message"
            >
              ➤
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
