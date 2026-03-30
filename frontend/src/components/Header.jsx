import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheckIcon, ChartBarIcon, BoltIcon, CpuChipIcon } from '@heroicons/react/24/outline';

const StatCard = ({ icon: Icon, label, value, trend }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="glass-card rounded-2xl p-6 hover:shadow-2xl transition-all duration-300 group"
  >
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2.5 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 text-white group-hover:scale-110 transition-transform duration-300">
            <Icon className="w-5 h-5" />
          </div>
          <p className="text-sm font-medium text-slate-600">{label}</p>
        </div>
        <p className="text-3xl font-bold text-slate-900 mt-2">{value}</p>
        {trend && (
          <p className="text-xs text-green-600 font-medium mt-2 flex items-center gap-1">
            <span>↗</span> {trend}
          </p>
        )}
      </div>
    </div>
  </motion.div>
);

const Header = ({ stats }) => {
  return (
    <div className="mb-8">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-100 text-primary-700 text-sm font-medium mb-6">
          <ShieldCheckIcon className="w-4 h-4" />
          <span>AI-Powered Threat Intelligence</span>
        </div>
        
        <h1 className="text-5xl md:text-6xl font-display font-bold mb-4 bg-gradient-to-r from-slate-900 via-primary-800 to-slate-900 bg-clip-text text-transparent">
          Attack Pattern Predictor
        </h1>
        
        <p className="text-lg text-slate-600 max-w-2xl mx-auto font-light">
          Advanced machine learning system predicting next-stage cyber attacks with{' '}
          <span className="font-semibold text-primary-600">90%+ accuracy</span>
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          icon={CpuChipIcon}
          label="Model Accuracy"
          value="90.2%"
          trend="+5% this month"
        />
        <StatCard
          icon={ChartBarIcon}
          label="Predictions"
          value={stats?.predictions || "1.2K"}
          trend="+12% this week"
        />
        <StatCard
          icon={BoltIcon}
          label="Response Time"
          value="< 100ms"
          trend="Optimized"
        />
        <StatCard
          icon={ShieldCheckIcon}
          label="Threat Level"
          value="Medium"
          trend="Stable"
        />
      </div>
    </div>
  );
};

export default Header;
