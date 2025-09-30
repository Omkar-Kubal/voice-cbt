import { useState } from "react";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

interface HowDidYouHearScreenProps {
  onAnswer: (answer: string) => void;
}

export const HowDidYouHearScreen = ({ onAnswer }: HowDidYouHearScreenProps) => {
  const [selectedOption, setSelectedOption] = useState<string>("");

  const options = [
    { value: "instagram", label: "instagram", icon: "📸" },
    { value: "tiktok", label: "tiktok", icon: "🎵" },
    { value: "youtube", label: "youtube", icon: "▶️" },
    { value: "google", label: "google", icon: "🔍" },
    { value: "facebook", label: "facebook", icon: "📘" },
    { value: "friend/family", label: "friend/family", icon: "🧑‍🤝‍🧑" }
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground text-center">
          how did you hear about Pravesti?
        </h2>

        {/* Options List */}
        <RadioGroup value={selectedOption} onValueChange={setSelectedOption} className="space-y-4">
          {options.map((option) => (
            <div key={option.value} className="relative">
              <RadioGroupItem 
                value={option.value} 
                id={option.value}
                className="sr-only"
              />
              <Label 
                htmlFor={option.value}
                className={`
                  flex items-center gap-3 w-full p-4 rounded-lg border-2 cursor-pointer transition-colors duration-200
                  ${selectedOption === option.value 
                    ? 'bg-primary text-primary-foreground border-primary' 
                    : 'bg-card text-foreground border-border hover:bg-secondary'
                  }
                `}
              >
                <span className="text-xl">{option.icon}</span>
                <span>{option.label}</span>
              </Label>
            </div>
          ))}
        </RadioGroup>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button 
            className="btn-hero w-full" 
            disabled={!selectedOption}
            onClick={() => selectedOption && onAnswer(selectedOption)}
          >
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
};