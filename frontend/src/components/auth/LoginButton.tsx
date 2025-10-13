import React from 'react';
import { Button } from '@/components/ui/button';
import { useAuthContext } from './AuthProvider';
import { Loader2, Chrome } from 'lucide-react';

interface LoginButtonProps {
  className?: string;
  variant?: 'default' | 'outline' | 'secondary' | 'ghost' | 'link' | 'destructive';
  size?: 'default' | 'sm' | 'lg' | 'icon';
}

const LoginButton: React.FC<LoginButtonProps> = ({ 
  className, 
  variant = 'default',
  size = 'default'
}) => {
  const { signInWithGoogle, loading, error } = useAuthContext();

  const handleGoogleSignIn = async () => {
    try {
      await signInWithGoogle();
    } catch (error) {
      console.error('Google sign-in error:', error);
    }
  };

  return (
    <div className="space-y-2">
      <Button
        onClick={handleGoogleSignIn}
        disabled={loading}
        variant={variant}
        size={size}
        className={`w-full ${className}`}
      >
        {loading ? (
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
        ) : (
          <Chrome className="mr-2 h-4 w-4" />
        )}
        {loading ? 'Signing in...' : 'Continue with Google'}
      </Button>
      
      {error && (
        <p className="text-sm text-red-600 text-center">
          {error}
        </p>
      )}
    </div>
  );
};

export { LoginButton };
export default LoginButton;
