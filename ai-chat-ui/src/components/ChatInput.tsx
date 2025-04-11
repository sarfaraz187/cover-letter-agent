import React, { useState, useRef, useEffect } from 'react';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  return (
    <div className="border-t border-gray-700 bg-dark py-4">
      <form 
        onSubmit={handleSubmit}
        className="max-w-4xl mx-auto px-4 sm:px-6"
      >
        <div className="relative rounded-lg border border-gray-600 bg-gray-700 shadow-sm">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message AI Assistant..."
            className="w-full resize-none bg-transparent py-3 pl-4 pr-12 text-white focus:outline-none focus:ring-0"
            rows={1}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!message.trim() || isLoading}
            className={`absolute right-2 bottom-2.5 rounded-md p-1 
              ${message.trim() && !isLoading
                ? 'bg-primary text-white hover:bg-primary/90'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
              }`}
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </div>
        <div className="mt-2 text-xs text-center text-gray-400">
          AI Assistant is designed to be helpful, harmless, and honest.
        </div>
      </form>
    </div>
  );
};

export default ChatInput; 