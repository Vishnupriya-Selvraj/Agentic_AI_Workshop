// src/components/LoadingSpinner.jsx
import React from 'react';
import { RefreshCw } from 'lucide-react';

const LoadingSpinner = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex items-center justify-center">
      <div className="text-center">
        <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-indigo-600" />
        <p className="text-gray-600">Loading analysis...</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;