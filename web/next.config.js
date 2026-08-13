/** @type {import('next').NextConfig} */

const isCapacitorBuild = process.env.CAPACITOR_BUILD === 'true';
const backendUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL || 'https://frame-friends.onrender.com';


const nextConfig = {
  reactStrictMode: true,
  // Only disable image optimization for Capacitor (static export) builds
  images: {
    unoptimized: isCapacitorBuild,
    domains: ['images.unsplash.com'],
  },
  // Strip console.* calls in production for smaller output & no accidental leaks
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? { exclude: ['error', 'warn'] } : false,
  },
  // TF.js needs these webpack settings to work in browser builds
  webpack: (config, { isServer }) => {
    // NOTE: webpack cache is intentionally NOT disabled here.
    // Keeping the filesystem cache makes HMR fast (only changed modules rebuild).
    // Only Capacitor static builds get a special flag if needed.
    if (isCapacitorBuild) {
      config.cache = false;
    }

    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
        crypto: false,
      };
    }
    return config;
  },
  ...(isCapacitorBuild
    ? {
        output: 'export',
        trailingSlash: true,
      }
    : backendUrl
    ? {
        async rewrites() {
          return [
            {
              source: '/api/:path*',
              destination: `${backendUrl}/api/:path*`,
            },
          ];
        },
      }
    : {}),
};

module.exports = nextConfig;
