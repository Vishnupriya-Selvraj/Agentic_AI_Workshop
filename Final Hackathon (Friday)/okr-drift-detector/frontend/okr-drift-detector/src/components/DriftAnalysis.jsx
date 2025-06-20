import { AlertTriangle, Target, ArrowRight } from 'lucide-react'

const DriftAnalysis = ({ analysisData }) => {
  const riskLevel = analysisData.drift_report.drift_level.toLowerCase()

  const riskColors = {
    low: 'from-emerald-400 to-emerald-600 text-white',
    medium: 'from-amber-400 to-amber-600 text-white',
    high: 'from-rose-500 to-rose-700 text-white'
  }

  return (
    <div className="tab-content space-y-8 px-4 py-6">
      
      {/* Drift Level Indicator */}
      <div className="bg-gradient-to-br from-white to-gray-50 rounded-3xl shadow-2xl border border-gray-200 p-6 transition-transform hover:scale-[1.01] duration-300">
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-3 text-xl font-semibold text-gray-900">
            <AlertTriangle className="w-6 h-6 text-yellow-600 animate-pulse" />
            <span>Drift Analysis</span>
          </div>
          <div
            className={`px-4 py-1 rounded-full text-sm font-medium bg-gradient-to-r ${riskColors[riskLevel]} shadow-md transition-all`}
          >
            {analysisData.drift_report.drift_level} Risk Level
          </div>
        </div>
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-lg text-gray-800 text-sm leading-relaxed shadow-inner">
          {analysisData.drift_report.reasoning}
        </div>
      </div>

      {/* Flagged Transitions */}
      {analysisData.drift_report.flagged_transitions?.length > 0 && (
        <div className="bg-gradient-to-br from-white to-slate-50 rounded-3xl shadow-2xl border border-gray-200 p-6 transition-transform hover:scale-[1.01] duration-300">
          <div className="flex items-center gap-3 mb-5 text-xl font-semibold text-gray-900">
            <AlertTriangle className="w-6 h-6 text-orange-500" />
            <span>Flagged Transitions</span>
          </div>
          <div className="space-y-4">
            {analysisData.drift_report.flagged_transitions.map((transition, index) => (
              <div
                key={index}
                className="bg-gradient-to-r from-slate-100 to-slate-200 rounded-xl p-4 border border-gray-300 hover:shadow-lg hover:scale-[1.01] transition-all duration-300"
              >
                <div className="flex items-center gap-2 font-semibold text-gray-900">
                  <span>{transition.from}</span>
                  <ArrowRight className="w-4 h-4 text-gray-600" />
                  <span>{transition.to}</span>
                </div>
                <p className="mt-2 text-sm text-gray-700 italic">
                  {transition.reason}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pattern Classification */}
      <div className="bg-gradient-to-br from-white via-blue-50 to-white rounded-3xl shadow-2xl border border-blue-100 p-6 transition-transform hover:scale-[1.01] duration-300">
        <div className="flex items-center gap-3 mb-4 text-xl font-semibold text-gray-900">
          <Target className="w-6 h-6 text-sky-600" />
          <span>Behavioral Pattern</span>
        </div>
        <div className="bg-blue-50 border-l-4 border-sky-300 p-4 rounded-lg text-sm text-gray-800 leading-relaxed shadow-inner">
          {analysisData.pattern_classification}
        </div>
      </div>
    </div>
  )
}

export default DriftAnalysis
