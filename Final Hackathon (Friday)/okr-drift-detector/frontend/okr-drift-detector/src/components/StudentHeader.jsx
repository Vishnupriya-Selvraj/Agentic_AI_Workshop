// src/components/StudentHeader.jsx
import { User } from 'lucide-react';

const StudentHeader = ({ analysisData, studentName }) => {
  return (
    <div className="student-header">
      <div className="student-info">
        <div className="avatar">
          <User className="avatar-icon" />
        </div>
        <div>
          <h2>{studentName || 'Student'}</h2>
          <p>Student ID: {analysisData?.student_id || 'N/A'}</p>
          <p>Last analyzed: {
            analysisData?.analysis_date || analysisData?.analysis_timestamp 
              ? new Date(analysisData.analysis_date || analysisData.analysis_timestamp).toLocaleString() 
              : 'Never'
          }</p>
        </div>
      </div>
      <div className={`drift-level ${analysisData?.drift_report?.drift_level?.toLowerCase() || 'medium'}`}>
        {analysisData?.drift_report?.drift_level || 'Medium'} Drift
      </div>
    </div>
  );
};

export default StudentHeader;