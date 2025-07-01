import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, RadarChart, PolarGrid, 
  PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import { 
  User, Target, TrendingUp, TrendingDown, AlertTriangle, CheckCircle, 
  BookOpen, Briefcase, Code, Users, Heart, ChevronRight, Calendar,
  MessageSquare, Award, ArrowRight, RefreshCw, Plus,
  Goal, ListChecks, CalendarCheck, Bookmark, Link2, ChevronDown,
  ChevronUp, ClipboardCheck, Star, Zap, Globe, Mail, Clock,
  Search, Loader2, ChevronLeft
} from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

const OKRDriftDetector = () => {
  const [studentId, setStudentId] = useState('');
  const [quarterlyGoal, setQuarterlyGoal] = useState('');
  const [currentLevel, setCurrentLevel] = useState('beginner');
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('trajectory');
  const [expandedMonths, setExpandedMonths] = useState({});
  const [step, setStep] = useState(1); // For multi-step form
  const [apiStatus, setApiStatus] = useState('unknown');
  
  // Constants for UI
  const pillarIcons = {
    CLT: BookOpen,
    CFC: Briefcase,
    SCD: Code,
    IIPC: Users,
    SRI: Heart
  };

  const pillarColors = {
    CLT: '#3B82F6', // Blue
    CFC: '#10B981', // Green  
    SCD: '#F59E0B', // Yellow
    IIPC: '#8B5CF6', // Purple
    SRI: '#EF4444'  // Red
  };

  const driftLevelColors = {
    Low: '#10B981',
    Medium: '#F59E0B', 
    High: '#EF4444'
  };

  const skillLevels = [
    { value: 'beginner', label: 'Beginner' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'advanced', label: 'Advanced' }
  ];

  // Check API health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
          setApiStatus('healthy');
        } else {
          setApiStatus('unhealthy');
        }
      } catch (error) {
        setApiStatus('error');
        console.error('API health check failed:', error);
      }
    };
    checkHealth();
  }, []);

  const toggleExpandMonth = (month) => {
    setExpandedMonths(prev => ({
      ...prev,
      [month]: !prev[month]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_id: parseInt(studentId),
          quarterly_goal: quarterlyGoal,
          current_level: currentLevel
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAnalysisData(data);
      setStep(3); // Move to results view
    } catch (error) {
      console.error('Error analyzing student:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const renderInputForm = () => (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-2xl">
        <div className="flex items-center justify-center mb-6">
          <Target className="w-8 h-8 text-indigo-600 mr-2" />
          <h1 className="text-2xl font-bold text-gray-900">OKR Goal-Drift Analysis</h1>
        </div>
        
        {step === 1 && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Student ID
              </label>
              <input
                type="number"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                placeholder="Enter student ID"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                required
              />
            </div>
            
            <div className="flex justify-end">
              <button
                onClick={() => setStep(2)}
                disabled={!studentId}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next <ChevronRight className="inline ml-1" />
              </button>
            </div>
          </div>
        )}

        {step === 2 && (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Quarterly Goal
              </label>
              <input
                type="text"
                value={quarterlyGoal}
                onChange={(e) => setQuarterlyGoal(e.target.value)}
                placeholder="E.g. Become a GenAI Expert"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Current Skill Level
              </label>
              <select
                value={currentLevel}
                onChange={(e) => setCurrentLevel(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                required
              >
                {skillLevels.map((level) => (
                  <option key={level.value} value={level.value}>
                    {level.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="flex justify-between">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="px-4 py-2 border border-gray-300 rounded-lg flex items-center"
              >
                <ChevronLeft className="w-4 h-4 mr-1" /> Back
              </button>
              <button
                type="submit"
                disabled={loading || !quarterlyGoal}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {loading ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <Search className="w-4 h-4 mr-2" />
                )}
                Analyze
              </button>
            </div>
          </form>
        )}
        
        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-lg">
            Error: {error}
          </div>
        )}
        
        <div className="mt-6 text-center text-sm text-gray-500">
          API Status: 
          <span className={`ml-2 px-2 py-1 rounded-full text-xs ${
            apiStatus === 'healthy' ? 'bg-green-100 text-green-800' :
            apiStatus === 'unhealthy' ? 'bg-yellow-100 text-yellow-800' :
            'bg-red-100 text-red-800'
          }`}>
            {apiStatus}
          </span>
        </div>
      </div>
    </div>
  );

  const renderRoadmap = () => {
    if (!analysisData?.coaching_plan?.quarterly_roadmap) return null;
    
    return (
      <div className="space-y-6">
        {Object.entries(analysisData.coaching_plan.quarterly_roadmap).map(([month, pillars]) => (
          <div key={month} className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
            <div 
              className="flex justify-between items-center cursor-pointer"
              onClick={() => toggleExpandMonth(month)}
            >
              <h4 className="font-semibold text-lg flex items-center">
                <CalendarCheck className="w-5 h-5 mr-2 text-blue-600" />
                {month}
              </h4>
              {expandedMonths[month] ? (
                <ChevronUp className="w-5 h-5 text-gray-500" />
              ) : (
                <ChevronDown className="w-5 h-5 text-gray-500" />
              )}
            </div>
            
            {expandedMonths[month] && (
              <div className="mt-4 space-y-6">
                {Object.entries(pillars).map(([pillar, okrs]) => {
                  const Icon = pillarIcons[pillar];
                  return (
                    <div key={pillar} className="border-l-4 pl-4" style={{ borderColor: pillarColors[pillar] }}>
                      <div className="flex items-center mb-2">
                        <Icon className="w-5 h-5 mr-2" style={{ color: pillarColors[pillar] }} />
                        <h5 className="font-medium">{pillar}</h5>
                      </div>
                      
                      <div className="space-y-4 ml-2">
                        {Object.entries(okrs).map(([okrType, details]) => (
                          <div key={okrType} className="bg-gray-50 p-3 rounded-lg">
                            <h6 className="font-medium text-sm mb-2">{okrType}</h6>
                            
                            {okrType === 'Project' && details.ideas ? (
                              <div className="space-y-2">
                                <h6 className="text-sm font-medium">Project Ideas:</h6>
                                <div className="bg-white p-3 rounded border border-gray-200">
                                  {details.ideas.map((line, i) => (
                                    <p key={i} className="text-sm">{line}</p>
                                  ))}
                                </div>
                                <p className="text-xs text-gray-600 mt-1">
                                  <span className="font-medium">Action:</span> {details.action}
                                </p>
                              </div>
                            ) : (
                              <div className="space-y-3">
                                {details.recommendations && (
                                  <div>
                                    <h6 className="text-xs font-medium uppercase tracking-wider text-gray-500 mb-1">Recommendations</h6>
                                    <ul className="space-y-2">
                                      {details.recommendations.map((rec, i) => (
                                        <li key={i} className="flex items-start">
                                          <Link2 className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0 text-gray-400" />
                                          <div>
                                            <a 
                                              href={rec.url} 
                                              target="_blank" 
                                              rel="noopener noreferrer"
                                              className="text-blue-600 hover:underline text-sm"
                                            >
                                              {rec.title}
                                            </a>
                                            <p className="text-xs text-gray-500">{rec.description}</p>
                                          </div>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                )}
                                
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                  <div>
                                    <h6 className="text-xs font-medium uppercase tracking-wider text-gray-500 mb-1">Action</h6>
                                    <p className="text-sm">{details.action}</p>
                                  </div>
                                  
                                  {details.success_metrics && (
                                    <div>
                                      <h6 className="text-xs font-medium uppercase tracking-wider text-gray-500 mb-1">Success Metrics</h6>
                                      <ul className="list-disc list-inside text-sm space-y-1">
                                        {details.success_metrics.map((metric, i) => (
                                          <li key={i}>{metric}</li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}
                                </div>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderAnalysis = () => {
    if (!analysisData) return null;

    // Data processing for charts
    const pillarData = analysisData.pillar_analysis ? Object.entries(analysisData.pillar_analysis).map(([pillar, data]) => ({
      pillar,
      ...data
    })) : [];

    const getDriftLevel = () => {
      if (!analysisData?.drift_analysis) return 'Medium';
      return analysisData.drift_analysis.drift_level || 'Medium';
    };

    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50">
        {/* Header */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center space-x-3">
                <Target className="w-8 h-8 text-indigo-600" />
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">OKR Goal-Drift Detector</h1>
                  <p className="text-sm text-gray-500">AI-powered OKR trajectory analysis</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="bg-indigo-50 px-3 py-1 rounded-full text-sm font-medium text-indigo-700 flex items-center">
                  <Goal className="w-4 h-4 mr-1" />
                  {analysisData.goal_analysis.quarterly_goal}
                </div>
                <button
                  onClick={() => setStep(1)}
                  className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  <span>New Analysis</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Student Header */}
          <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center">
                  <User className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">{analysisData.student_info.name}</h2>
                  <p className="text-gray-500">Student ID: {analysisData.student_info.id}</p>
                  <p className="text-sm text-gray-400">
                    Current Level: {analysisData.goal_analysis.current_level.charAt(0).toUpperCase() + analysisData.goal_analysis.current_level.slice(1)}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                  getDriftLevel() === 'Low' ? 'bg-green-100 text-green-800' :
                  getDriftLevel() === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {getDriftLevel()} Drift
                </div>
                <div className="px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
                  Readiness: {analysisData.goal_analysis.readiness_score}/100
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="bg-white rounded-xl shadow-sm mb-8">
            <div className="border-b border-gray-200">
              <nav className="flex space-x-8 px-6">
                {[
                  { id: 'trajectory', label: 'Trajectory Analysis', icon: TrendingUp },
                  { id: 'pillars', label: '5-Pillar Performance', icon: Target },
                  { id: 'drift', label: 'Drift Detection', icon: AlertTriangle },
                  { id: 'coaching', label: 'AI Coaching', icon: MessageSquare }
                ].map(tab => {
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
          </div>

          {/* Content based on active tab */}
          {activeTab === 'trajectory' && (
            <div className="space-y-8">
              {/* Trajectory Summary */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-indigo-600" />
                  Trajectory Summary
                </h3>
                <div className="bg-indigo-50 rounded-lg p-4">
                  <p className="text-gray-700">{analysisData.pattern_analysis || 'No trajectory summary available'}</p>
                </div>
              </div>

              {/* Goal Alignment */}
              {analysisData.coaching_plan?.goal_alignment && (
                <div className="bg-white rounded-xl shadow-sm p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Target className="w-5 h-5 mr-2 text-indigo-600" />
                    Goal Alignment
                  </h3>
                  <div className="bg-green-50 rounded-lg p-4">
                    <p className="text-gray-700">{analysisData.coaching_plan.goal_alignment}</p>
                  </div>
                </div>
              )}

              {/* Cross-Pillar Synergies */}
              {analysisData.coaching_plan?.cross_pillar_synergies && (
                <div className="bg-white rounded-xl shadow-sm p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Link2 className="w-5 h-5 mr-2 text-indigo-600" />
                    Cross-Pillar Synergies
                  </h3>
                  <div className="space-y-2">
                    {analysisData.coaching_plan.cross_pillar_synergies.map((synergy, i) => (
                      <div key={i} className="flex items-start">
                        <span className="text-blue-600 mr-2 mt-1">•</span>
                        <span className="text-gray-700">{synergy}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'pillars' && (
            <div className="space-y-8">
              {/* 5-Pillar Overview */}
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                {pillarData.map(({ pillar, score, focus, trend }) => {
                  const Icon = pillarIcons[pillar];
                  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : null;
                  
                  return (
                    <div key={pillar} className="bg-white rounded-xl shadow-sm p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div className={`p-2 rounded-lg`} style={{ backgroundColor: pillarColors[pillar] + '20' }}>
                          <Icon className="w-6 h-6" style={{ color: pillarColors[pillar] }} />
                        </div>
                        {TrendIcon && (
                          <TrendIcon className={`w-4 h-4 ${trend === 'up' ? 'text-green-500' : 'text-red-500'}`} />
                        )}
                      </div>
                      <h4 className="font-semibold text-gray-900 mb-1">{pillar}</h4>
                      <p className="text-sm text-gray-600 mb-3">{focus || 'General'}</p>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Score</span>
                          <span className="font-medium">{score || 0}/100</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${score || 0}%`,
                              backgroundColor: pillarColors[pillar]
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Radar Chart */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">5-Pillar Performance Radar</h3>
                <ResponsiveContainer width="100%" height={400}>
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={pillarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="pillar" />
                    <PolarRadiusAxis angle={18} domain={[0, 100]} />
                    <Radar name="Score" dataKey="score" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeTab === 'drift' && (
            <div className="space-y-8">
              {/* Drift Level Indicator */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                    <AlertTriangle className="w-5 h-5 mr-2 text-yellow-600" />
                    Drift Analysis
                  </h3>
                  <div className={`px-4 py-2 rounded-full text-sm font-medium ${
                    getDriftLevel() === 'Low' ? 'bg-green-100 text-green-800' :
                    getDriftLevel() === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {getDriftLevel()} Risk Level
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-gray-700">{analysisData.drift_analysis?.reasoning || 'No drift analysis reasoning available'}</p>
                </div>
              </div>

              {/* Flagged Transitions */}
              {analysisData.drift_analysis?.flagged_transitions?.length > 0 && (
                <div className="bg-white rounded-xl shadow-sm p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <AlertTriangle className="w-5 h-5 mr-2 text-orange-600" />
                    Flagged Transitions
                  </h3>
                  <div className="space-y-4">
                    {analysisData.drift_analysis.flagged_transitions.map((transition, index) => (
                      <div key={index} className="border border-orange-200 rounded-lg p-4 bg-orange-50">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-sm font-medium text-gray-900">{transition.from}</span>
                          <ArrowRight className="w-4 h-4 text-orange-600" />
                          <span className="text-sm font-medium text-gray-900">{transition.to}</span>
                        </div>
                        <div className="mb-2">
                          <p className="text-sm text-orange-800">{transition.reason}</p>
                        </div>
                        <div className="bg-white p-2 rounded border border-orange-100">
                          <p className="text-xs font-medium text-orange-800">Suggested Action:</p>
                          <p className="text-sm">{transition.suggested_action}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'coaching' && (
            <div className="space-y-8">
              {/* Goal Summary */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Goal className="w-5 h-5 mr-2 text-indigo-600" />
                  Your Learning Goal
                </h3>
                <div className="bg-indigo-50 rounded-lg p-4">
                  <p className="text-gray-700 font-medium">{analysisData.goal_analysis.quarterly_goal}</p>
                  <p className="text-sm text-gray-600 mt-1">
                    Current Level: {analysisData.goal_analysis.current_level.charAt(0).toUpperCase() + analysisData.goal_analysis.current_level.slice(1)}
                  </p>
                </div>
              </div>

              {/* Roadmap */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <CalendarCheck className="w-5 h-5 mr-2 text-indigo-600" />
                  3-Month Roadmap to Achieve Your Goal
                </h3>
                {renderRoadmap()}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <>
      {step < 3 ? renderInputForm() : renderAnalysis()}
    </>
  );
};

export default OKRDriftDetector;