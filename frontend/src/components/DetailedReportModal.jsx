import React, { useState, useEffect } from 'react';
import { stockDataService } from '../services/api';

const DetailedReportModal = ({ keyword, isOpen, onClose }) => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen && keyword) {
      fetchReport();
    }
  }, [isOpen, keyword]);

  const fetchReport = async () => {
    if (!keyword) return;

    try {
      setLoading(true);
      setError(null);
      const response = await stockDataService.generateReport(keyword);
      setReport(response);
    } catch (err) {
      setError('리포트를 생성하는데 실패했습니다.');
      console.error('Failed to generate report:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setReport(null);
    setError(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={handleClose}>&times;</button>

        <h2 className="modal-title">{keyword} 상세 리포트</h2>

        {loading && (
          <div className="loading">
            <p>리포트를 생성하는 중...</p>
          </div>
        )}

        {error && (
          <div className="error">
            <p>{error}</p>
            <button onClick={fetchReport}>다시 시도</button>
          </div>
        )}

        {report && !loading && (
          <div className="report-content">
            <div dangerouslySetInnerHTML={{ __html: report.report.replace(/\n/g, '<br>') }} />

            <div className="report-meta">
              <p><strong>생성 시간:</strong> {new Date(report.generated_at).toLocaleString('ko-KR')}</p>
              <p><strong>키워드:</strong> {report.keyword}</p>
            </div>
          </div>
        )}

        {!loading && !error && !report && (
          <p>리포트 데이터를 불러올 수 없습니다.</p>
        )}
      </div>
    </div>
  );
};

export default DetailedReportModal;