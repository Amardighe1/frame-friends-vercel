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

  // 2) Always use Render backend directly to avoid Vercel rewrite limits and proxy connection errors
  if (typeof window !== 'undefined') {
    // If we're on localhost, we can still use relative paths for dev rewrites,
    // but on Vercel production, we MUST use the direct Render URL.
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return '';
    }
    return RENDER_API_URL;
  }

  // Server-side / fallback
  return RENDER_API_URL;
}

/**
 * Build full API path. Re-resolves base on every call.
 */
export function apiUrl(path: string): string {
  const base = resolveApiBase();
  return `${base}${path}`;
}
