'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import {
  Leaf,
  TrendingUp,
  Shield,
  BarChart3,
  Cloud,
  Camera,
  Stethoscope,
  ShoppingCart,
  AlertTriangle,
  ArrowRight,
  Sun,
  Bell,
} from 'lucide-react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { useAuth } from '@/contexts/AuthContext';
import { Navbar } from '@/components/layout/Navbar';
import { HeroSection } from '@/components/sections/HeroSection';
import { StatsSection } from '@/components/sections/StatsSection';
import { apiUrl } from '@/lib/api-config';

// ── Lazy-load below-the-fold sections (not needed for FCP) ────────────────
const FeaturesSection = dynamic(
  () => import('@/components/sections/FeaturesSection').then((m) => m.FeaturesSection),
  { ssr: false, loading: () => <div className="h-32" /> }
);
const HowItWorksSection = dynamic(
  () => import('@/components/sections/HowItWorksSection').then((m) => m.HowItWorksSection),
  { ssr: false, loading: () => <div className="h-32" /> }
);
const TestimonialsSection = dynamic(
  () => import('@/components/sections/TestimonialsSection').then((m) => m.TestimonialsSection),
  { ssr: false, loading: () => <div className="h-32" /> }
);
const CTASection = dynamic(
  () => import('@/components/sections/CTASection').then((m) => m.CTASection),
  { ssr: false, loading: () => <div className="h-16" /> }
);
const Footer = dynamic(
  () => import('@/components/layout/Footer').then((m) => m.Footer),
  { ssr: false, loading: () => <div className="h-16" /> }
);

const quickActions = [
  { label: 'पीक तपासा', desc: 'फोटो काढा, रोग ओळखा', icon: Camera, color: 'from-emerald-500 to-emerald-600', href: '/crop-analysis' },
  { label: 'भाव अंदाज', desc: '15 दिवसांचा अंदाज', icon: TrendingUp, color: 'from-amber-500 to-orange-500', href: '/price-forecast' },
  { label: 'मंडी भाव', desc: 'आजचे बाजारभाव', icon: BarChart3, color: 'from-purple-500 to-purple-600', href: '/markets' },
  { label: 'हवामान', desc: 'स्थानिक अंदाज', icon: Cloud, color: 'from-sky-500 to-cyan-500', href: '/weather' },
  { label: 'मंडी विक्री', desc: 'खरेदीदार शोधा', icon: ShoppingCart, color: 'from-rose-500 to-pink-500', href: '/mandi' },
  { label: 'डॉक्टर', desc: 'पशुवैद्यकीय सेवा', icon: Stethoscope, color: 'from-teal-500 to-teal-600', href: '/veterinary' },
  { label: 'आपत्कालीन', desc: 'SOS मदत', icon: AlertTriangle, color: 'from-red-500 to-red-600', href: '/dashboard/farmer' },
];

/* ── Tips carousel ───────────────────────────────────────── */
const dailyTips = [
  'पिकावर कीड दिसल्यास लगेच "पीक तपासा" मध्ये फोटो अपलोड करा.',
  'विक्रीपूर्वी "भाव अंदाज" तपासा — योग्य वेळी विक्री करा.',
  'पावसाळ्यात "हवामान" विभागात दररोज अंदाज पहा.',
  'नवीन खरेदीदार शोधण्यासाठी "मंडी विक्री" वापरा.',
];

