import { useState, useEffect } from 'react'
import PromptEditor from '../components/PromptEditor/PromptEditor'
import VariantTable from '../components/VariantTable/VariantTable'
import ResultsView from '../components/ResultsView/ResultsView'
import HistoryGraph from '../components/HistoryGraph/HistoryGraph'
import { fetchModels, generateVariants, evaluatePrompts } from '../utils/api'
import styles from '../styles/Home.module.css'

export default function Home() {
  const [activeTab, setActiveTab] = useState('draft')
  const [basePrompt, setBasePrompt] = useState('')
  const [variants, setVariants] = useState([])
  const [results, setResults] = useState([])
  const [models, setModels] = useState([])
  const [selectedModel, setSelectedModel] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    async function loadModels() {
      const availableModels = await fetchModels()
      setModels(availableModels)
      if (availableModels.length > 0) {
        setSelectedModel(availableModels[0].name)
      }
    }
    loadModels()
  }, [])

  const handleGenerateVariants = async () => {
    setIsLoading(true)
    try {
      const generatedVariants = await generateVariants(basePrompt, 5)
      setVariants(generatedVariants)
      setActiveTab('variants')
    } catch (error) {
      console.error('Error generating variants:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleEvaluate = async (testData) => {
    setIsLoading(true)
    try {
      const evaluationResults = await evaluatePrompts(variants, testData)
      setResults(evaluationResults)
      setActiveTab('results')
    } catch (error) {
      console.error('Error evaluating prompts:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>PromptOpt Co-Pilot</h1>
        <nav className={styles.navTabs}>
          {['draft', 'variants', 'results', 'history'].map(tab => (
            <button
              key={tab}
              className={`${styles.tab} ${activeTab === tab ? styles.activeTab : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>
      </header>

      <main className={styles.main}>
        {activeTab === 'draft' && (
          <PromptEditor
            prompt={basePrompt}
            onPromptChange={setBasePrompt}
            onGenerate={handleGenerateVariants}
            models={models}
            selectedModel={selectedModel}
            onModelChange={setSelectedModel}
            isLoading={isLoading}
          />
        )}

        {activeTab === 'variants' && (
          <VariantTable
            variants={variants}
            onEvaluate={handleEvaluate}
            isLoading={isLoading}
          />
        )}

        {activeTab === 'results' && (
          <ResultsView results={results} basePrompt={basePrompt} />
        )}

        {activeTab === 'history' && <HistoryGraph />}
      </main>
    </div>
  )
}