import { 
  TrendingUp, TrendingDown 
} from 'lucide-react'
import { 
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar 
} from 'recharts'
import { ResponsiveContainer } from 'recharts';

const PillarPerformance = ({ analysisData, pillarIcons, pillarColors }) => {
  const pillarData = analysisData.pillar_analysis ? 
    Object.entries(analysisData.pillar_analysis).map(([pillar, data]) => ({
      pillar,
      ...data
    })) : []

  return (
    <div className="tab-content">
      {/* 5-Pillar Overview */}
      <div className="card">
        <div className="pillar-grid">
          {pillarData.map((pillar) => {
            const Icon = pillarIcons[pillar.pillar]
            const TrendIcon = pillar.trend === 'up' ? TrendingUp : 
                            pillar.trend === 'down' ? TrendingDown : null
            
            return (
              <div key={pillar.pillar} className="pillar-card">
                <div className="pillar-header">
                  <div className="pillar-icon-container">
                    <Icon className="pillar-icon" />
                  </div>
                  {TrendIcon && (
                    <TrendIcon className={`trend-icon ${pillar.trend}`} />
                  )}
                </div>
                <h4 className="pillar-name">{pillar.pillar}</h4>
                <p className="pillar-focus">{pillar.focus}</p>
                <div className="pillar-metrics">
                  <div className="metric-row">
                    <span>Score</span>
                    <span className="metric-value">{pillar.score}/100</span>
                  </div>
                  <div className="score-bar">
                    <div 
                      className="score-progress" 
                      style={{ 
                        width: `${pillar.score}%`,
                        backgroundColor: pillarColors[pillar.pillar]
                      }}
                    />
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Radar Chart */}
      <div className="card">
        <div className="card-header">
          <span>5-Pillar Performance Radar</span>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height={400}>
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={pillarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="pillar" />
              <PolarRadiusAxis angle={18} domain={[0, 100]} />
              <Radar 
                name="Score" 
                dataKey="score" 
                stroke="#3B82F6" 
                fill="#3B82F6" 
                fillOpacity={0.3} 
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Pillar Analysis */}
      <div className="card">
        <div className="card-header">
          <span>Pillar Breakdown</span>
        </div>
        <div className="pillar-breakdown">
          <div className="breakdown-column">
            <h4>Strong Pillars</h4>
            {pillarData
              .filter(pillar => pillar.score >= 70)
              .map(pillar => {
                const Icon = pillarIcons[pillar.pillar]
                return (
                  <div key={pillar.pillar} className="pillar-strength strong">
                    <Icon className="strength-icon" />
                    <span className="pillar-label">{pillar.pillar}</span>
                    <span className="pillar-score">({pillar.score}/100)</span>
                  </div>
                )
              })}
          </div>
          <div className="breakdown-column">
            <h4>Areas for Improvement</h4>
            {pillarData
              .filter(pillar => pillar.score < 70)
              .map(pillar => {
                const Icon = pillarIcons[pillar.pillar]
                return (
                  <div key={pillar.pillar} className="pillar-strength weak">
                    <Icon className="strength-icon" />
                    <span className="pillar-label">{pillar.pillar}</span>
                    <span className="pillar-score">({pillar.score}/100)</span>
                  </div>
                )
              })}
          </div>
        </div>
      </div>
    </div>
  )
}

export default PillarPerformance