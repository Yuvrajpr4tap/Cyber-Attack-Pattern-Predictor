import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import InputSection from './components/InputSection';
import ResultsSection from './components/ResultsSection';
import LoadingSkeleton from './components/LoadingSkeleton';
import ErrorAlert from './components/ErrorAlert';

function App() {
  const [sequence, setSequence] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [examples, setExamples] = useState([]);
  const [stats, setStats] = useState({ predictions: '1.2K' });

  const API_URL = 'http://localhost:5000';

  // Fetch examples on mount
  useEffect(() => {
    fetchExamples();
  }, []);

  const fetchExamples = async () => {
    try {
      const response = await fetch(`${API_URL}/example`);
      const data = await response.json();
      if (data.success) {
        setExamples(data.examples);
      }
    } catch (err) {
      console.error('Failed to load examples:', err);
    }
  };

  const handlePredict = useCallback(async () => {
    setError(null);
    setPrediction(null);

    const attacks = sequence
      .split(/[,\n\->→]+/)
      .map(s => s.trim())
      .filter(s => s.length > 0);

    if (attacks.length === 0) {
      setError('Please enter at least one attack step');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sequence: attacks, model: 'ensemble', top_k: 5 })
      });

      const data = await response.json();

      if (data.success) {
        setPrediction(data);
      } else {
        setError(data.error || 'Prediction failed. Please try again.');
      }
    } catch (err) {
      setError('Failed to connect to API. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  }, [sequence, API_URL]);

  const handleLoadExample = useCallback((example) => {
    setSequence(example.sequence.join(', '));
    setPrediction(null);
    setError(null);
  }, []);

  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handlePredict();
    }
  }, [handlePredict]);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyPress);
    return () => document.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-0 w-96 h-96 bg-primary-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse-slow" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse-slow" />
      </div>

      <div className="max-w-7xl mx-auto">
        <Header stats={stats} />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <InputSection
              sequence={sequence}
              setSequence={setSequence}
              onPredict={handlePredict}
              loading={loading}
              examples={examples}
              onLoadExample={handleLoadExample}
            />

            <AnimatePresence>
              {error && <ErrorAlert error={error} onDismiss={() => setError(null)} />}
            </AnimatePresence>

            <AnimatePresence mode="wait">
              {loading ? (
                <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                  <LoadingSkeleton />
                </motion.div>
              ) : prediction ? (
                <motion.div key="results" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                  <ResultsSection prediction={prediction} />
                </motion.div>
              ) : (
                <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-center py-16">
                  <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-slate-100 mb-4">
                    <svg className="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-slate-700 mb-2">Ready to Analyze</h3>
                  <p className="text-sm text-slate-500 max-w-sm mx-auto">
                    Enter an attack sequence or select a quick example to get started.
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div className="space-y-6">
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }} className="glass-card rounded-2xl p-6">
              <h3 className="text-lg font-display font-bold text-slate-900 mb-4">How It Works</h3>
              <div className="space-y-4">
                {[
                  { step: '1', title: 'Enter Sequence', desc: 'Input observed attack patterns' },
                  { step: '2', title: 'AI Analysis', desc: 'LSTM & Markov models process data' },
                  { step: '3', title: 'Get Prediction', desc: 'Receive next attack with confidence' }
                ].map((item, idx) => (
                  <div key={idx} className="flex gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 text-white flex items-center justify-center font-bold text-sm">
                      {item.step}
                    </div>
                    <div>
                      <p className="font-semibold text-slate-900 text-sm">{item.title}</p>
                      <p className="text-xs text-slate-600">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }} className="glass-card rounded-2xl p-6">
              <h3 className="text-lg font-display font-bold text-slate-900 mb-4">Risk Levels</h3>
              <div className="space-y-3">
                {[
                  { color: 'bg-red-500', title: 'High', desc: 'Critical threats requiring immediate action' },
                  { color: 'bg-amber-500', title: 'Medium', desc: 'Active attacks needing attention' },
                  { color: 'bg-emerald-500', title: 'Low', desc: 'Reconnaissance or probing activities' }
                ].map((item, idx) => (
                  <div key={idx} className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${item.color}`} />
                    <div className="flex-1">
                      <p className="font-semibold text-sm text-slate-900">{item.title}</p>
                      <p className="text-xs text-slate-600">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>

        <motion.footer initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }} className="mt-16 text-center text-sm text-slate-500">
          <p>Built with React, TensorFlow & Flask • <span className="text-primary-600 font-semibold">Attack Pattern Predictor</span> v2.0</p>
        </motion.footer>
      </div>
    </div>
  );
}

export default App;
