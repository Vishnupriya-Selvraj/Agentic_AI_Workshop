const API_BASE_URL = 'http://localhost:8000';

export const checkAPIHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('API health check failed');
    }
    return await response.json();
  } catch (error) {
    console.error('API Health Check Error:', error);
    return { status: 'unhealthy', error: error.message };
  }
};

export const analyzeStudentOKRs = async (studentId, quarterlyGoal, currentLevel) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        student_id: parseInt(studentId),
        quarterly_goal: quarterlyGoal,
        current_level: currentLevel
      })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to analyze OKRs: ${response.statusText}`);
    }
    
    const data = await response.json();
    return transformAnalysisData(data);
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getStudentReports = async (studentId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/reports/${parseInt(studentId)}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch reports: ${response.statusText}`);
    }
    
    const data = await response.json();
    if (!data || (Array.isArray(data) && data.length === 0)) {
      throw new Error('No reports found');
    }
    return Array.isArray(data) ? data.map(transformAnalysisData) : [transformAnalysisData(data)];
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getStudentProfile = async (studentId) => {
  try {
    const reports = await getStudentReports(studentId);
    const latestReport = reports[0];
    
    return {
      student_id: studentId,
      name: latestReport.student_info?.name || `Student ${studentId}`,
      register_number: latestReport.student_info?.register_number || '',
      email: `student${studentId}@institution.edu`,
      department: 'Computer Science',
      institution: 'SNS Institution of Technology'
    };
  } catch (error) {
    console.error('Failed to fetch student profile:', error);
    throw error;
  }
};

const transformAnalysisData = (backendData) => {
  if (!backendData) return null;
  
  // Handle MongoDB date format
  const analysisDate = backendData.analysis_date?.$date 
    ? new Date(backendData.analysis_date.$date) 
    : new Date(backendData.analysis_date || new Date());

  return {
    student_info: {
      id: backendData.student_info?.id || backendData.student_id,
      name: backendData.student_info?.name || `Student ${backendData.student_id}`,
      register_number: backendData.student_info?.register_number || ''
    },
    goal_analysis: {
      quarterly_goal: backendData.goal_analysis?.quarterly_goal || 'Not specified',
      current_level: backendData.goal_analysis?.current_level || 'beginner',
      readiness_score: backendData.goal_analysis?.readiness_score || 0
    },
    drift_analysis: {
      drift_level: backendData.drift_analysis?.drift_level || 'Medium',
      reasoning: backendData.drift_analysis?.reasoning || 'No drift analysis available',
      flagged_transitions: backendData.drift_analysis?.flagged_transitions || []
    },
    pattern_analysis: backendData.pattern_analysis || backendData.pattern_classification || 'No pattern analysis available',
    coaching_plan: backendData.coaching_plan || {
      quarterly_roadmap: {},
      goal_alignment: 'No coaching plan generated',
      cross_pillar_synergies: []
    },
    pillar_analysis: backendData.pillar_analysis || {
      CLT: { score: 0, focus: '', completion: 0, trend: 'stable' },
      CFC: { score: 0, focus: '', completion: 0, trend: 'stable' },
      SCD: { score: 0, focus: '', completion: 0, trend: 'stable' },
      IIPC: { score: 0, focus: '', completion: 0, trend: 'stable' },
      SRI: { score: 0, focus: '', completion: 0, trend: 'stable' }
    },
    analysis_date: analysisDate.toISOString(),
    _id: backendData._id?.$oid || backendData._id
  };
};

export default {
  checkAPIHealth,
  analyzeStudentOKRs,
  getStudentReports,
  getStudentProfile
};