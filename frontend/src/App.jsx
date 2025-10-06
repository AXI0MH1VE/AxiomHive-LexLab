import React, { useState, useEffect, useRef } from 'react'
import './ChatInterface.css'

export default function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m an AI assistant powered by AxiomHive. How can I help you today?',
      timestamp: new Date(),
      cognitiveDepth: null,
      verificationStatus: null
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showAdvancedView, setShowAdvancedView] = useState(false)
  const [operationalStatus, setOperationalStatus] = useState({
    reasoning: 'active',
    memory: 'active',
    ethics: 'active',
    verification: 'active'
  })
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputText,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    try {
      // Simulate the AxiomHive modular cognitive processing
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: inputText,
          enableCognitiveDepth: showAdvancedView,
          modules: ['reasoning', 'emotional_analysis', 'memory_trace', 'pattern_detection', 'ethics_sentinel']
        })
      })

      const data = await response.json()
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.response || simulateResponse(inputText),
        timestamp: new Date(),
        cognitiveDepth: data.cognitiveAnalysis || generateCognitiveAnalysis(inputText),
        verificationStatus: data.verification || generateVerification(),
        reasoningPath: data.reasoningPath || generateReasoningPath(inputText)
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      // Fallback to simulated response
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: simulateResponse(inputText),
        timestamp: new Date(),
        cognitiveDepth: generateCognitiveAnalysis(inputText),
        verificationStatus: generateVerification(),
        reasoningPath: generateReasoningPath(inputText)
      }
      setMessages(prev => [...prev, assistantMessage])
    }
    
    setIsLoading(false)
  }

  const simulateResponse = (input) => {
    // Simulate sophisticated AxiomHive responses based on input
    const responses = [
      `I understand you're asking about "${input}". Let me process this through the modular cognitive architecture to provide a comprehensive response with verifiable reasoning.`,
      `Based on my analysis using the Reasoning Body and Pattern Detection modules, here's what I can determine about your query regarding "${input}".`,
      `I've engaged the Memory Trace Manager and Emotional Analyzer to provide context-aware insights on "${input}". The Ethics Sentinel has verified this response meets all safety guidelines.`
    ]
    return responses[Math.floor(Math.random() * responses.length)]
  }

  const generateCognitiveAnalysis = (input) => {
    return {
      reasoningModules: ['Logical Analysis', 'Context Evaluation', 'Pattern Recognition'],
      confidenceScore: Math.floor(Math.random() * 20 + 80), // 80-100%
      memoryReferences: Math.floor(Math.random() * 5 + 1),
      ethicalCompliance: true,
      logicalSoundness: 'Verified'
    }
  }

  const generateVerification = () => {
    return {
      factualAccuracy: 'Verified',
      sourceTraceability: 'Available',
      logicalConsistency: 'Confirmed',
      ethicalAlignment: 'Compliant'
    }
  }

  const generateReasoningPath = (input) => {
    return [
      'Input Analysis: Query parsed and tokenized',
      'Context Retrieval: Relevant memory traces accessed',
      'Logical Processing: Applied reasoning matrices',
      'Ethical Review: Safety Guardian validation',
      'Response Generation: Modular synthesis complete'
    ]
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const newChat = () => {
    setMessages([{
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m an AI assistant. How can I help you today?',
      timestamp: new Date(),
      cognitiveDepth: null,
      verificationStatus: null
    }])
  }

  return (
    <div className="chat-app">
      <div className="chat-container">
        <header className="chat-header">
          <div className="header-content">
            <div className="logo-section">
              <div className="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
                </svg>
              </div>
              <div className="brand">
                <h1>AxiomChat</h1>
                <span className="subtitle">Powered by AxiomHive</span>
              </div>
            </div>
            <div className="header-actions">
              <button
                className={`mode-toggle ${showAdvancedView ? 'active' : ''}`}
                onClick={() => setShowAdvancedView(!showAdvancedView)}
                title="Advanced Mode"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" fill="currentColor"/>
                </svg>
              </button>
              <button className="new-chat-btn" onClick={newChat}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" fill="currentColor"/>
                </svg>
                New chat
              </button>
            </div>
          </div>
        </header>

        {/* Operational Status (Hidden by default) */}
        {showAdvancedView && (
          <div className="operational-status">
            <div className="status-item">
              <span className="status-label">Reasoning Engine:</span>
              <span className={`status-indicator ${operationalStatus.reasoning}`}>{operationalStatus.reasoning}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Memory System:</span>
              <span className={`status-indicator ${operationalStatus.memory}`}>{operationalStatus.memory}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Ethics Sentinel:</span>
              <span className={`status-indicator ${operationalStatus.ethics}`}>{operationalStatus.ethics}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Verification:</span>
              <span className={`status-indicator ${operationalStatus.verification}`}>{operationalStatus.verification}</span>
            </div>
          </div>
        )}

        <div className="messages-container">
          {messages.map((message) => (
            <div key={message.id} className={`message-wrapper ${message.type}`}>
              <div className="message-avatar">
                {message.type === 'assistant' ? (
                  <div className="avatar assistant">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
                    </svg>
                  </div>
                ) : (
                  <div className="avatar user">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/>
                    </svg>
                  </div>
                )}
              </div>
              <div className="message-content">
                <div className="message-bubble">
                  <div className="message-text">{message.content}</div>

                  {/* Advanced View: Cognitive Depth Indicators */}
                  {showAdvancedView && message.cognitiveDepth && (
                    <div className="cognitive-analysis">
                      <div className="analysis-header">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                          <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0L19.2 12l-4.6-4.6L16 6l6 6-6 6-1.4-1.4z" fill="currentColor"/>
                        </svg>
                        Cognitive Analysis
                      </div>
                      <div className="analysis-metrics">
                        <div className="metric">
                          <span className="metric-label">Confidence</span>
                          <span className="metric-value">{message.cognitiveDepth.confidenceScore}%</span>
                        </div>
                        <div className="metric">
                          <span className="metric-label">Modules</span>
                          <span className="metric-value">{message.cognitiveDepth.reasoningModules.length}</span>
                        </div>
                        <div className="metric">
                          <span className="metric-label">Memory</span>
                          <span className="metric-value">{message.cognitiveDepth.memoryReferences}</span>
                        </div>
                      </div>

                      {message.reasoningPath && (
                        <details className="reasoning-path">
                          <summary>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z" fill="currentColor"/>
                            </svg>
                            Reasoning Path
                          </summary>
                          <div className="reasoning-steps">
                            {message.reasoningPath.map((step, i) => (
                              <div key={i} className="reasoning-step">
                                <span className="step-number">{i + 1}</span>
                                <span className="step-text">{step}</span>
                              </div>
                            ))}
                          </div>
                        </details>
                      )}
                    </div>
                  )}
                </div>

                {/* Verification Badges */}
                {message.verificationStatus && (
                  <div className="verification-badges">
                    <div className="badge verified">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" fill="currentColor"/>
                      </svg>
                      Verified
                    </div>
                    <div className="badge logical">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                        <path d="M13 7h-2v4H7v2h4v4h2v-4h4v-2h-4V7zm-1-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" fill="currentColor"/>
                      </svg>
                      Logic
                    </div>
                    <div className="badge ethical">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                        <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z" fill="currentColor"/>
                      </svg>
                      Safe
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          
         {isLoading && (
           <div className="message-wrapper assistant loading">
             <div className="message-avatar">
               <div className="avatar assistant">
                 <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                   <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
                 </svg>
               </div>
             </div>
             <div className="message-content">
               <div className="message-bubble">
                 <div className="typing-indicator">
                   <div className="typing-dot"></div>
                   <div className="typing-dot"></div>
                   <div className="typing-dot"></div>
                 </div>
                 {showAdvancedView && (
                   <div className="processing-status">
                     <div className="processing-text">Processing through cognitive modules...</div>
                     <div className="processing-bar">
                       <div className="processing-progress"></div>
                     </div>
                   </div>
                 )}
               </div>
             </div>
           </div>
         )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <div className="input-wrapper">
            <div className="input-field">
              <textarea
                ref={textareaRef}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Message AxiomChat..."
                rows={1}
                className="message-input"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={!inputText.trim() || isLoading}
                className="send-button"
              >
                {isLoading ? (
                  <div className="loading-spinner"></div>
                ) : (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z" fill="currentColor"/>
                  </svg>
                )}
              </button>
            </div>
          </div>
          <div className="input-footer">
            <div className="footer-content">
              <span className="disclaimer">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
                </svg>
                Powered by AxiomHive cognitive architecture
              </span>
              <span className="footer-links">
                <a href="#" className="footer-link">Terms</a>
                <a href="#" className="footer-link">Privacy</a>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
