import React, { useState } from 'react';
import { Button } from './button';
import { Sheet, SheetContent, SheetTrigger } from './sheet';
import { Menu, X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MobileNavProps {
  children: React.ReactNode;
  className?: string;
}

const MobileNav: React.FC<MobileNavProps> = ({ children, className }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className={cn('block md:hidden', className)}>
      <Sheet open={isOpen} onOpenChange={setIsOpen}>
        <SheetTrigger asChild>
          <Button variant="outline" size="icon" className="md:hidden">
            <Menu className="h-4 w-4" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64">
          <div className="flex flex-col space-y-4 mt-4">
            {children}
          </div>
        </SheetContent>
      </Sheet>
    </div>
  );
};

export default MobileNav;
