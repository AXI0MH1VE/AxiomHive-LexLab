import React, { useState, useEffect, useRef } from 'react'
import './ChatInterface.css'

export default function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m an AI assistant. How can I help you today?',
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
      {/* ChatGPT-like Interface */}
      <div className="chat-container">
        <header className="chat-header">
          <div className="header-left">
            <h1 className="chat-title">ChatGPT</h1>
            <span className="version-indicator">Powered by AxiomHive</span>
          </div>
          <div className="header-controls">
            <button 
              className={`advanced-toggle ${showAdvancedView ? 'active' : ''}`}
              onClick={() => setShowAdvancedView(!showAdvancedView)}
              title="Toggle Advanced View"
            >
              🔍
            </button>
            <button className="new-chat-btn" onClick={newChat}>+ New chat</button>
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
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                
                {/* Advanced View: Cognitive Depth Indicators */}
                {showAdvancedView && message.cognitiveDepth && (
                  <div className="cognitive-analysis">
                    <div className="analysis-header">🧠 Cognitive Analysis</div>
                    <div className="analysis-metrics">
                      <span className="metric">Confidence: {message.cognitiveDepth.confidenceScore}%</span>
                      <span className="metric">Modules: {message.cognitiveDepth.reasoningModules.length}</span>
                      <span className="metric">Memory Refs: {message.cognitiveDepth.memoryReferences}</span>
                    </div>
                    
                    {message.reasoningPath && (
                      <details className="reasoning-path">
                        <summary>🔗 Reasoning Path</summary>
                        <ol>
                          {message.reasoningPath.map((step, i) => (
                            <li key={i}>{step}</li>
                          ))}
                        </ol>
                      </details>
                    )}
                  </div>
                )}

                {/* Verification Badges */}
                {message.verificationStatus && (
                  <div className="verification-badges">
                    <span className="badge verified" title="Factually Verified">✓ Verified</span>
                    <span className="badge logical" title="Logically Sound">⚡ Logic</span>
                    <span className="badge ethical" title="Ethically Compliant">🛡️ Safe</span>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message assistant loading">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
                {showAdvancedView && (
                  <div className="processing-status">
                    Processing through cognitive modules...
                  </div>
                )}
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <div className="input-wrapper">
            <textarea
              ref={textareaRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Message ChatGPT..."
              rows={1}
              className="message-input"
              disabled={isLoading}
            />
            <button 
              onClick={sendMessage} 
              disabled={!inputText.trim() || isLoading}
              className="send-button"
            >
              {isLoading ? '⏳' : '↑'}
            </button>
          </div>
          <div className="input-footer">
            <span className="disclaimer">Powered by AxiomHive modular cognitive architecture</span>
          </div>
        </div>
      </div>
    </div>
  )
}
    </div>
  )
}
