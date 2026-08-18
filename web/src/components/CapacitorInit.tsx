'use client';

import { useEffect } from 'react';

/**
 * Detects Capacitor native platform and configures the status bar + safe area CSS vars.
 *
 * Strategy:
 *  1. StatusBar.setOverlaysWebView(false) → Android gives system status bar its own
 *     space; WebView starts BELOW it (no top overlay).
 *  2. We still read safe-area-inset-* from CSS env() and mirror them to CSS custom
 *     properties (--sat, --sab, --sal, --sar) so components can use them in calc().
 *  3. A small bottom safe area (for home indicator) is always applied via CSS var
 *     so the BottomNav and page content never go behind the gesture indicator.
 */
export function CapacitorInit() {
  useEffect(() => {
    const isCapacitor =
      typeof window !== 'undefined' &&
      (window as any).Capacitor?.isNativePlatform?.() === true;

    if (isCapacitor) {
      document.body.classList.add('capacitor-app');

      // Configure status bar: non-overlapping so WebView has its own space
      import('@capacitor/status-bar')
        .then(({ StatusBar, Style }) => {
          StatusBar.setOverlaysWebView({ overlay: false });
          StatusBar.setStyle({ style: Style.Light });
          StatusBar.setBackgroundColor({ color: '#FFFFFF' });
        })
        .catch(() => {
          // StatusBar plugin not installed — skip
        });
    }

    // Update CSS custom properties from safe-area-inset env() values.
    // We do this by reading a test element that has padding set to env() values.
    // This is necessary because JS cannot read env() directly.
    const updateSafeAreaVars = () => {
      const el = document.createElement('div');
      el.style.cssText = `
        position: fixed;
        top: 0; left: 0;
        width: 0; height: 0;
        padding-top: env(safe-area-inset-top, 0px);
        padding-bottom: env(safe-area-inset-bottom, 0px);
        padding-left: env(safe-area-inset-left, 0px);
        padding-right: env(safe-area-inset-right, 0px);
        pointer-events: none;
        visibility: hidden;
      `;
      document.body.appendChild(el);
      const computed = getComputedStyle(el);
      const top    = computed.paddingTop    || '0px';
      const bottom = computed.paddingBottom || '0px';
      const left   = computed.paddingLeft   || '0px';
      const right  = computed.paddingRight  || '0px';
      document.documentElement.style.setProperty('--sat', top);
      document.documentElement.style.setProperty('--sab', bottom);
      document.documentElement.style.setProperty('--sal', left);
      document.documentElement.style.setProperty('--sar', right);
      // Update page-bottom-padding
      const navHeight = 64;
      const bottomPx = parseInt(bottom) || 0;
      document.documentElement.style.setProperty(
        '--page-bottom-padding',
        `${navHeight + bottomPx + 8}px`
      );
      document.body.removeChild(el);
    };

    updateSafeAreaVars();
    window.addEventListener('resize', updateSafeAreaVars);
    return () => window.removeEventListener('resize', updateSafeAreaVars);
  }, []);

  return null;
}
