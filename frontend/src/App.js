import React, { useState } from 'react';
import './App.css';
import InteractiveCloudMap from './components/InteractiveCloudMap';
import DetailedReportModal from './components/DetailedReportModal';

function App() {
  const [selectedKeyword, setSelectedKeyword] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleWordClick = (keyword) => {
    setSelectedKeyword(keyword);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedKeyword(null);
  };

  return (
    <div className="app">
      <header className="header">
        <h1 className="title">Reddit Stock Monitor</h1>
        <p className="subtitle">
          레딧에서 최근 많이 언급되는 주식 키워드를 실시간으로 수집하고 시각화하는 서비스
        </p>
      </header>

      <main>
        <InteractiveCloudMap onWordClick={handleWordClick} />

        <DetailedReportModal
          keyword={selectedKeyword}
          isOpen={isModalOpen}
          onClose={handleCloseModal}
        />
      </main>

      <footer style={{ textAlign: 'center', marginTop: '40px', color: '#7f8c8d', fontSize: '0.9rem' }}>
        <p>데이터는 실시간으로 업데이트됩니다. 마지막 업데이트: {new Date().toLocaleString('ko-KR')}</p>
      </footer>
    </div>
  );
}

export default App;