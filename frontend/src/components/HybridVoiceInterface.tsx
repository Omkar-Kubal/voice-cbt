import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic, MicOff, Volume2, Brain, MessageSquare, Loader2 } from 'lucide-react';

interface HybridVoiceInterfaceProps {
  onTextSubmit: (text: string) => void;
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
}

const HybridVoiceInterface: React.FC<HybridVoiceInterfaceProps> = ({
  onTextSubmit,
  isListening,
  isProcessing,
  isSpeaking
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessingAudio, setIsProcessingAudio] = useState(false);
  const [error, setError] = useState('');
  const [showTextInput, setShowTextInput] = useState(false);
  const [manualText, setManualText] = useState('');
  const [speechRecognitionFailed, setSpeechRecognitionFailed] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';
      recognitionRef.current.maxAlternatives = 1;

      recognitionRef.current.onstart = () => {
        console.log('Speech recognition started');
        setIsRecording(true);
        setError('');
        setSpeechRecognitionFailed(false);
      };

      recognitionRef.current.onresult = (event: any) => {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        setTranscript(transcript);
        
        if (event.results[current].isFinal) {
          console.log('Final transcript:', transcript);
          // Automatically submit the transcript
          onTextSubmit(transcript);
          setTranscript('');
        }
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsRecording(false);
        setSpeechRecognitionFailed(true);
        
        if (event.error === 'network') {
          setError('Speech recognition failed due to network issues. Please use text input instead.');
          setShowTextInput(true);
        } else if (event.error === 'not-allowed') {
          setError('Microphone access denied. Please allow microphone access and try again.');
        } else {
          setError(`Speech recognition error: ${event.error}. Please use text input instead.`);
          setShowTextInput(true);
        }
      };

      recognitionRef.current.onend = () => {
        console.log('Speech recognition ended');
        setIsRecording(false);
      };
    } else {
      setError('Speech recognition not supported in this browser. Please use text input.');
      setShowTextInput(true);
    }
  }, [onTextSubmit]);

  const startListening = () => {
    console.log('Start listening clicked');
    if (recognitionRef.current && !speechRecognitionFailed) {
      setTranscript('');
      setError('');
      setShowTextInput(false);
      try {
        recognitionRef.current.start();
      } catch (error) {
        console.error('Error starting speech recognition:', error);
        setError('Error starting speech recognition. Please use text input.');
        setShowTextInput(true);
      }
    } else {
      setError('Speech recognition not available. Please use text input.');
      setShowTextInput(true);
    }
  };

  const stopListening = () => {
    console.log('Stop listening clicked');
    if (recognitionRef.current && isRecording) {
      recognitionRef.current.stop();
    }
  };

  const handleManualSubmit = () => {
    if (manualText.trim()) {
      onTextSubmit(manualText);
      setManualText('');
      setShowTextInput(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleManualSubmit();
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Brain className="h-5 w-5" />
          <span>Smart Voice Interface</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Voice Controls */}
        <div className="flex items-center justify-center space-x-4">
          <Button
            onClick={isRecording ? stopListening : startListening}
            disabled={isProcessing || isSpeaking}
            className={`w-16 h-16 rounded-full ${
              isRecording 
                ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {isRecording ? <MicOff className="h-8 w-8" /> : <Mic className="h-8 w-8" />}
          </Button>
        </div>

        {/* Status and Transcript */}
        <div className="text-center space-y-2">
          {isRecording && (
            <div className="text-blue-400 animate-pulse">
              <Mic className="h-4 w-4 inline mr-2" />
              Listening... Speak now
            </div>
          )}
          
          {isProcessing && (
            <div className="text-yellow-400 animate-pulse">
              <Brain className="h-4 w-4 inline mr-2" />
              AI is thinking...
            </div>
          )}

          {isSpeaking && (
            <div className="text-green-400 animate-pulse">
              <Volume2 className="h-4 w-4 inline mr-2" />
              AI is speaking...
            </div>
          )}

          {transcript && (
            <div className="p-3 bg-slate-800 rounded-lg">
              <p className="text-sm text-slate-300">You said:</p>
              <p className="text-white font-medium">{transcript}</p>
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-900 border border-red-600 rounded-lg">
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          {!isRecording && !isProcessing && !isSpeaking && !transcript && !error && (
            <div className="text-slate-400">
              <p>Click the microphone to start speaking</p>
              <p className="text-sm">Your speech will be converted to text automatically</p>
            </div>
          )}
        </div>

        {/* Manual Text Input Fallback */}
        {showTextInput && (
          <div className="space-y-3 p-4 bg-slate-800 rounded-lg">
            <p className="text-sm text-slate-300">Voice recognition failed. Please type your message:</p>
            <div className="flex space-x-2">
              <input
                type="text"
                value={manualText}
                onChange={(e) => setManualText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message here..."
                className="flex-1 px-3 py-2 bg-slate-700 text-white rounded border border-slate-600 focus:border-blue-500 focus:outline-none"
                autoFocus
              />
              <Button
                onClick={handleManualSubmit}
                disabled={!manualText.trim()}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <MessageSquare className="h-4 w-4 mr-2" />
                Send
              </Button>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="text-center text-sm text-slate-400">
          <p>Click the microphone to start speaking</p>
          <p>If voice recognition fails, you can type your message</p>
          <p className="text-xs text-slate-500 mt-2">
            Hybrid approach: Voice first, text fallback
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default HybridVoiceInterface;
