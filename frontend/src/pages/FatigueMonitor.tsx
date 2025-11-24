import { useState } from 'react'
import { Card, CardHeader, CardBody } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import {
  AlertTriangle,
  TrendingDown,
  Activity,
  Target,
  Zap,
  CheckCircle,
  XCircle,
} from 'lucide-react'
import { motion } from 'framer-motion'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts'

interface FatigueData {
  id: number
  adSetName: string
  score: number
  level: 'low' | 'moderate' | 'high' | 'critical'
  frequency: number
  ctr: number
  cpa: number
  trend: 'improving' | 'stable' | 'declining'
  actionRequired: boolean
}

export default function FatigueMonitor() {
  const [selectedAdSet, setSelectedAdSet] = useState<number | null>(null)

  // Mock data
  const fatigueData: FatigueData[] = [
    {
      id: 1,
      adSetName: 'Summer Campaign - Conversion',
      score: 0.75,
      level: 'high',
      frequency: 7.2,
      ctr: 1.8,
      cpa: 22.5,
      trend: 'declining',
      actionRequired: true,
    },
    {
      id: 2,
      adSetName: 'Winter Sale - Awareness',
      score: 0.45,
      level: 'moderate',
      frequency: 5.1,
      ctr: 2.4,
      cpa: 15.2,
      trend: 'stable',
      actionRequired: false,
    },
    {
      id: 3,
      adSetName: 'Spring Collection - Traffic',
      score: 0.25,
      level: 'low',
      frequency: 3.8,
      ctr: 3.1,
      cpa: 12.1,
      trend: 'improving',
      actionRequired: false,
    },
    {
      id: 4,
      adSetName: 'Fall Preview - Engagement',
      score: 0.88,
      level: 'critical',
      frequency: 9.5,
      ctr: 1.2,
      cpa: 28.9,
      trend: 'declining',
      actionRequired: true,
    },
  ]

  const timelineData = [
    { day: 'Day 1', score: 0.15, ctr: 3.2, frequency: 2.1 },
    { day: 'Day 2', score: 0.22, ctr: 3.0, frequency: 3.4 },
    { day: 'Day 3', score: 0.35, ctr: 2.8, frequency: 4.2 },
    { day: 'Day 4', score: 0.48, ctr: 2.5, frequency: 5.5 },
    { day: 'Day 5', score: 0.62, ctr: 2.1, frequency: 6.8 },
    { day: 'Day 6', score: 0.75, ctr: 1.8, frequency: 7.9 },
    { day: 'Day 7', score: 0.82, ctr: 1.5, frequency: 8.5 },
  ]

  const radarData = [
    { metric: 'Frequency', value: 75, fullMark: 100 },
    { metric: 'CTR Decay', value: 65, fullMark: 100 },
    { metric: 'CPA Increase', value: 80, fullMark: 100 },
    { metric: 'Engagement Drop', value: 55, fullMark: 100 },
    { metric: 'Negative Feedback', value: 40, fullMark: 100 },
  ]

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'low':
        return 'success'
      case 'moderate':
        return 'warning'
      case 'high':
        return 'warning'
      case 'critical':
        return 'danger'
      default:
        return 'default'
    }
  }

  const getLevelIcon = (level: string) => {
    switch (level) {
      case 'low':
        return <CheckCircle className="w-5 h-5" />
      case 'critical':
        return <XCircle className="w-5 h-5" />
      default:
        return <AlertTriangle className="w-5 h-5" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            Fatigue Monitor
          </h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Real-time creative fatigue detection and alerts
          </p>
        </div>
        <button className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors flex items-center space-x-2">
          <Zap className="w-5 h-5" />
          <span>Scan All Ad Sets</span>
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {['low', 'moderate', 'high', 'critical'].map((level, index) => {
          const count = fatigueData.filter((d) => d.level === level).length
          return (
            <motion.div
              key={level}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white dark:bg-gray-900 rounded-lg p-4 border border-gray-200 dark:border-gray-800"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 capitalize">
                    {level} Fatigue
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                    {count}
                  </p>
                </div>
                <Badge variant={getLevelColor(level)}>
                  {getLevelIcon(level)}
                </Badge>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Ad Sets List */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Ad Set Fatigue Scores
              </h3>
            </CardHeader>
            <CardBody className="p-0">
              <div className="divide-y divide-gray-200 dark:divide-gray-800">
                {fatigueData.map((item) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className={`p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer ${
                      selectedAdSet === item.id ? 'bg-primary-50 dark:bg-primary-900/10' : ''
                    }`}
                    onClick={() => setSelectedAdSet(item.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <h4 className="font-medium text-gray-900 dark:text-white">
                            {item.adSetName}
                          </h4>
                          <Badge variant={getLevelColor(item.level)}>
                            {item.level.toUpperCase()}
                          </Badge>
                          {item.actionRequired && (
                            <Badge variant="danger">Action Required</Badge>
                          )}
                        </div>

                        {/* Metrics Row */}
                        <div className="mt-3 grid grid-cols-3 gap-4">
                          <div>
                            <p className="text-xs text-gray-600 dark:text-gray-400">
                              Fatigue Score
                            </p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                              {(item.score * 100).toFixed(0)}%
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-600 dark:text-gray-400">
                              Frequency
                            </p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                              {item.frequency.toFixed(1)}
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-600 dark:text-gray-400">CTR</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                              {item.ctr.toFixed(1)}%
                            </p>
                          </div>
                        </div>

                        {/* Progress Bar */}
                        <div className="mt-3">
                          <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div
                              className={`h-full transition-all ${
                                item.level === 'critical'
                                  ? 'bg-danger-500'
                                  : item.level === 'high'
                                  ? 'bg-warning-500'
                                  : item.level === 'moderate'
                                  ? 'bg-warning-400'
                                  : 'bg-success-500'
                              }`}
                              style={{ width: `${item.score * 100}%` }}
                            />
                          </div>
                        </div>
                      </div>

                      {item.actionRequired && (
                        <button className="ml-4 px-3 py-1.5 bg-primary-500 hover:bg-primary-600 text-white text-sm rounded-lg font-medium transition-colors">
                          Rotate Creative
                        </button>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Fatigue Factors Radar */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Fatigue Factors
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Contributing factors breakdown
              </p>
            </CardHeader>
            <CardBody className="flex justify-center">
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#374151" />
                  <PolarAngleAxis
                    dataKey="metric"
                    tick={{ fill: '#9ca3af', fontSize: 11 }}
                  />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#9ca3af' }} />
                  <Radar
                    name="Score"
                    dataKey="value"
                    stroke="#0ea5e9"
                    fill="#0ea5e9"
                    fillOpacity={0.5}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Recommendations
              </h3>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <Activity className="w-5 h-5 text-primary-500 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Rotate high fatigue creatives
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                      4 ad sets need immediate attention
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <TrendingDown className="w-5 h-5 text-warning-500 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Lower frequency caps
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                      Reduce audience saturation
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Target className="w-5 h-5 text-success-500 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Expand targeting
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                      Reach fresh audiences
                    </p>
                  </div>
                </div>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>

      {/* Timeline Chart */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Fatigue Progression
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            7-day fatigue score trend
          </p>
        </CardHeader>
        <CardBody>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={timelineData}>
              <defs>
                <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
              <XAxis dataKey="day" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#f3f4f6',
                }}
              />
              <Area
                type="monotone"
                dataKey="score"
                stroke="#0ea5e9"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorScore)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </CardBody>
      </Card>
    </div>
  )
}
