import { Lightbulb, CheckCircle, Award } from 'lucide-react'

const CoachingRecommendations = ({ analysisData }) => {
  return (
    <div className="tab-content">
      {/* AI Coaching Recommendations */}
      <div className="card">
        <div className="card-header">
          <Lightbulb className="icon" />
          <span>AI-Powered Coaching Recommendations</span>
        </div>
        <div className="recommendation-list">
          {analysisData.coaching_recommendations?.map((recommendation, index) => (
            <div key={index} className="recommendation-item">
              <div className="recommendation-number">{index + 1}</div>
              <p>{recommendation}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Action Plan */}
      <div className="card">
        <div className="card-header">
          <CheckCircle className="icon" />
          <span>Suggested Action Plan</span>
        </div>
        <div className="action-plan">
          <div className="action-item immediate">
            <div className="action-bullet"></div>
            <span className="action-timeframe">Immediate (This Week)</span>
            <span className="action-description">Create LinkedIn article about GenAI journey</span>
          </div>
          <div className="action-item short-term">
            <div className="action-bullet"></div>
            <span className="action-timeframe">Short-term (This Month)</span>
            <span className="action-description">Find AI-focused hackathon to participate</span>
          </div>
          <div className="action-item long-term">
            <div className="action-bullet"></div>
            <span className="action-timeframe">Long-term (Next Quarter)</span>
            <span className="action-description">Integrate AI skills across all OKR pillars</span>
          </div>
        </div>
      </div>

      {/* Progress Tracking */}
      <div className="card">
        <div className="card-header">
          <Award className="icon" />
          <span>Track Your Progress</span>
        </div>
        <div className="progress-grid">
          <div className="progress-item">
            <div className="progress-count">3</div>
            <p>Recommendations</p>
            <p>Completed</p>
          </div>
          <div className="progress-item">
            <div className="progress-count">2</div>
            <p>Recommendations</p>
            <p>In Progress</p>
          </div>
          <div className="progress-item">
            <div className="progress-count">0</div>
            <p>Recommendations</p>
            <p>Not Started</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CoachingRecommendations