/* ── Farmer Dashboard Component ──────────────────────────── */
function FarmerHome({ user }: { user: { full_name: string; role: string } }) {
  const [tipIndex, setTipIndex] = useState(0);

  // Rotate tips every 5s
  useEffect(() => {
    const t = setInterval(() => setTipIndex((i) => (i + 1) % dailyTips.length), 5000);
    return () => clearInterval(t);
  }, []);

  // Fetch market summary (non-blocking, best-effort — result not shown but primes cache)
  useEffect(() => {
    fetch(apiUrl('/api/market/summary'))
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => {});
  }, []);

  const firstName = user.full_name?.split(' ')[0] || 'शेतकरी';
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'सुप्रभात' : hour < 17 ? 'नमस्कार' : 'शुभ संध्याकाळ';

  return (
    <div className="min-h-[100dvh] bg-slate-50" style={{ paddingBottom: 'var(--page-bottom-padding)' }}>
      {/* ── Header ────────────────────────────────── */}
      <div className="bg-gradient-to-br from-emerald-600 via-emerald-500 to-teal-500 text-white" style={{ paddingTop: 'var(--sat, 0px)' }}>
        <div className="px-4 pt-4 pb-6">
          {/* Top bar */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
                <Leaf className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight">मंडीमित्र</span>
            </div>
            <Link href="/dashboard/farmer" className="relative p-2 bg-white/15 rounded-xl backdrop-blur-sm">
              <Bell className="w-5 h-5" />
              <div className="absolute top-1 right-1 w-2 h-2 bg-amber-400 rounded-full" />
            </Link>
          </div>

          {/* Greeting */}
          <div className="mb-1">
            <h1 className="text-2xl font-bold">{greeting}, {firstName}! 👋</h1>
            <p className="text-emerald-100 text-sm mt-0.5">तुमच्या शेतीसाठी आज काय करायचे?</p>
          </div>
        </div>

        {/* ── Tip card (overlapping) ───────────────── */}
        <div className="px-4 -mb-6">
          <motion.div
            key={tipIndex}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-lg shadow-emerald-900/10 p-4 flex items-start gap-3"
          >
            <div className="w-8 h-8 bg-amber-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <Sun className="w-4 h-4 text-amber-600" />
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-amber-600 mb-0.5">💡 आजची टिप</p>
              <p className="text-sm text-slate-700 leading-relaxed">{dailyTips[tipIndex]}</p>
            </div>
          </motion.div>
        </div>
      </div>

      {/* ── Quick Actions Grid ─────────────────────── */}
      <div className="px-4 mt-10">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-base font-bold text-slate-800">सेवा</h2>
          <span className="text-xs text-slate-400">सर्व वैशिष्ट्ये</span>
        </div>
        <div className="grid grid-cols-3 sm:grid-cols-4 gap-2 sm:gap-3">
          {quickActions.map((action, i) => (
            <Link key={action.href} href={action.href} className="group">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                className="flex flex-col items-center"
              >
                <div className={`w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br ${action.color} rounded-2xl flex items-center justify-center shadow-md mb-1.5 group-active:scale-95 transition-transform`}>
                  <action.icon className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                </div>
                <span className="text-[11px] font-medium text-slate-700 text-center leading-tight">
                  {action.label}
                </span>
              </motion.div>
            </Link>
          ))}
        </div>
      </div>

      {/* ── Feature Highlight Cards ─────────────────── */}
      <div className="px-4 mt-6 space-y-3">
        <h2 className="text-base font-bold text-slate-800">प्रमुख वैशिष्ट्ये</h2>

        <Link href="/crop-analysis" className="block">
          <div className="bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl p-4 text-white shadow-md flex items-center gap-4">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <Camera className="w-6 h-6" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-bold text-sm">📸 पीक रोग ओळख</h3>
              <p className="text-xs text-emerald-100 mt-0.5">फोटो काढा → AI तात्काळ रोग ओळखतो → उपाय मिळवा</p>
            </div>
            <ArrowRight className="w-5 h-5 flex-shrink-0 opacity-70" />
          </div>
        </Link>

        <Link href="/price-forecast" className="block">
          <div className="bg-gradient-to-r from-amber-500 to-orange-500 rounded-2xl p-4 text-white shadow-md flex items-center gap-4">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <TrendingUp className="w-6 h-6" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-bold text-sm">📈 भाव अंदाज</h3>
              <p className="text-xs text-amber-100 mt-0.5">15 दिवसांचा अंदाज → योग्य वेळी विक्री करा</p>
            </div>
            <ArrowRight className="w-5 h-5 flex-shrink-0 opacity-70" />
          </div>
        </Link>

        <Link href="/markets" className="block">
          <div className="bg-gradient-to-r from-purple-500 to-indigo-500 rounded-2xl p-4 text-white shadow-md flex items-center gap-4">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <BarChart3 className="w-6 h-6" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-bold text-sm">💰 आजचे मंडी भाव</h3>
              <p className="text-xs text-purple-100 mt-0.5">400+ बाजारांचे रिअल-टाइम दर</p>
            </div>
            <ArrowRight className="w-5 h-5 flex-shrink-0 opacity-70" />
          </div>
        </Link>
      </div>

      {/* ── Quick Help Section ──────────────────────── */}
      <div className="px-4 mt-6 mb-8">
        <div className="bg-red-50 border border-red-100 rounded-2xl p-4 flex items-center gap-3">
          <div className="w-10 h-10 bg-red-500 rounded-xl flex items-center justify-center flex-shrink-0">
            <AlertTriangle className="w-5 h-5 text-white" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-bold text-sm text-red-800">🚨 आपत्कालीन मदत</h3>
            <p className="text-xs text-red-600 mt-0.5">जनावरांसाठी तात्काळ डॉक्टर बोलवा</p>
          </div>
          <Link href="/dashboard/farmer" className="px-3 py-1.5 bg-red-500 text-white text-xs font-bold rounded-lg flex-shrink-0">
            SOS
          </Link>
        </div>
      </div>
    </div>
  );
}

/* ── Landing Page (for non-logged-in visitors) ───────────── */
function LandingPage() {
  const [isScrolled, setIsScrolled] = useState(false);
  const rafRef = useRef<number | null>(null);

  // Throttle scroll handler with requestAnimationFrame — fires at most once per frame
  const handleScroll = useCallback(() => {
    if (rafRef.current !== null) return;
    rafRef.current = requestAnimationFrame(() => {
      setIsScrolled(window.scrollY > 50);
      rafRef.current = null;
    });
  }, []);

  useEffect(() => {
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
  }, [handleScroll]);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-emerald-50/30">
      <Navbar isScrolled={isScrolled} />
      <HeroSection />
      <StatsSection />
      <FeaturesSection />
      <HowItWorksSection />
      <TestimonialsSection />
      <CTASection />
      <Footer />
    </main>
  );
}

/* ── Page Router ─────────────────────────────────────────── */
export default function HomePage() {
  const { user, loading } = useAuth();

  // loading is now false on first render when a cached user exists
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="flex flex-col items-center gap-3">
          <div className="w-12 h-12 bg-emerald-500 rounded-2xl flex items-center justify-center animate-pulse">
            <Leaf className="w-6 h-6 text-white" />
          </div>
          <p className="text-sm text-slate-500">लोड होत आहे...</p>
        </div>
      </div>
    );
  }

  if (user && user.role === 'farmer') {
    return <FarmerHome user={user} />;
  }

  return <LandingPage />;
}
