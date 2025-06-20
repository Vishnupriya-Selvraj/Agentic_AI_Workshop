const API_BASE_URL = 'http://localhost:8000';

export const checkAPIHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`API health check failed with status ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('API health check failed:', error);
    throw error;
  }
};

export const analyzeStudentOKRs = async (studentId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: studentId })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to analyze OKRs: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // Transform data to match frontend structure
    return transformAnalysisData(data);
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getStudentReports = async (studentId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/reports/${studentId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch reports: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // If we have multiple reports, get the latest one
    const latestReport = Array.isArray(data) ? data[0] : data;
    
    return transformAnalysisData(latestReport);
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getStudentProfile = async (studentId) => {
  try {
    // In a real implementation, this would call a /profile endpoint
    // For now, we'll use mock data that matches the backend model
    return {
      student_id: studentId,
      name: 'Demo Student',
      email: 'demo.student@example.com',
      program: 'Computer Science',
      year: 2024
    };
  } catch (error) {
    console.error('Failed to fetch student profile:', error);
    throw error;
  }
};

// Helper function to transform backend data to frontend format
const transformAnalysisData = (backendData) => {
  if (!backendData) return null;
  
  // Map backend data to frontend structure
  return {
    student_id: backendData.student_id,
    student_name: backendData.student_id, // Will be replaced by actual name from profile
    trajectory_summary: backendData.trajectory_summary,
    drift_report: {
      drift_level: backendData.drift_level,
      flagged_transitions: backendData.flagged_transitions || [],
      reasoning: backendData.reasoning || ''
    },
    pattern_classification: backendData.pattern_classification,
    coaching_recommendations: backendData.coaching_recommendations || [],
    pillar_analysis: backendData.pillar_analysis || {
      CLT: { score: 0, focus: '', completion: 0, trend: 'stable' },
      CFC: { score: 0, focus: '', completion: 0, trend: 'stable' },
      SCD: { score: 0, focus: '', completion: 0, trend: 'stable' },
      IIPC: { score: 0, focus: '', completion: 0, trend: 'stable' },
      SRI: { score: 0, focus: '', completion: 0, trend: 'stable' }
    },
    okr_history: backendData.okr_history || [],
    analysis_timestamp: backendData.analysis_date || new Date().toISOString()
  };
};