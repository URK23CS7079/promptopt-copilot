import { useState } from 'react'
import styles from './PromptEditor.module.css'

export default function PromptEditor({
  prompt,
  onPromptChange,
  onGenerate,
  models,
  selectedModel,
  onModelChange,
  isLoading
}) {
  const [testData, setTestData] = useState(null)

  const handleFileUpload = (e) => {
    setTestData(e.target.files[0])
  }

  return (
    <div className={styles.editorContainer}>
      <div className={styles.modelSelector}>
        <label htmlFor="model-select">Select Model:</label>
        <select
          id="model-select"
          value={selectedModel}
          onChange={(e) => onModelChange(e.target.value)}
          disabled={isLoading}
        >
          {models.map(model => (
            <option key={model.name} value={model.name}>
              {model.name} ({model.size}, needs {model.ram_required} RAM)
            </option>
          ))}
        </select>
      </div>

      <textarea
        className={styles.promptInput}
        value={prompt}
        onChange={(e) => onPromptChange(e.target.value)}
        placeholder="Enter your base prompt here..."
        disabled={isLoading}
      />

      <div className={styles.testDataUpload}>
        <label htmlFor="test-data-upload">Upload Test Data (CSV/JSON):</label>
        <input
          id="test-data-upload"
          type="file"
          accept=".csv,.json"
          onChange={handleFileUpload}
          disabled={isLoading}
        />
      </div>

      <button
        className={styles.generateButton}
        onClick={onGenerate}
        disabled={!prompt || isLoading}
      >
        {isLoading ? 'Generating...' : 'Generate Variants'}
      </button>

      <div className={styles.tipsSection}>
        <h3>Prompt Engineering Tips</h3>
        <ul>
          <li>Be specific about the desired output format</li>
          <li>Include examples when possible</li>
          <li>Use clear instructions with step-by-step guidance</li>
          <li>Specify constraints or limitations</li>
        </ul>
      </div>
    </div>
  )
}