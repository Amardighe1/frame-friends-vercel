/**
 * API Base URL utility for FarmFriend.
 *
 * Resolution order:
 *  1. NEXT_PUBLIC_API_URL env var (baked in at build time)
 *  2. Capacitor APK: uses Render backend directly (HTTPS)
 *  3. Vercel / dev: empty string (relative URLs proxied by Next.js rewrites)
 */

const ENV_API_URL = process.env.NEXT_PUBLIC_API_URL || '';

// Render backend — used by Capacitor APK for direct HTTPS API calls
const RENDER_API_URL = 'https://frame-friends.onrender.com';

function resolveApiBase(): string {
  // 0) If user configured IP in the app, always use it
  if (typeof window !== 'undefined') {
    const override = localStorage.getItem('farmfriend_api_url');
    if (override) return override.replace(/\/+$/, '');
  }

  // 1) Build-time env var
  if (ENV_API_URL) return ENV_API_URL.replace(/\/+$/, '');

  // 2) Capacitor APK — call Render backend directly over HTTPS
  if (typeof window !== 'undefined' && (window as any).Capacitor) {
    return RENDER_API_URL;
  }

  // 3) Vercel & localhost dev: relative URLs — Next.js rewrites proxy /api/* to Render
  return '';
}

/**
 * Build full API path. Re-resolves base on every call.
 */
export function apiUrl(path: string): string {
  const base = resolveApiBase();
  return `${base}${path}`;
}
