'use client';

import { useEffect, useState } from 'react';
import { MotionConfig } from 'framer-motion';
import { AuthProvider } from '@/contexts/AuthContext';

export function Providers({ children }: { children: React.ReactNode }) {
  const [reduceMotion, setReduceMotion] = useState(false);

  useEffect(() => {
    const isNative =
      typeof window !== 'undefined' &&
      (window as any).Capacitor?.isNativePlatform?.() === true;
    if (isNative) {
      setReduceMotion(true);
    }
  }, []);

  return (
    <MotionConfig reducedMotion={reduceMotion ? 'always' : 'user'}>
      <AuthProvider>{children}</AuthProvider>
    </MotionConfig>
  );
}
