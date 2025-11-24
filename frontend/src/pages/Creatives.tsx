import { useState } from 'react'
import { Card, CardHeader, CardBody } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import {
  Sparkles,
  Image,
  Video,
  LayoutGrid,
  Copy,
  Wand2,
  Plus,
  Play,
  Pause,
  Archive,
  TrendingUp,
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'

interface Creative {
  id: number
  name: string
  format: 'image' | 'video' | 'carousel' | 'collection'
  status: 'active' | 'paused' | 'testing' | 'archived'
  headline: string
  bodyText: string
  cta: string
  performance: {
    ctr: number
    conversions: number
    spend: number
  }
  variationType: string
  aiGenerated: boolean
  imageUrl?: string
}

export default function Creatives() {
  const [selectedCreative, setSelectedCreative] = useState<Creative | null>(null)
  const [showGenerateModal, setShowGenerateModal] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [variationType, setVariationType] = useState<string[]>([])
  const [variationCount, setVariationCount] = useState(3)

  // Mock data
  const creatives: Creative[] = [
    {
      id: 1,
      name: 'Summer Sale Hero Image',
      format: 'image',
      status: 'active',
      headline: 'Get 50% Off Summer Collection',
      bodyText: 'Limited time offer! Shop premium styles now.',
      cta: 'Shop Now',
      performance: { ctr: 2.8, conversions: 125, spend: 450.5 },
      variationType: 'original',
      aiGenerated: false,
      imageUrl: 'https://via.placeholder.com/400x300/0ea5e9/ffffff?text=Summer+Sale',
    },
    {
      id: 2,
      name: 'Summer Sale - Hook Variation',
      format: 'image',
      status: 'testing',
      headline: 'Save Big on Your Favorite Summer Styles',
      bodyText: 'Limited time offer! Shop premium styles now.',
      cta: 'Shop Now',
      performance: { ctr: 3.2, conversions: 142, spend: 420.0 },
      variationType: 'hook_variation',
      aiGenerated: true,
      imageUrl: 'https://via.placeholder.com/400x300/22c55e/ffffff?text=Hook+Variation',
    },
    {
      id: 3,
      name: 'Product Showcase Video',
      format: 'video',
      status: 'active',
      headline: 'See Our Products in Action',
      bodyText: 'Watch how our products transform your summer.',
      cta: 'Watch Now',
      performance: { ctr: 4.1, conversions: 198, spend: 680.0 },
      variationType: 'original',
      aiGenerated: false,
      imageUrl: 'https://via.placeholder.com/400x300/f59e0b/ffffff?text=Video+Ad',
    },
  ]

  const formatIcons = {
    image: <Image className="w-4 h-4" />,
    video: <Video className="w-4 h-4" />,
    carousel: <LayoutGrid className="w-4 h-4" />,
    collection: <Copy className="w-4 h-4" />,
  }

  const handleGenerate = async () => {
    if (!selectedCreative || variationType.length === 0) {
      toast.error('Please select a creative and variation types')
      return
    }

    setGenerating(true)
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000))
      toast.success(`Generated ${variationCount} variations successfully!`)
      setShowGenerateModal(false)
      setVariationType([])
    } catch (error) {
      toast.error('Failed to generate variations')
    } finally {
      setGenerating(false)
    }
  }

  const toggleVariationType = (type: string) => {
    setVariationType((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            Creative Management
          </h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Manage and generate creative variations with AI
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowGenerateModal(true)}
            className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors flex items-center space-x-2"
          >
            <Sparkles className="w-5 h-5" />
            <span>Generate Variations</span>
          </button>
          <button className="px-4 py-2 bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 text-gray-900 dark:text-white rounded-lg font-medium transition-colors flex items-center space-x-2">
            <Plus className="w-5 h-5" />
            <span>New Creative</span>
          </button>
        </div>
      </div>

      {/* Creatives Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {creatives.map((creative) => (
          <motion.div
            key={creative.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.02 }}
            className="cursor-pointer"
            onClick={() => setSelectedCreative(creative)}
          >
            <Card hoverable>
              {/* Image Preview */}
              <div className="relative h-48 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 rounded-t-xl overflow-hidden">
                {creative.imageUrl && (
                  <img
                    src={creative.imageUrl}
                    alt={creative.name}
                    className="w-full h-full object-cover"
                  />
                )}
                <div className="absolute top-3 right-3 flex space-x-2">
                  {creative.aiGenerated && (
                    <Badge variant="info">
                      <Wand2 className="w-3 h-3 mr-1" />
                      AI Generated
                    </Badge>
                  )}
                  <Badge variant={creative.status === 'active' ? 'success' : 'default'}>
                    {creative.status}
                  </Badge>
                </div>
                <div className="absolute bottom-3 left-3">
                  <Badge variant="default">{formatIcons[creative.format]}</Badge>
                </div>
              </div>

              <CardBody>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {creative.name}
                </h3>

                {/* Creative Content Preview */}
                <div className="space-y-2 mb-4">
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-500">Headline</p>
                    <p className="text-sm text-gray-900 dark:text-white line-clamp-1">
                      {creative.headline}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-500">Body</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                      {creative.bodyText}
                    </p>
                  </div>
                </div>

                {/* Performance Metrics */}
                <div className="grid grid-cols-3 gap-2 pt-3 border-t border-gray-200 dark:border-gray-800">
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-500">CTR</p>
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">
                      {creative.performance.ctr}%
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-500">Conv.</p>
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">
                      {creative.performance.conversions}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-500">Spend</p>
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">
                      ${creative.performance.spend}
                    </p>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex space-x-2 mt-4">
                  {creative.status === 'active' ? (
                    <button className="flex-1 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg text-sm font-medium transition-colors flex items-center justify-center space-x-1">
                      <Pause className="w-4 h-4" />
                      <span>Pause</span>
                    </button>
                  ) : (
                    <button className="flex-1 px-3 py-1.5 bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400 hover:bg-success-200 dark:hover:bg-success-900/30 rounded-lg text-sm font-medium transition-colors flex items-center justify-center space-x-1">
                      <Play className="w-4 h-4" />
                      <span>Activate</span>
                    </button>
                  )}
                  <button className="flex-1 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg text-sm font-medium transition-colors flex items-center justify-center space-x-1">
                    <Archive className="w-4 h-4" />
                    <span>Archive</span>
                  </button>
                </div>
              </CardBody>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Generate Modal */}
      <AnimatePresence>
        {showGenerateModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => !generating && setShowGenerateModal(false)}
              className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            />

            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="relative w-full max-w-2xl bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800"
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-800">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-primary-100 dark:bg-primary-900/20 rounded-lg">
                    <Sparkles className="w-6 h-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                      Generate Creative Variations
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      AI-powered creative generation
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-6 space-y-6">
                {/* Select Creative */}
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white mb-2">
                    Select Original Creative
                  </label>
                  <select
                    value={selectedCreative?.id || ''}
                    onChange={(e) =>
                      setSelectedCreative(
                        creatives.find((c) => c.id === parseInt(e.target.value)) || null
                      )
                    }
                    className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Choose a creative...</option>
                    {creatives.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Variation Types */}
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white mb-3">
                    Variation Types
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    {['hook', 'angle', 'copy', 'format'].map((type) => (
                      <button
                        key={type}
                        onClick={() => toggleVariationType(type)}
                        className={`p-4 rounded-lg border-2 transition-all ${
                          variationType.includes(type)
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                        }`}
                      >
                        <p className="font-medium text-gray-900 dark:text-white capitalize">
                          {type} Variation
                        </p>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          {type === 'hook' && 'Different opening hooks'}
                          {type === 'angle' && 'Different value propositions'}
                          {type === 'copy' && 'Rewritten body text'}
                          {type === 'format' && 'Different ad formats'}
                        </p>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Variation Count */}
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white mb-2">
                    Number of Variations: {variationCount}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={variationCount}
                    onChange={(e) => setVariationCount(parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-primary-500"
                  />
                  <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mt-1">
                    <span>1</span>
                    <span>10</span>
                  </div>
                </div>
              </div>

              <div className="p-6 border-t border-gray-200 dark:border-gray-800 flex justify-end space-x-3">
                <button
                  onClick={() => setShowGenerateModal(false)}
                  disabled={generating}
                  className="px-4 py-2 bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 text-gray-900 dark:text-white rounded-lg font-medium transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleGenerate}
                  disabled={generating || !selectedCreative || variationType.length === 0}
                  className="px-6 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center space-x-2"
                >
                  {generating ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      <span>Generating...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      <span>Generate {variationCount} Variations</span>
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  )
}
