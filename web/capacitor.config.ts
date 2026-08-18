import type { CapacitorConfig } from '@capacitor/cli';

const isLocalBuild = process.env.CAPACITOR_LOCAL_BUILD === 'true';

const config: CapacitorConfig = {
  appId: 'com.farmfriend.app',
  appName: 'FarmFriend',
  webDir: 'out',
  ...(isLocalBuild
    ? {}
    : {
        server: {
          url: 'https://frame-friends.vercel.app',
          androidScheme: 'https',
          allowNavigation: [
            'frame-friends.vercel.app',
            '*.vercel.app',
            'frame-friends.onrender.com',
            '*.onrender.com',
          ],
        },
      }),
  android: {
    backgroundColor: '#FFFFFF',
    allowMixedContent: isLocalBuild,
    webContentsDebuggingEnabled: false,
  },
  plugins: {
    StatusBar: {
      overlaysWebView: false,
      style: 'LIGHT',
      backgroundColor: '#FFFFFF',
    },
    Keyboard: {
      resize: 'body',
      style: 'LIGHT',
    },
  },
};

export default config;
