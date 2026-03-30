import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldExclamationIcon, 
  ExclamationTriangleIcon, 
  MagnifyingGlassIcon,
  ChartBarIcon,
  ArrowRightIcon
} from '@heroicons/react/24/solid';

const getRiskConfig = (risk) => {
  const configs = {
    HIGH: {
      color: 'danger',
      icon: ShieldExclamationIcon,
      gradient: 'from-red-500 to-rose-600',
      bg: 'bg-red-50',
      border: 'border-red-200',
      text: 'text-red-700'
    },
    MEDIUM: {
      color: 'warning',
      icon: ExclamationTriangleIcon,
      gradient: 'from-amber-500 to-orange-600',
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      text: 'text-amber-700'
    },
    LOW: {
      color: 'success',
      icon: MagnifyingGlassIcon,
      gradient: 'from-emerald-500 to-green-600',
      bg: 'bg-emerald-50',
      border: 'border-emerald-200',
      text: 'text-emerald-700'
    }
  };
  return configs[risk] || configs.MEDIUM;
};

const AttackFlow = ({ sequence, predicted }) => (
  <div className="flex items-center justify-center flex-wrap gap-2 mb-8">
    {sequence.map((attack, idx) => (
      <React.Fragment key={idx}>
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: idx * 0.1 }}
          className="px-4 py-2 rounded-lg bg-slate-100 border border-slate-200 font-mono text-sm text-slate-700"
        >
          {attack}
        </motion.div>
        {idx < sequence.length - 1 && (
          <ArrowRightIcon className="w-4 h-4 text-slate-400" />
        )}
      </React.Fragment>
    ))}
    <ArrowRightIcon className="w-4 h-4 text-primary-500 animate-pulse" />
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: sequence.length * 0.1 }}
      className="px-4 py-2 rounded-lg bg-gradient-to-r from-primary-500 to-purple-600 text-white font-mono text-sm font-semibold shadow-lg"
    >
      {predicted}
    </motion.div>
  </div>
);

const PredictionCard = ({ prediction, title }) => {
  const config = getRiskConfig(prediction.risk_level);
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`glass-card rounded-2xl p-6 border-2 ${config.border}`}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-xl bg-gradient-to-br ${config.gradient} text-white`}>
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-600">{title}</p>
            <p className="text-2xl font-bold text-slate-900 font-mono">
              {prediction.attack}
            </p>
          </div>
        </div>
        <div className={`px-4 py-2 rounded-full ${config.bg} ${config.text} font-bold text-sm`}>
          {prediction.risk_level}
        </div>
      </div>

      {/* Confidence Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-slate-600">Confidence</span>
          <span className="text-sm font-bold text-slate-900">
            {(prediction.confidence * 100).toFixed(1)}%
          </span>
        </div>
        <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${prediction.confidence * 100}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
            className={`h-full bg-gradient-to-r ${config.gradient} rounded-full`}
          />
        </div>
      </div>

      {/* Risk Description */}
      <div className={`p-4 rounded-xl ${config.bg} border ${config.border}`}>
        <p className={`text-sm ${config.text} font-medium`}>
          {prediction.description}
        </p>
      </div>
    </motion.div>
  );
};

const TopPredictions = ({ predictions }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass-card rounded-2xl p-6"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-br from-primary-500 to-purple-600">
          <ChartBarIcon className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-xl font-display font-bold text-slate-900">
          Top Predictions
        </h3>
      </div>

      <div className="space-y-3">
        {predictions.map((pred, idx) => {
          const config = getRiskConfig(pred.risk_level);
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="flex items-center gap-4 p-4 rounded-xl hover:bg-slate-50 transition-colors duration-200"
            >
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-primary-600 text-white flex items-center justify-center font-bold text-sm">
                {idx + 1}
              </div>
              
              <div className="flex-1">
                <p className="font-mono text-sm font-semibold text-slate-900 mb-1">
                  {pred.attack}
                </p>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      style={{ width: `${pred.confidence * 100}%` }}
                      className={`h-full bg-gradient-to-r ${config.gradient} rounded-full`}
                    />
                  </div>
                  <span className="text-xs font-bold text-slate-600 w-12 text-right">
                    {(pred.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              <div className={`px-3 py-1 rounded-full ${config.bg} ${config.text} text-xs font-bold`}>
                {pred.risk_level}
              </div>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
};

const ResultsSection = ({ prediction }) => {
  if (!prediction) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="space-y-6"
      >
        {/* Attack Flow */}
        <AttackFlow
          sequence={prediction.input_sequence}
          predicted={prediction.predicted_attack}
        />

        {/* Main Prediction */}
        <PredictionCard
          prediction={{
            attack: prediction.predicted_attack,
            confidence: prediction.confidence,
            risk_level: prediction.risk_level,
            description: prediction.risk_description
          }}
          title="Next Predicted Attack"
        />

        {/* Top Predictions */}
        {prediction.top_predictions && (
          <TopPredictions predictions={prediction.top_predictions.slice(0, 5)} />
        )}

        {/* Metadata */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="flex items-center justify-center gap-6 text-sm text-slate-600"
        >
          <div className="flex items-center gap-2">
            <span className="font-medium">Model:</span>
            <span className="font-mono text-primary-600">{prediction.model_used}</span>
          </div>
          <div className="w-px h-4 bg-slate-300" />
          <div className="flex items-center gap-2">
            <span className="font-medium">Sequence Length:</span>
            <span className="font-mono text-primary-600">{prediction.sequence_length}</span>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default ResultsSection;
