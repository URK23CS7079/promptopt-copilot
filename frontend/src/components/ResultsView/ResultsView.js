import styles from './ResultsView.module.css'

export default function ResultsView({ results, basePrompt }) {
  return (
    <div className={styles.container}>
      <h2>Evaluation Results</h2>
      
      <div className={styles.resultsGrid}>
        <div className={styles.metricsSection}>
          <h3>Performance Metrics</h3>
          <table className={styles.metricsTable}>
            <thead>
              <tr>
                <th>Variant</th>
                <th>Exact Match</th>
                <th>Latency</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result, index) => (
                <tr key={index}>
                  <td>Variant {index + 1}</td>
                  <td>{(result.metrics.exact_match * 100).toFixed(1)}%</td>
                  <td>{result.metrics.latency || 'N/A'}s</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className={styles.recommendationSection}>
          <h3>Optimization Recommendation</h3>
          <div className={styles.recommendationCard}>
            <h4>Best Performing Variant</h4>
            <p>Variant 3 (82% accuracy)</p>
            
            <h4>Suggested Improvements</h4>
            <ul>
              <li>Add more specific output requirements</li>
              <li>Include an example in the prompt</li>
              <li>Break down into step-by-step instructions</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}