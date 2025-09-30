import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Send, Loader2 } from 'lucide-react';

interface TextInputProps {
  onSend: (text: string) => void;
  disabled?: boolean;
}

const TextInput = ({ onSend, disabled = false }: TextInputProps) => {
  const [message, setMessage] = useState('');
  const [isComposing, setIsComposing] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  // Handle Enter key (submit) vs Shift+Enter (new line)
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !isComposing) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Handle composition events for better international input support
  const handleCompositionStart = () => {
    setIsComposing(true);
  };

  const handleCompositionEnd = () => {
    setIsComposing(false);
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        {/* Text input area */}
        <div className="relative">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onCompositionStart={handleCompositionStart}
            onCompositionEnd={handleCompositionEnd}
            placeholder="Type your thoughts here... (Press Enter to send, Shift+Enter for new line)"
            disabled={disabled}
            className="min-h-[120px] max-h-[200px] resize-none bg-slate-800 border-slate-600 text-white placeholder-slate-400 focus:border-yellow-400 focus:ring-yellow-400/20"
            style={{ scrollbarWidth: 'thin' }}
          />
          
          {/* Character count indicator */}
          <div className="absolute bottom-2 right-2 text-xs text-slate-500">
            {message.length}/1000
          </div>
        </div>

        {/* Send button and controls */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 text-sm text-slate-400">
            <span>Press Enter to send</span>
            <span>•</span>
            <span>Shift+Enter for new line</span>
          </div>
          
          <Button
            type="submit"
            disabled={!message.trim() || disabled}
            className="bg-yellow-400 hover:bg-yellow-300 text-slate-900 font-medium px-6 py-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {disabled ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Send className="w-4 h-4 mr-2" />
                Send
              </>
            )}
          </Button>
        </div>
      </form>

      {/* Helpful tips */}
      <div className="mt-4 text-center text-sm text-slate-500">
        <p>
          💡 <strong>Tip:</strong> You can share anything that's on your mind. 
          The more open you are, the better I can help you explore your thoughts and feelings.
        </p>
      </div>
    </div>
  );
};

export default TextInput;
