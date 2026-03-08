/**
 * API Base URL utility for MANDIMITRA.
 *
 * Resolution order:
 *  1. NEXT_PUBLIC_API_URL env var (baked in at build time)
 *  2. Capacitor APK: uses Vercel proxy (HTTPS, no mixed-content)
 *  3. Vercel / dev: empty string (relative URLs proxied by Vercel rewrites)
 */

const ENV_API_URL = process.env.NEXT_PUBLIC_API_URL || '';

// Vercel proxy URL — used by Capacitor APK so all calls stay HTTPS
// Vercel rewrites /api/* → EC2 backend, avoiding Android mixed-content blocks
const VERCEL_API_URL = 'https://mandimitra-rose.vercel.app';

function resolveApiBase(): string {
  // 1) Build-time env var
  if (ENV_API_URL) return ENV_API_URL.replace(/\/+$/, '');

  // 2) Capacitor APK — route via Vercel HTTPS proxy (no mixed content, no cleartext)
  if (typeof window !== 'undefined' && (window as any).Capacitor) {
    const override = localStorage.getItem('mandimitra_api_url');
    if (override) return override.replace(/\/+$/, '');
    return VERCEL_API_URL;
  }

  // 3) Vercel & localhost dev: relative URLs — Vercel rewrites proxy /api/* to EC2
  return '';
}

/**
 * Build full API path. Re-resolves base on every call.
 */
export function apiUrl(path: string): string {
  const base = resolveApiBase();
  return `${base}${path}`;
}
