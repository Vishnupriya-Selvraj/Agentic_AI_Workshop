import { Calendar, TrendingUp } from 'lucide-react'
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts'

const TrajectoryAnalysis = ({ analysisData, pillarIcons, pillarColors }) => {
  const trajectoryData = analysisData.okr_history?.map((okr, index) => ({
    cycle: okr.cycle,
    completion: okr.completion || okr.completion_status * 100,
    pillar: okr.pillar
  })) || []

  return (
    <div className="tab-content">
      {/* Trajectory Summary */}
      <div className="card">
        <h3 className="card-header">
          <TrendingUp className="icon" />
          Trajectory Summary
        </h3>
        <div className="highlight-box">
          <p>{analysisData.trajectory_summary}</p>
        </div>
      </div>

      {/* OKR Timeline */}
      <div className="card">
        <h3 className="card-header">
          <Calendar className="icon" />
          OKR Timeline
        </h3>
        <div className="timeline">
          {analysisData.okr_history?.map((okr, index) => {
            const Icon = pillarIcons[okr.pillar]
            const completion = okr.completion || okr.completion_status * 100
            
            return (
              <div key={index} className="timeline-item">
                <div className="pillar-icon" style={{ backgroundColor: `${pillarColors[okr.pillar]}20` }}>
                  <Icon style={{ color: pillarColors[okr.pillar] }} />
                </div>
                <div className="timeline-content">
                  <div className="timeline-header">
                    <span>{okr.cycle}</span>
                    <span className={`status ${okr.status === 'completed' || completion >= 90 ? 'completed' : 'in-progress'}`}>
                      {okr.status || (completion >= 90 ? 'completed' : 'in-progress')}
                    </span>
                  </div>
                  <p className="objective">{okr.objective}</p>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ 
                        width: `${completion}%`,
                        backgroundColor: pillarColors[okr.pillar]
                      }}
                    />
                    <span>{Math.round(completion)}%</span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Progress Chart */}
      <div className="card">
        <h3>Progress Over Time</h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trajectoryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="cycle" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
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
    </div>
  )
}

export default TrajectoryAnalysis