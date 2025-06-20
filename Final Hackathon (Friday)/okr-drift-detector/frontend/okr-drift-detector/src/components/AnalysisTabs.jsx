// src/components/AnalysisTabs.jsx
import React, { useState } from 'react';
import { 
  TrendingUp, Target, AlertTriangle, MessageSquare
} from 'lucide-react';
import OKRTimeline from './OKRTimeline';
import PillarPerformance from './PillarPerformance';
import DriftAnalysis from './DriftAnalysis';
import CoachingRecommendations from './CoachingRecommendations';

const AnalysisTabs = ({ analysisData }) => {
  const [activeTab, setActiveTab] = useState('trajectory');

  const tabs = [
    { id: 'trajectory', label: 'Trajectory', icon: TrendingUp },
    { id: 'pillars', label: '5-Pillar Analysis', icon: Target },
    { id: 'drift', label: 'Drift Detection', icon: AlertTriangle },
    { id: 'coaching', label: 'AI Coaching', icon: MessageSquare }
  ];

  return (
    <div className="space-y-8">
      {/* Navigation Tabs */}
      <div className="bg-white rounded-xl shadow-sm">
        <nav className="flex space-x-8 px-6 border-b border-gray-200">
          {tabs.map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="space-y-8">
        {activeTab === 'trajectory' && (
          <>
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-indigo-600" />
                Trajectory Summary
              </h3>
              <div className="bg-indigo-50 rounded-lg p-4">
                <p className="text-gray-700">{analysisData.trajectory_summary}</p>
              </div>
            </div>

            <OKRTimeline okrHistory={analysisData.okr_history} />
          </>
        )}

        {activeTab === 'pillars' && (
          <PillarPerformance pillarAnalysis={analysisData.pillar_analysis} />
        )}

        {activeTab === 'drift' && (
          <DriftAnalysis 
            driftReport={analysisData.drift_report} 
            patternClassification={analysisData.pattern_classification} 
          />
        )}

        {activeTab === 'coaching' && (
          <CoachingRecommendations 
            recommendations={analysisData.coaching_recommendations} 
            pattern={analysisData.pattern_classification}
          />
        )}
      </div>
    </div>
  );
};

export default AnalysisTabs;