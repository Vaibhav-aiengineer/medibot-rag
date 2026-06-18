'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  const isBot = message.role === 'bot';

  // Detect RBAC-blocked messages
  const isRbacBlocked = isBot && message.answer && (
    message.answer.includes('do not have access') ||
    message.answer.includes('does not have access')
  );

  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      {/* Avatar */}
      <div className="message-avatar">
        {isUser ? '👤' : '🏥'}
      </div>

      {/* Content */}
      <div className="message-content">
        {/* Bubble */}
        <div className={`message-bubble ${isRbacBlocked ? 'rbac-blocked' : ''}`}>
          {isUser ? (
            <span>{message.text}</span>
          ) : (
            <>
              {isRbacBlocked && (
                <div className="rbac-warning-icon">
                  ⚠️ Access Restricted
                </div>
              )}
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.answer}
              </ReactMarkdown>
            </>
          )}
        </div>

        {/* Meta — sources & retrieval badge (bot only) */}
        {isBot && (
          <div className="message-meta">
            {/* Retrieval type badge */}
            {message.retrieval_type && (
              <span className={`retrieval-badge ${message.retrieval_type}`}>
                {message.retrieval_type === 'hybrid_rag' ? '🔗 Hybrid RAG' : '🗄️ SQL RAG'}
              </span>
            )}

            {/* Source citations */}
            {message.sources && message.sources.length > 0 && message.sources.map((src, idx) => (
              <span key={idx} className="source-chip">
                <span className="source-icon">📄</span>
                {src.source_document}
                {src.section_title && src.section_title !== 'Unknown' && (
                  <> › {src.section_title}</>
                )}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
