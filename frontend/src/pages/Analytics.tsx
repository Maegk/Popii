import { Card, CardHeader, CardBody } from '@/components/ui/Card'
import { BarChart3 } from 'lucide-react'

export default function Analytics() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Analytics</h2>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Deep insights into creative performance
        </p>
      </div>

      <Card>
        <CardBody className="p-12 text-center">
          <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Advanced Analytics Coming Soon
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Comprehensive performance analytics and insights will be available here
          </p>
        </CardBody>
      </Card>
    </div>
  )
}
