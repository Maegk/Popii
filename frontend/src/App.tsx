import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import AdSets from './pages/AdSets'
import Creatives from './pages/Creatives'
import FatigueMonitor from './pages/FatigueMonitor'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="ad-sets" element={<AdSets />} />
        <Route path="creatives" element={<Creatives />} />
        <Route path="fatigue" element={<FatigueMonitor />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  )
}

export default App
