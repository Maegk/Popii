import { useEffect, useState } from 'react'
import { Target, Sparkles, TrendingUp, AlertTriangle, DollarSign, Eye } from 'lucide-react'
import { MetricCard } from '@/components/dashboard/MetricCard'
import { Card, CardHeader, CardBody } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import { adSetsApi, fatigueApi } from '@/lib/api'
import { useStore } from '@/store/useStore'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const { adSets, setAdSets } = useStore()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const response = await adSetsApi.list()
      setAdSets(response.data)
    } catch (error) {
      toast.error('Failed to load dashboard data')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  // Mock data for charts
  const performanceData = [
    { date: 'Mon', ctr: 2.4, cpa: 15.2, fatigue: 0.3 },
    { date: 'Tue', ctr: 2.6, cpa: 14.8, fatigue: 0.35 },
    { date: 'Wed', ctr: 2.3, cpa: 16.1, fatigue: 0.45 },
    { date: 'Thu', ctr: 2.1, cpa: 17.5, fatigue: 0.55 },
    { date: 'Fri', ctr: 1.9, cpa: 18.9, fatigue: 0.68 },
    { date: 'Sat', ctr: 2.5, cpa: 14.2, fatigue: 0.25 },
    { date: 'Sun', ctr: 2.7, cpa: 13.5, fatigue: 0.22 },
  ]

  const fatigueDistribution = [
    { name: 'Low', value: 45, color: '#22c55e' },
    { name: 'Moderate', value: 30, color: '#f59e0b' },
    { name: 'High', value: 20, color: '#ef4444' },
    { name: 'Critical', value: 5, color: '#dc2626' },
  ]

  const recentRotations = [
    { id: 1, adSet: 'Summer Campaign', creative: 'Beach Scene v2', time: '2 hours ago', status: 'success' },
    { id: 2, adSet: 'Winter Sale', creative: 'Snow Mountain v3', time: '5 hours ago', status: 'success' },
    { id: 3, adSet: 'Spring Collection', creative: 'Flower Field v1', time: '1 day ago', status: 'success' },
  ]

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h2>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Monitor creative performance and fatigue across all campaigns
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Active Ad Sets"
          value={adSets.length || 24}
          change={12}
          icon={<Target className="w-6 h-6" />}
          iconBg="bg-primary-500"
          delay={0}
        />
        <MetricCard
          title="Active Creatives"
          value={156}
          change={8}
          icon={<Sparkles className="w-6 h-6" />}
          iconBg="bg-purple-500"
          delay={0.1}
        />
        <MetricCard
          title="Avg. CTR"
          value="2.4%"
          change={-5}
          icon={<TrendingUp className="w-6 h-6" />}
          iconBg="bg-success-500"
          delay={0.2}
        />
        <MetricCard
          title="High Fatigue Alerts"
          value={8}
          change={-15}
          icon={<AlertTriangle className="w-6 h-6" />}
          iconBg="bg-warning-500"
          delay={0.3}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Trends */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Performance Trends
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              CTR and CPA over the last 7 days
            </p>
          </CardHeader>
          <CardBody>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
                <XAxis
                  dataKey="date"
                  stroke="#9ca3af"
                  style={{ fontSize: '12px' }}
                />
                <YAxis
                  yAxisId="left"
                  stroke="#9ca3af"
                  style={{ fontSize: '12px' }}
                />
                <YAxis
                  yAxisId="right"
                  orientation="right"
                  stroke="#9ca3af"
                  style={{ fontSize: '12px' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#f3f4f6',
                  }}
                />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="ctr"
                  stroke="#22c55e"
                  strokeWidth={2}
                  dot={{ fill: '#22c55e', r: 4 }}
                  name="CTR %"
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="cpa"
                  stroke="#f59e0b"
                  strokeWidth={2}
                  dot={{ fill: '#f59e0b', r: 4 }}
                  name="CPA $"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardBody>
        </Card>

        {/* Fatigue Distribution */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Fatigue Distribution
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Current fatigue levels across all ad sets
            </p>
          </CardHeader>
          <CardBody className="flex items-center justify-center">
            <div className="w-full max-w-sm">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={fatigueDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {fatigueDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1f2937',
                      border: 'none',
                      borderRadius: '8px',
                      color: '#f3f4f6',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="mt-4 grid grid-cols-2 gap-2">
                {fatigueDistribution.map((item) => (
                  <div key={item.name} className="flex items-center space-x-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {item.name}: {item.value}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Fatigue Timeline */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Fatigue Score Timeline
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Average fatigue score progression
          </p>
        </CardHeader>
        <CardBody>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
              <XAxis dataKey="date" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#f3f4f6',
                }}
              />
              <Bar dataKey="fatigue" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardBody>
      </Card>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Rotations */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Recent Rotations
            </h3>
          </CardHeader>
          <CardBody className="p-0">
            <div className="divide-y divide-gray-200 dark:divide-gray-800">
              {recentRotations.map((rotation) => (
                <div key={rotation.id} className="p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {rotation.adSet}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Rotated to: {rotation.creative}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                        {rotation.time}
                      </p>
                    </div>
                    <Badge variant="success">Success</Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Quick Actions
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-3">
              <button className="w-full px-4 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors flex items-center justify-center space-x-2">
                <Sparkles className="w-5 h-5" />
                <span>Generate Creative Variations</span>
              </button>
              <button className="w-full px-4 py-3 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-900 dark:text-white rounded-lg font-medium transition-colors flex items-center justify-center space-x-2">
                <Target className="w-5 h-5" />
                <span>Create New Ad Set</span>
              </button>
              <button className="w-full px-4 py-3 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-900 dark:text-white rounded-lg font-medium transition-colors flex items-center justify-center space-x-2">
                <AlertTriangle className="w-5 h-5" />
                <span>Check All Fatigue Scores</span>
              </button>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
