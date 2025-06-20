// src/pages/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { analyzeStudentOKRs, getStudentReports, getStudentProfile } from '../utils/api';
import StudentHeader from '../components/StudentHeader';
import AnalysisTabs from '../components/AnalysisTabs';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const { studentId = 'student_123' } = useParams();
  const [analysisData, setAnalysisData] = useState(null);
  const [studentProfile, setStudentProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [profile, analysis] = await Promise.all([
        getStudentProfile(studentId),
        analyzeStudentOKRs(studentId)
      ]);
      setStudentProfile(profile);
      setAnalysisData(analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [studentId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorDisplay message={error} />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {studentProfile && (
          <StudentHeader 
            profile={studentProfile} 
            onRefresh={fetchData}
            loading={loading}
          />
        )}
        
        {analysisData && (
          <AnalysisTabs analysisData={analysisData} />
        )}
      </div>
    </div>
  );
};

const ErrorDisplay = ({ message }) => (
  <div className="min-h-screen flex items-center justify-center">
    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      <strong>Error:</strong> {message}
      <button 
        onClick={() => window.location.reload()}
        className="ml-4 bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded"
      >
        Retry
      </button>
    </div>
  </div>
);

export default Dashboard;