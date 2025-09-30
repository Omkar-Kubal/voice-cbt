import { Button } from "@/components/ui/button";

export const DifferentFromChatGPTScreen = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8 text-center">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground">
          how is that different from chatgpt?
        </h2>

        {/* Illustration Placeholder */}
        <div className="bg-brand-green/30 rounded-2xl h-48 w-full flex items-center justify-center">
          <span className="text-6xl">📚</span>
        </div>

        {/* Descriptive Paragraph */}
        <p className="text-lg text-muted-foreground leading-relaxed">
          Pravesti's built for mental health, trained on research-backed data
        </p>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button className="btn-hero w-full">
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
};