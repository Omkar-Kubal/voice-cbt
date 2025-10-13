import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Mic, MicOff } from 'lucide-react';

const VoiceTest: React.FC = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState('');
  const recognitionRef = useRef<any>(null);

  const startListening = () => {
    try {
      // Check if speech recognition is available
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        setError('Speech recognition not supported in this browser');
        return;
      }

      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';
      recognitionRef.current.maxAlternatives = 1;

      recognitionRef.current.onstart = () => {
        console.log('Speech recognition started');
        setIsListening(true);
        setError('');
      };

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        console.log('Transcript:', transcript);
        setTranscript(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        let errorMessage = `Speech recognition error: ${event.error}`;
        
        // Handle specific error types
        if (event.error === 'network') {
          errorMessage = 'Network error: Please check your internet connection and try again.';
        } else if (event.error === 'not-allowed') {
          errorMessage = 'Microphone access denied: Please allow microphone access and refresh the page.';
        } else if (event.error === 'no-speech') {
          errorMessage = 'No speech detected: Please try speaking louder or closer to the microphone.';
        }
        
        setError(errorMessage);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        console.log('Speech recognition ended');
        setIsListening(false);
      };

      recognitionRef.current.start();
    } catch (err) {
      console.error('Error starting speech recognition:', err);
      setError(`Error: ${err}`);
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsListening(false);
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Voice Test</h2>
      
      <div className="space-y-4">
        <div className="flex items-center space-x-4">
          <Button
            onClick={isListening ? stopListening : startListening}
            className={`w-16 h-16 rounded-full ${
              isListening 
                ? 'bg-red-500 hover:bg-red-600' 
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {isListening ? <MicOff className="h-8 w-8" /> : <Mic className="h-8 w-8" />}
          </Button>
          
          <div>
            <p className="text-sm text-gray-600">
              {isListening ? 'Listening...' : 'Click to start listening'}
            </p>
          </div>
        </div>

        {transcript && (
          <div className="p-4 bg-gray-100 rounded">
            <p className="font-medium">Transcript:</p>
            <p>{transcript}</p>
          </div>
        )}

        {error && (
          <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            <p className="font-medium">Error:</p>
            <p>{error}</p>
          </div>
        )}

        <div className="text-sm text-gray-500">
          <p>Browser support:</p>
          <p>• Speech Recognition: {('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) ? '✅ Yes' : '❌ No'}</p>
          <p>• Speech Synthesis: {'speechSynthesis' in window ? '✅ Yes' : '❌ No'}</p>
        </div>
      </div>
    </div>
  );
};

export default VoiceTest;
