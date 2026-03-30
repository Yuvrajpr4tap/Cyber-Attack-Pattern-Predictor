import React from 'react';
import { motion } from 'framer-motion';

const LoadingSkeleton = () => {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Attack Flow Skeleton */}
      <div className="flex items-center justify-center gap-2">
        {[1, 2, 3, 4].map((i) => (
          <React.Fragment key={i}>
            <div className="h-10 w-32 bg-slate-200 rounded-lg" />
            {i < 4 && <div className="w-4 h-4 bg-slate-200 rounded" />}
          </React.Fragment>
        ))}
      </div>

      {/* Main Card Skeleton */}
      <div className="glass-card rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-slate-200 rounded-xl" />
            <div>
              <div className="h-4 w-24 bg-slate-200 rounded mb-2" />
              <div className="h-8 w-48 bg-slate-200 rounded" />
            </div>
          </div>
          <div className="h-8 w-20 bg-slate-200 rounded-full" />
        </div>
        <div className="h-3 bg-slate-200 rounded-full mb-4" />
        <div className="h-24 bg-slate-200 rounded-xl" />
      </div>

      {/* Top Predictions Skeleton */}
      <div className="glass-card rounded-2xl p-6">
        <div className="h-6 w-48 bg-slate-200 rounded mb-6" />
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="flex items-center gap-4 p-4">
              <div className="w-8 h-8 bg-slate-200 rounded-full" />
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-slate-200 rounded w-3/4" />
                <div className="h-2 bg-slate-200 rounded" />
              </div>
              <div className="h-6 w-16 bg-slate-200 rounded-full" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LoadingSkeleton;
