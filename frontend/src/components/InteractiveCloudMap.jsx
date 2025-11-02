import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import cloud from 'd3-cloud';
import { stockDataService } from '../services/api';

const InteractiveCloudMap = ({ onWordClick }) => {
  const svgRef = useRef();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStockData();
  }, []);

  const fetchStockData = async () => {
    try {
      setLoading(true);
      const response = await stockDataService.getStockData();
      setData(response.data || []);
      setError(null);
    } catch (err) {
      setError('데이터를 불러오는데 실패했습니다.');
      console.error('Failed to fetch stock data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!data.length || !svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove(); // Clear previous content

    const width = 800;
    const height = 400;

    svg.attr('width', width).attr('height', height);

    // Prepare data for word cloud
    const words = data.map(item => ({
      text: item.keyword,
      size: Math.max(20, Math.min(100, item.mentions / 10)), // Scale font size
      mentions: item.mentions,
      sentiment: item.sentiment
    }));

    // Color scale based on sentiment
    const colorScale = d3.scaleLinear()
      .domain([-1, 0, 1])
      .range(['#e74c3c', '#f39c12', '#27ae60']);

    // Layout for word cloud
    const layout = cloud()
      .size([width, height])
      .words(words)
      .padding(5)
      .rotate(() => ~~(Math.random() * 2) * 90) // 0 or 90 degrees
      .fontSize(d => d.size)
      .on('end', draw);

    layout.start();

    function draw(words) {
      const g = svg.append('g')
        .attr('transform', `translate(${width / 2},${height / 2})`);

      g.selectAll('text')
        .data(words)
        .enter().append('text')
        .style('font-size', d => `${d.size}px`)
        .style('font-family', 'Impact')
        .style('fill', d => colorScale(d.sentiment))
        .attr('text-anchor', 'middle')
        .attr('transform', d => `translate(${d.x},${d.y}) rotate(${d.rotate})`)
        .text(d => d.text)
        .style('cursor', 'pointer')
        .on('click', (event, d) => {
          if (onWordClick) {
            onWordClick(d.text);
          }
        })
        .on('mouseover', function(event, d) {
          d3.select(this)
            .transition()
            .duration(200)
            .style('opacity', 0.7)
            .style('font-size', `${d.size * 1.2}px`);
        })
        .on('mouseout', function(event, d) {
          d3.select(this)
            .transition()
            .duration(200)
            .style('opacity', 1)
            .style('font-size', `${d.size}px`);
        })
        .append('title') // Tooltip
        .text(d => `${d.text}: ${d.mentions} mentions, Sentiment: ${d.sentiment.toFixed(2)}`);
    }
  }, [data, onWordClick]);

  if (loading) {
    return (
      <div className="loading">
        <h3>데이터를 불러오는 중...</h3>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <h3>오류</h3>
        <p>{error}</p>
        <button onClick={fetchStockData}>다시 시도</button>
      </div>
    );
  }

  return (
    <div className="cloud-container">
      <h2>실시간 주식 키워드 클라우드</h2>
      <p>단어를 클릭하여 상세 리포트를 확인하세요.</p>
      <svg ref={svgRef}></svg>
      {data.length === 0 && !loading && (
        <p>표시할 데이터가 없습니다.</p>
      )}
    </div>
  );
};

export default InteractiveCloudMap;