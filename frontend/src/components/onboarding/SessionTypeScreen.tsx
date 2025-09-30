import { useState } from "react";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

interface SessionTypeScreenProps {
  onSelect: (type: string) => void;
}

export const SessionTypeScreen = ({ onSelect }: SessionTypeScreenProps) => {
  const [selectedType, setSelectedType] = useState<string>("");

  const sessionTypes = [
    { 
      value: "voice", 
      label: "Start Vocal Session", 
      icon: "🎤",
      description: "Talk naturally with AI through voice conversation"
    },
    { 
      value: "text", 
      label: "Start Text Session", 
      icon: "💭",
      description: "Chat with AI through written messages"
    }
  ];

  const handleContinue = () => {
    if (selectedType) {
      onSelect(selectedType);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground text-center">
          how would you like to continue?
        </h2>

        {/* Options List */}
        <RadioGroup value={selectedType} onValueChange={setSelectedType} className="space-y-4">
          {sessionTypes.map((type) => (
            <div key={type.value} className="relative">
              <RadioGroupItem 
                value={type.value} 
                id={type.value}
                className="sr-only"
              />
              <Label 
                htmlFor={type.value}
                className={`
                  flex flex-col items-center gap-2 w-full p-6 rounded-lg border-2 cursor-pointer transition-colors duration-200 text-center
                  ${selectedType === type.value 
                    ? 'bg-primary text-primary-foreground border-primary' 
                    : 'bg-card text-foreground border-border hover:bg-secondary'
                  }
                `}
              >
                <span className="text-4xl">{type.icon}</span>
                <span className="text-lg font-semibold">{type.label}</span>
                <span className="text-sm opacity-80">{type.description}</span>
              </Label>
            </div>
          ))}
        </RadioGroup>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button 
            className="btn-hero w-full" 
            disabled={!selectedType}
            onClick={handleContinue}
          >
            Start Session
          </Button>
        </div>
      </div>
    </div>
  );
};