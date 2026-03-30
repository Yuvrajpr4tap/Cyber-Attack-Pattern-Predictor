import React from 'react';
import { motion } from 'framer-motion';
import { SparklesIcon, PaperAirplaneIcon } from '@heroicons/react/24/outline';

const InputSection = ({ sequence, setSequence, onPredict, loading, examples, onLoadExample }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass-card rounded-3xl p-8 mb-8"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-br from-primary-500 to-purple-600">
          <SparklesIcon className="w-5 h-5 text-white" />
        </div>
        <h2 className="text-2xl font-display font-bold text-slate-900">
          Analyze Attack Sequence
        </h2>
      </div>

      {/* Input Area */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Enter Attack Sequence
          </label>
          <textarea
            value={sequence}
            onChange={(e) => setSequence(e.target.value)}
            placeholder="scan, port_scan, login_attempt, brute_force"
            rows={4}
            className="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 outline-none transition-all duration-200 font-mono text-sm resize-none bg-white/50"
          />
          <p className="mt-2 text-xs text-slate-500">
            Separate attacks with commas, arrows (→), or new lines
          </p>
        </div>

        {/* Predict Button */}
        <button
          onClick={onPredict}
          disabled={loading || !sequence.trim()}
          className="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold shadow-lg shadow-primary-500/30 hover:shadow-xl hover:shadow-primary-500/40 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center justify-center gap-2 group"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <PaperAirplaneIcon className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              <span>Predict Next Attack</span>
            </>
          )}
        </button>
      </div>

      {/* Quick Examples */}
      {examples.length > 0 && (
        <div className="mt-8 pt-6 border-t border-slate-200">
          <p className="text-sm font-medium text-slate-700 mb-3">Quick Start Examples</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {examples.map((example, idx) => (
              <button
                key={idx}
                onClick={() => onLoadExample(example)}
                className="text-left p-4 rounded-xl border-2 border-slate-200 hover:border-primary-500 hover:bg-primary-50/50 transition-all duration-200 group"
              >
                <p className="font-medium text-slate-900 text-sm mb-1 group-hover:text-primary-600">
                  {example.name}
                </p>
                <p className="text-xs text-slate-500 font-mono">
                  {example.sequence.join(' → ')}
                </p>
              </button>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default InputSection;
