import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX, 
  Settings, 
  Brain, 
  Heart,
  Zap,
  Clock
} from 'lucide-react';

interface VoiceSettings {
  rate: number;
  volume: number;
  pitch: number;
  emotion: string;
}

interface EnhancedVoiceInterfaceProps {
  onVoiceStart: () => void;
  onVoiceStop: () => void;
  onTextSubmit: (text: string) => void;
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
  currentEmotion?: string;
  responseText?: string;
  className?: string;
}

const EnhancedVoiceInterface: React.FC<EnhancedVoiceInterfaceProps> = ({
  onVoiceStart,
  onVoiceStop,
  onTextSubmit,
  isListening,
  isProcessing,
  isSpeaking,
  currentEmotion,
  responseText,
  className = ""
}) => {
  const [voiceSettings, setVoiceSettings] = useState<VoiceSettings>({
    rate: 180,
    volume: 0.9,
    pitch: 1.0,
    emotion: 'neutral'
  });
  
  const [showSettings, setShowSettings] = useState(false);
  const [voiceAnalysis, setVoiceAnalysis] = useState<any>(null);
  const [isGeneratingVoice, setIsGeneratingVoice] = useState(false);
  
  const audioRef = useRef<HTMLAudioElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Emotion-based voice parameters
  const emotionVoiceConfigs = {
    sad: { rate: 150, volume: 0.8, pitch: 0.9, color: 'blue' },
    angry: { rate: 160, volume: 0.7, pitch: 0.8, color: 'red' },
    anxious: { rate: 170, volume: 0.85, pitch: 1.0, color: 'yellow' },
    happy: { rate: 200, volume: 0.95, pitch: 1.1, color: 'green' },
    neutral: { rate: 180, volume: 0.9, pitch: 1.0, color: 'gray' }
  };

  // Update voice settings based on emotion
  useEffect(() => {
    if (currentEmotion && emotionVoiceConfigs[currentEmotion as keyof typeof emotionVoiceConfigs]) {
      const config = emotionVoiceConfigs[currentEmotion as keyof typeof emotionVoiceConfigs];
      setVoiceSettings(prev => ({
        ...prev,
        rate: config.rate,
        volume: config.volume,
        pitch: config.pitch,
        emotion: currentEmotion
      }));
    }
  }, [currentEmotion]);

  const startRecording = async () => {
    try {
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
      
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        processAudioBlob(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current.start();
      onVoiceStart();
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      onVoiceStop();
    }
  };

  const processAudioBlob = async (audioBlob: Blob) => {
    try {
      // Convert blob to base64
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64Audio = reader.result?.toString().split(',')[1];
        if (base64Audio) {
          // Process with enhanced audio processing
          const response = await fetch('/api/v1/audio/process/enhanced', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audio_data: base64Audio })
          });
          
          const result = await response.json();
          setVoiceAnalysis(result);
          
          // Continue with normal processing
          onTextSubmit(''); // Trigger text processing
        }
      };
      reader.readAsDataURL(audioBlob);
    } catch (error) {
      console.error('Error processing audio:', error);
    }
  };

  const generateEnhancedVoice = async (text: string) => {
    if (!text) return;
    
    setIsGeneratingVoice(true);
    try {
      const response = await fetch('/api/v1/audio/tts/enhanced', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text,
          emotion: voiceSettings.emotion,
          voice_instructions: {
            rate: voiceSettings.rate,
            volume: voiceSettings.volume,
            pitch: voiceSettings.pitch
          }
        })
      });
      
      const result = await response.json();
      
      if (result.success && result.output_file) {
        // Play the generated audio
        if (audioRef.current) {
          audioRef.current.src = result.output_file;
          audioRef.current.play();
        }
      }
    } catch (error) {
      console.error('Error generating voice:', error);
    } finally {
      setIsGeneratingVoice(false);
    }
  };

  const getEmotionColor = (emotion: string) => {
    const config = emotionVoiceConfigs[emotion as keyof typeof emotionVoiceConfigs];
    return config?.color || 'gray';
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Voice Analysis Display */}
      {voiceAnalysis && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Brain className="h-5 w-5" />
              <span>Voice Analysis</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium">Quality Score:</span>
                <Badge variant="secondary" className="ml-2">
                  {voiceAnalysis.quality_score}/100
                </Badge>
              </div>
              <div>
                <span className="font-medium">Duration:</span>
                <span className="ml-2">{voiceAnalysis.audio_analysis?.duration?.toFixed(2)}s</span>
              </div>
              <div>
                <span className="font-medium">Sample Rate:</span>
                <span className="ml-2">{voiceAnalysis.audio_analysis?.sample_rate}Hz</span>
              </div>
              <div>
                <span className="font-medium">Channels:</span>
                <span className="ml-2">{voiceAnalysis.audio_analysis?.channels}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Main Voice Interface */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span className="flex items-center space-x-2">
              <Heart className="h-5 w-5" />
              <span>Enhanced Voice Interface</span>
            </span>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowSettings(!showSettings)}
            >
              <Settings className="h-4 w-4" />
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Voice Controls */}
          <div className="flex items-center justify-center space-x-4">
            <Button
              onClick={isListening ? stopRecording : startRecording}
              disabled={isProcessing || isSpeaking}
              className={`w-16 h-16 rounded-full ${
                isListening 
                  ? 'bg-red-500 hover:bg-red-600' 
                  : 'bg-blue-500 hover:bg-blue-600'
              }`}
            >
              {isListening ? <MicOff className="h-8 w-8" /> : <Mic className="h-8 w-8" />}
            </Button>
            
            {responseText && (
              <Button
                onClick={() => generateEnhancedVoice(responseText)}
                disabled={isGeneratingVoice}
                variant="outline"
                className="w-16 h-16 rounded-full"
              >
                {isGeneratingVoice ? (
                  <Clock className="h-8 w-8 animate-spin" />
                ) : (
                  <Volume2 className="h-8 w-8" />
                )}
              </Button>
            )}
          </div>

          {/* Status Indicators */}
          <div className="flex items-center justify-center space-x-4">
            {isListening && (
              <Badge variant="destructive" className="animate-pulse">
                <Mic className="h-3 w-3 mr-1" />
                Listening...
              </Badge>
            )}
            {isProcessing && (
              <Badge variant="secondary" className="animate-pulse">
                <Brain className="h-3 w-3 mr-1" />
                Processing...
              </Badge>
            )}
            {isSpeaking && (
              <Badge variant="default" className="animate-pulse">
                <Volume2 className="h-3 w-3 mr-1" />
                Speaking...
              </Badge>
            )}
            {currentEmotion && (
              <Badge 
                variant="outline" 
                style={{ 
                  borderColor: `var(--${getEmotionColor(currentEmotion)}-500)`,
                  color: `var(--${getEmotionColor(currentEmotion)}-700)`
                }}
              >
                {currentEmotion}
              </Badge>
            )}
          </div>

          {/* Voice Settings */}
          {showSettings && (
            <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
              <h4 className="font-medium">Voice Settings</h4>
              
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium">Speech Rate: {voiceSettings.rate} WPM</label>
                  <Slider
                    value={[voiceSettings.rate]}
                    onValueChange={([value]) => setVoiceSettings(prev => ({ ...prev, rate: value }))}
                    min={100}
                    max={300}
                    step={10}
                    className="mt-2"
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium">Volume: {Math.round(voiceSettings.volume * 100)}%</label>
                  <Slider
                    value={[voiceSettings.volume]}
                    onValueChange={([value]) => setVoiceSettings(prev => ({ ...prev, volume: value }))}
                    min={0.1}
                    max={1.0}
                    step={0.1}
                    className="mt-2"
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium">Pitch: {voiceSettings.pitch.toFixed(1)}</label>
                  <Slider
                    value={[voiceSettings.pitch]}
                    onValueChange={([value]) => setVoiceSettings(prev => ({ ...prev, pitch: value }))}
                    min={0.5}
                    max={2.0}
                    step={0.1}
                    className="mt-2"
                  />
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Hidden audio element for playback */}
      <audio ref={audioRef} className="hidden" />
    </div>
  );
};

export default EnhancedVoiceInterface;
