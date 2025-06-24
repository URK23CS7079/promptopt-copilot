import React from 'react';
import styles from './HistoryGraph.module.css';

export default function HistoryGraph() {
  const mockData = [
    { version: 'v1', accuracy: 65 },
    { version: 'v2', accuracy: 78 },
    { version: 'v3', accuracy: 82 }
  ];

  return (
    <div className={styles.container}>
      <h2>Optimization History</h2>
      <div className={styles.graph}>
        {mockData.map((item, index) => (
          <div key={index} className={styles.barContainer}>
            <div 
              className={styles.bar} 
              style={{ height: `${item.accuracy}%` }}
              title={`Accuracy: ${item.accuracy}%`}
            ></div>
            <span className={styles.label}>{item.version}</span>
          </div>
        ))}
      </div>
    </div>
  );
}