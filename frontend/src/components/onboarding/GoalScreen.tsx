import { useState } from "react";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

interface GoalScreenProps {
  onAnswer: (answer: string) => void;
}

export const GoalScreen = ({ onAnswer }: GoalScreenProps) => {
  const [selectedGoal, setSelectedGoal] = useState<string>("");

  const goals = [
    "Reduce stress",
    "Manage anxiety",
    "Improve my mood",
    "Practice mindfulness"
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground text-center">
          what is your main goal for today?
        </h2>

        {/* Options List */}
        <RadioGroup value={selectedGoal} onValueChange={setSelectedGoal} className="space-y-4">
          {goals.map((goal, index) => (
            <div key={index} className="relative">
              <RadioGroupItem 
                value={goal} 
                id={goal}
                className="sr-only"
              />
              <Label 
                htmlFor={goal}
                className={`
                  block w-full p-4 rounded-lg border-2 cursor-pointer text-center transition-colors duration-200
                  ${selectedGoal === goal 
                    ? 'bg-primary text-primary-foreground border-primary' 
                    : 'bg-card text-foreground border-border hover:bg-secondary'
                  }
                `}
              >
                {goal}
              </Label>
            </div>
          ))}
        </RadioGroup>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button 
            className="btn-hero w-full" 
            disabled={!selectedGoal}
            onClick={() => selectedGoal && onAnswer(selectedGoal)}
          >
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
};