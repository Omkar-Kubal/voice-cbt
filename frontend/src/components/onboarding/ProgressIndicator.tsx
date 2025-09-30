import { Progress } from "@/components/ui/progress";

interface ProgressIndicatorProps {
  currentStep: number;
  totalSteps: number;
}

export const ProgressIndicator = ({ currentStep, totalSteps }: ProgressIndicatorProps) => {
  const progressValue = (currentStep / totalSteps) * 100;

  return (
    <div className="fixed top-0 left-0 right-0 z-50 bg-background/90 backdrop-blur-sm border-b border-border">
      <div className="max-w-md mx-auto px-6 py-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-muted-foreground">
            Step {currentStep} of {totalSteps}
          </span>
          <span className="text-sm font-medium text-muted-foreground">
            {Math.round(progressValue)}%
          </span>
        </div>
        <Progress value={progressValue} className="h-2" />
      </div>
    </div>
  );
};