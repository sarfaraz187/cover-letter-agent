import React, { useState, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import { Message } from '../types';
import * as apiService from '../services/api';

const SAMPLE_MESSAGES: Message[] = [
  {
    id: '1',
    role: 'assistant',
    content: 'Hello! I\'m your AI assistant. How can I help you today?',
    timestamp: new Date()
  }
];

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>(SAMPLE_MESSAGES);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: new Date()
    };
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsLoading(true);
    
    // Call API for response
    try {
      console.log('Sending message to API...');
      // Connect to the Flask API
      const aiResponseContent = await apiService.sendMessage(content);
      
      const aiResponse: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: aiResponseContent,
        timestamp: new Date()
      };
      
      setMessages(prevMessages => [...prevMessages, aiResponse]);
    } catch (error) {
      console.error('Error getting AI response:', error);
      
      // Add an error message
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again later.`,
        timestamp: new Date()
      };
      
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-dark text-white">
      <div className="flex-1 overflow-y-auto">
        {messages.map(message => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isLoading && (
          <div className="py-5 bg-gray-700">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 flex">
              <div className="mr-4 flex-shrink-0">
                <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
                  <div className="dot-typing"></div>
                </div>
              </div>
              <div className="flex-1">
                <div className="text-sm font-semibold text-gray-300 mb-1">
                  AI Assistant
                </div>
                <div className="text-gray-100">Thinking...</div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow; 