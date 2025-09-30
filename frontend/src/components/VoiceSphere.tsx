import { useState, useEffect } from 'react';
import { Mic, MicOff, Volume2, Loader2 } from 'lucide-react';

interface VoiceSphereProps {
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
  onClick: () => void;
  disabled?: boolean;
  'aria-label'?: string;
}

const VoiceSphere = ({ isListening, isProcessing, isSpeaking, onClick, disabled = false, 'aria-label': ariaLabel }: VoiceSphereProps) => {
  const [animationPhase, setAnimationPhase] = useState(0);

  // Animation effect for the sphere
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isListening || isSpeaking) {
      interval = setInterval(() => {
        setAnimationPhase(prev => (prev + 1) % 360);
      }, 50);
    } else {
      setAnimationPhase(0);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isListening, isSpeaking]);

  // Generate waveform bars for listening state
  const generateWaveformBars = () => {
    const bars = [];
    for (let i = 0; i < 20; i++) {
      const height = isListening ? Math.random() * 40 + 10 : 5;
      const delay = i * 0.1;
      bars.push(
        <div
          key={i}
          className="bg-white rounded-full"
          style={{
            width: '3px',
            height: `${height}px`,
            animationDelay: `${delay}s`,
            animation: isListening ? 'waveform 0.5s ease-in-out infinite alternate' : 'none'
          }}
        />
      );
    }
    return bars;
  };

  // Determine the sphere's visual state and content
  const getSphereContent = () => {
    if (isProcessing) {
      return (
        <div className="flex flex-col items-center justify-center space-y-4">
          <Loader2 className="w-12 h-12 text-white animate-spin" />
          <div className="text-white text-sm font-medium">thinking...</div>
        </div>
      );
    }

    if (isSpeaking) {
      return (
        <div className="flex flex-col items-center justify-center space-y-4">
          <Volume2 className="w-12 h-12 text-white animate-pulse" />
          <div className="text-white text-sm font-medium">speaking...</div>
        </div>
      );
    }

    if (isListening) {
      return (
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="flex space-x-1 items-end">
            {generateWaveformBars()}
          </div>
          <div className="text-white text-sm font-medium">listening...</div>
        </div>
      );
    }

    return (
      <div className="flex flex-col items-center justify-center space-y-4">
        <Mic className="w-12 h-12 text-white" />
        <div className="text-white text-sm font-medium">tap to speak</div>
      </div>
    );
  };

  // Determine sphere colors and effects based on state
  const getSphereStyles = () => {
    const baseClasses = "w-32 h-32 rounded-full flex items-center justify-center transition-all duration-300 transform";
    
    if (disabled) {
      return `${baseClasses} bg-gray-500 cursor-not-allowed opacity-50`;
    }
    
    if (isProcessing) {
      return `${baseClasses} bg-yellow-500 shadow-lg shadow-yellow-500/50 animate-pulse cursor-pointer hover:scale-105`;
    }
    
    if (isSpeaking) {
      return `${baseClasses} bg-blue-500 shadow-lg shadow-blue-500/50 cursor-pointer hover:scale-105`;
    }
    
    if (isListening) {
      return `${baseClasses} bg-red-500 shadow-lg shadow-red-500/50 animate-pulse cursor-pointer hover:scale-105`;
    }
    
    return `${baseClasses} bg-yellow-400 hover:bg-yellow-300 shadow-lg shadow-yellow-400/30 cursor-pointer hover:scale-105`;
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      {/* Main Voice Sphere */}
      <div
        className={getSphereStyles()}
        onClick={disabled ? undefined : onClick}
        aria-label={ariaLabel}
        role="button"
        tabIndex={disabled ? -1 : 0}
        onKeyDown={(e) => {
          if (!disabled && (e.key === 'Enter' || e.key === ' ')) {
            e.preventDefault();
            onClick();
          }
        }}
        style={{
          transform: isListening || isSpeaking ? `scale(${1 + Math.sin(animationPhase * Math.PI / 180) * 0.1})` : 'scale(1)',
          boxShadow: isListening || isSpeaking 
            ? `0 0 ${20 + Math.sin(animationPhase * Math.PI / 180) * 10}px rgba(255, 255, 255, 0.3)`
            : undefined
        }}
      >
        {getSphereContent()}
      </div>

      {/* Status indicator dots */}
      <div className="flex space-x-2">
        <div className={`w-2 h-2 rounded-full transition-colors duration-300 ${
          isListening ? 'bg-red-400' : 'bg-slate-600'
        }`} />
        <div className={`w-2 h-2 rounded-full transition-colors duration-300 ${
          isProcessing ? 'bg-yellow-400' : 'bg-slate-600'
        }`} />
        <div className={`w-2 h-2 rounded-full transition-colors duration-300 ${
          isSpeaking ? 'bg-blue-400' : 'bg-slate-600'
        }`} />
      </div>

      {/* CSS for waveform animation */}
      <style jsx>{`
        @keyframes waveform {
          0% { transform: scaleY(0.3); }
          100% { transform: scaleY(1); }
        }
      `}</style>
    </div>
  );
};

export default VoiceSphere;
