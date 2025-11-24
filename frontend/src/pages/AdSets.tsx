import { useState } from 'react'
import { Card, CardHeader, CardBody } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Target, Plus, Play, Pause, Trash2, Settings, TrendingUp } from 'lucide-react'
import { motion } from 'framer-motion'

export default function AdSets() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Ad Sets</h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Manage and monitor your ad sets
          </p>
        </div>
        <button className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors flex items-center space-x-2">
          <Plus className="w-5 h-5" />
          <span>New Ad Set</span>
        </button>
      </div>

      <Card>
        <CardBody className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Ad Set Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Platform
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Fatigue Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Performance
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                {[1, 2, 3, 4, 5].map((i) => (
                  <motion.tr
                    key={i}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: i * 0.05 }}
                    className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                  >
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <Target className="w-5 h-5 text-primary-500 mr-3" />
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white">
                            Summer Campaign {i}
                          </p>
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            Campaign ID: {1000 + i}
                          </p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <Badge variant="info">Meta</Badge>
                    </td>
                    <td className="px-6 py-4">
                      <Badge variant={i % 2 === 0 ? 'success' : 'default'}>
                        {i % 2 === 0 ? 'Active' : 'Paused'}
                      </Badge>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <div className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden w-24">
                          <div
                            className={`h-full ${
                              i < 3 ? 'bg-success-500' : i < 4 ? 'bg-warning-500' : 'bg-danger-500'
                            }`}
                            style={{ width: `${(i * 20)}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {i * 20}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm">
                        <p className="text-gray-900 dark:text-white font-medium">
                          CTR: {(2 + i * 0.2).toFixed(1)}%
                        </p>
                        <p className="text-gray-500 dark:text-gray-400">
                          CPA: ${(15 + i * 2).toFixed(2)}
                        </p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors">
                          {i % 2 === 0 ? (
                            <Pause className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                          ) : (
                            <Play className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                          )}
                        </button>
                        <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors">
                          <Settings className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                        </button>
                        <button className="p-2 hover:bg-danger-100 dark:hover:bg-danger-900/20 rounded-lg transition-colors">
                          <Trash2 className="w-4 h-4 text-danger-600 dark:text-danger-400" />
                        </button>
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardBody>
      </Card>
    </div>
  )
}
