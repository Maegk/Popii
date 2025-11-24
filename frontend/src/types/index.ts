export interface AdSet {
  id: number
  external_id: string
  platform: 'meta' | 'google' | 'tiktok' | 'linkedin'
  name: string
  monitoring_status: 'active' | 'paused' | 'stopped'
  auto_rotation_enabled: boolean
  created_at: string
  updated_at: string
}

export interface Creative {
  id: number
  name: string
  format: 'image' | 'video' | 'carousel' | 'collection'
  status: 'active' | 'paused' | 'archived' | 'testing'
  headline: string | null
  body_text: string | null
  call_to_action: string | null
  variation_type: string
  generated_by_ai: boolean
  created_at: string
}

export interface Metrics {
  ctr: number
  cpa: number
  cpm: number
  frequency: number
  engagement_rate: number
  impressions: number
  spend: number
  date: string
}

export interface FatigueScore {
  ad_set_id: number
  ad_set_name?: string
  fatigue_score: number
  fatigue_level: 'low' | 'moderate' | 'high' | 'critical'
  confidence: number
  action_required: boolean
  predicted_at?: string
}

export interface MonitoringStatus {
  ad_set_id: number
  ad_set_name: string
  monitoring_status: string
  current_metrics: Metrics
  anomalies: {
    has_anomaly: boolean
    ctr_drop: boolean
    cpa_increase: boolean
    engagement_drop: boolean
    high_frequency: boolean
    [key: string]: any
  }
  should_alert: boolean
  last_updated: string
}

export interface Recommendation {
  type: string
  recommendation: string
  reason: string
  confidence: number
}

export interface RotationHistory {
  creative_id: number
  creative_name: string
  paused_at: string
  variation_type: string
  was_ai_generated: boolean
}
