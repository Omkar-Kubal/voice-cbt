import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic, MicOff, Volume2, Brain, Loader2 } from 'lucide-react';

interface RealVoiceInterfaceProps {
  onTextSubmit: (text: string) => void;
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
}

const RealVoiceInterface: React.FC<RealVoiceInterfaceProps> = ({
  onTextSubmit,
  isListening,
  isProcessing,
  isSpeaking
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessingAudio, setIsProcessingAudio] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      console.log('Starting audio recording...');
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          sampleRate: 44100,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        } 
      });
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        console.log('Audio recorded, size:', audioBlob.size, 'bytes');
        
        // Process the audio with the backend
        await processAudio(audioBlob);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
      console.log('Recording started');
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Microphone access denied. Please allow microphone access and try again.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      console.log('Recording stopped');
    }
  };

  const processAudio = async (audioBlob: Blob) => {
    setIsProcessingAudio(true);
    setTranscript('Processing your speech...');
    
    try {
      // Convert audio to base64
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64Audio = reader.result?.toString().split(',')[1];
        if (base64Audio) {
          try {
            // Send to backend for speech-to-text processing
            const response = await fetch('http://localhost:8000/api/v1/process', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ audio_data: base64Audio })
            });
            
            if (response.ok) {
              const result = await response.json();
              if (result.transcript) {
                setTranscript(result.transcript);
                console.log('Speech-to-text result:', result.transcript);
                // Automatically submit the transcript
                onTextSubmit(result.transcript);
                setTranscript('');
              } else {
                setTranscript('Could not understand speech. Please try again.');
              }
            } else {
              throw new Error('Backend processing failed');
            }
          } catch (error) {
            console.error('Error processing audio:', error);
            setTranscript('Error processing audio. Please try again or use text mode.');
          }
        }
      };
      reader.readAsDataURL(audioBlob);
    } catch (error) {
      console.error('Error processing audio:', error);
      setTranscript('Error processing audio. Please try again or use text mode.');
    } finally {
      setIsProcessingAudio(false);
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
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isProcessing || isSpeaking || isProcessingAudio}
            className={`w-16 h-16 rounded-full ${
              isRecording 
                ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {isProcessingAudio ? (
              <Loader2 className="h-8 w-8 animate-spin" />
            ) : isRecording ? (
              <MicOff className="h-8 w-8" />
            ) : (
              <Mic className="h-8 w-8" />
            )}
          </Button>
        </div>

        {/* Status and Transcript */}
        <div className="text-center space-y-2">
          {isRecording && (
            <div className="text-blue-400 animate-pulse">
              <Mic className="h-4 w-4 inline mr-2" />
              Recording... Speak now
            </div>
          )}
          
          {isProcessingAudio && (
            <div className="text-yellow-400 animate-pulse">
              <Loader2 className="h-4 w-4 inline mr-2 animate-spin" />
              Processing your speech...
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

          {!isRecording && !isProcessing && !isSpeaking && !isProcessingAudio && !transcript && (
            <div className="text-slate-400">
              <p>Click the microphone to start speaking</p>
              <p className="text-sm">Your speech will be automatically converted to text</p>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="text-center text-sm text-slate-400">
          <p>Click the microphone and speak naturally</p>
          <p>Your speech will be automatically processed and sent to the AI</p>
          <p className="text-xs text-slate-500 mt-2">
            Powered by AI speech recognition
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default RealVoiceInterface;
