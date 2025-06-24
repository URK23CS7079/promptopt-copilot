import { useState } from 'react'
import styles from './VariantTable.module.css'

export default function VariantTable({ variants, onEvaluate, isLoading }) {
  const [testData, setTestData] = useState(null)

  const handleFileUpload = (e) => {
    setTestData(e.target.files[0])
  }

  const handleEvaluate = () => {
    if (!testData) {
      alert('Please upload test data first')
      return
    }
    onEvaluate(testData)
  }

  return (
    <div className={styles.container}>
      <h2>Generated Variants</h2>
      
      <div className={styles.uploadSection}>
        <label htmlFor="test-data">Upload Test Data (CSV/JSON):</label>
        <input
          id="test-data"
          type="file"
          accept=".csv,.json"
          onChange={handleFileUpload}
          disabled={isLoading}
        />
      </div>

      <div className={styles.tableWrapper}>
        <table className={styles.variantTable}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Variant</th>
              <th>Technique</th>
            </tr>
          </thead>
          <tbody>
            {variants.map((variant) => (
              <tr key={variant.id}>
                <td>{variant.id}</td>
                <td className={styles.promptCell}>{variant.content}</td>
                <td>{variant.parameters?.technique || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <button
        className={styles.evaluateButton}
        onClick={handleEvaluate}
        disabled={!testData || isLoading}
      >
        {isLoading ? 'Evaluating...' : 'Evaluate Variants'}
      </button>
    </div>
  )
}