import React from 'react';
import { cn } from '@/lib/utils';

interface ResponsiveGridProps {
  children: React.ReactNode;
  className?: string;
  mobileCols?: number;
  tabletCols?: number;
  desktopCols?: number;
}

const ResponsiveGrid: React.FC<ResponsiveGridProps> = ({
  children,
  className,
  mobileCols = 1,
  tabletCols = 2,
  desktopCols = 3
}) => {
  return (
    <div
      className={cn(
        'grid gap-4',
        `grid-cols-${mobileCols}`,
        `md:grid-cols-${tabletCols}`,
        `lg:grid-cols-${desktopCols}`,
        className
      )}
    >
      {children}
    </div>
  );
};

export default ResponsiveGrid;
