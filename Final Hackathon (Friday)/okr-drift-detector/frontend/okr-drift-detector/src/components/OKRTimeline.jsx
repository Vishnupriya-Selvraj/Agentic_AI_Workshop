// src/components/OKRTimeline.jsx
import React from 'react';
import { Calendar } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const OKRTimeline = ({ okrHistory }) => {
  const pillarIcons = {
    CLT: '📚',
    CFC: '💼',
    SCD: '💻',
    IIPC: '🤝',
    SRI: '❤️'
  };

  const pillarColors = {
    CLT: '#3B82F6',
    CFC: '#10B981',
    SCD: '#F59E0B',
    IIPC: '#8B5CF6',
    SRI: '#EF4444'
  };

  const chartData = okrHistory.map(okr => ({
    cycle: okr.cycle,
    completion: okr.completion_status * 100,
    pillar: okr.pillar
  }));

  return (
    <div className="space-y-8">
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Calendar className="w-5 h-5 mr-2 text-indigo-600" />
          OKR Timeline
        </h3>
        <div className="space-y-4">
          {okrHistory.map((okr, index) => (
            <div key={index} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl">{pillarIcons[okr.pillar]}</div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-900">{okr.cycle}</span>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    okr.completion_status >= 0.8 ? 'bg-green-100 text-green-800' : 
                    okr.completion_status >= 0.5 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {okr.completion_status >= 0.8 ? 'Completed' : okr.completion_status >= 0.5 ? 'In Progress' : 'Needs Attention'}
                  </span>
                </div>
                <p className="text-gray-700 mb-2">{okr.objective}</p>
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="h-2 rounded-full transition-all duration-300"
                      style={{ 
                        width: `${okr.completion_status * 100}%`,
                        backgroundColor: pillarColors[okr.pillar]
                      }}
                    />
                  </div>
                  <span className="text-sm font-medium text-gray-600">{Math.round(okr.completion_status * 100)}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="cycle" />
            <YAxis domain={[0, 100]} />
            <Tooltip 
              formatter={(value) => [`${value}%`, "Completion"]}
              labelFormatter={(label) => `Cycle: ${label}`}
            />
            <Line 
              type="monotone" 
              dataKey="completion" 
              stroke="#3B82F6" 
              strokeWidth={2}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default OKRTimeline;