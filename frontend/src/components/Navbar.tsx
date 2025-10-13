import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Menu, X, User, LogOut } from 'lucide-react';
import { useUserSessionContext } from '@/components/auth/UserSessionProvider';

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const { user, isLoggedIn, logout } = useUserSessionContext();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled 
        ? 'bg-background/95 backdrop-blur-sm shadow-soft' 
        : 'bg-transparent'
    }`}>
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
              <span className="text-accent-foreground font-bold text-lg">P</span>
            </div>
            <span className="text-xl font-bold text-foreground">
              Pravesti
            </span>
          </div>

          {/* Navigation Links - Hidden on mobile */}
          <div className="hidden md:flex items-center space-x-8">
            <a 
              href="#features" 
              className="text-muted-foreground hover:text-foreground transition-colors duration-200 font-medium"
            >
              Features
            </a>
            <a 
              href="#how-it-works" 
              className="text-muted-foreground hover:text-foreground transition-colors duration-200 font-medium"
            >
              How It Works
            </a>
            <a 
              href="#about" 
              className="text-muted-foreground hover:text-foreground transition-colors duration-200 font-medium"
            >
              About
            </a>
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm">
                    {user?.name?.charAt(0).toUpperCase() || 'U'}
                  </div>
                  <span className="text-sm font-medium">{user?.name}</span>
                </div>
                {user?.email?.includes('admin') ? (
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => window.location.href = '/admin'}
                  >
                    <User className="h-4 w-4 mr-2" />
                    Admin Dashboard
                  </Button>
                ) : (
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => window.location.href = '/app'}
                  >
                    <User className="h-4 w-4 mr-2" />
                    Start Session
                  </Button>
                )}
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={logout}
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </Button>
              </div>
            ) : (
              <>
                <Button 
                  variant="ghost" 
                  className="btn-ghost"
                  onClick={() => window.location.href = '/login'}
                >
                  Log In
                </Button>
                <Button 
                  className="btn-hero"
                  onClick={() => window.location.href = '/signup'}
                >
                  Sign Up
                </Button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;