import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { 
  Users, 
  Activity, 
  TrendingUp, 
  Brain, 
  Clock, 
  BarChart3,
  Smartphone,
  Monitor
} from 'lucide-react';

interface AnalyticsData {
  period: {
    start_date: string;
    end_date: string;
    days: number;
  };
  users: {
    total: number;
    active: number;
    growth_rate: number;
  };
  sessions: {
    total: number;
    completed: number;
    completion_rate: number;
    average_duration_minutes: number;
  };
  emotions: {
    total_entries: number;
    distribution: Record<string, number>;
    most_common: string;
  };
  recent_activity: {
    sessions_last_7_days: number;
    mood_entries_last_7_days: number;
  };
}

interface EmotionTrend {
  date: string;
  total_entries: number;
  emotions: Record<string, number>;
  percentages: Record<string, number>;
}

interface UserEngagement {
  user_id: string;
  username: string;
  sessions_count: number;
  mood_entries_count: number;
  engagement_score: number;
  last_activity: string | null;
}

const AnalyticsDashboard: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [emotionTrends, setEmotionTrends] = useState<EmotionTrend[]>([]);
  const [userEngagement, setUserEngagement] = useState<UserEngagement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isMobile, setIsMobile] = useState(false);

  // Check if mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Fetch analytics data
  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        
        const [overviewRes, trendsRes, engagementRes] = await Promise.all([
          fetch('/api/v1/analytics/overview?days=30'),
          fetch('/api/v1/analytics/emotions/trends?days=30'),
          fetch('/api/v1/analytics/users/engagement?days=30')
        ]);

        if (!overviewRes.ok || !trendsRes.ok || !engagementRes.ok) {
          throw new Error('Failed to fetch analytics data');
        }

        const [overview, trends, engagement] = await Promise.all([
          overviewRes.json(),
          trendsRes.json(),
          engagementRes.json()
        ]);

        setAnalyticsData(overview);
        setEmotionTrends(trends.trends || []);
        setUserEngagement(engagement.user_engagement || []);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load analytics');
        console.error('Analytics fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  const emotionColors: Record<string, string> = {
    happy: 'bg-green-500',
    sad: 'bg-blue-500',
    angry: 'bg-red-500',
    fear: 'bg-yellow-500',
    surprise: 'bg-purple-500',
    disgust: 'bg-orange-500',
    neutral: 'bg-gray-500'
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error Loading Analytics</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>
            Retry
          </Button>
        </div>
      </div>
    );
  }

  if (!analyticsData) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-600">No Data Available</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
            <div className="flex items-center space-x-2">
              {isMobile ? <Smartphone className="h-5 w-5" /> : <Monitor className="h-5 w-5" />}
              <span className="text-sm text-gray-500">
                {isMobile ? 'Mobile View' : 'Desktop View'}
              </span>
            </div>
          </div>
          <p className="text-gray-600">
            Comprehensive insights into your Voice CBT application usage
          </p>
        </div>

        {/* Overview Cards */}
        <div className={`grid gap-6 mb-8 ${isMobile ? 'grid-cols-1' : 'grid-cols-2 lg:grid-cols-4'}`}>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Users</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analyticsData.users.total}</div>
              <p className="text-xs text-muted-foreground">
                {analyticsData.users.active} active users
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Sessions</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analyticsData.sessions.total}</div>
              <p className="text-xs text-muted-foreground">
                {analyticsData.sessions.completion_rate.toFixed(1)}% completion rate
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Duration</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {analyticsData.sessions.average_duration_minutes.toFixed(1)}m
              </div>
              <p className="text-xs text-muted-foreground">
                per session
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Emotions Tracked</CardTitle>
              <Brain className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analyticsData.emotions.total_entries}</div>
              <p className="text-xs text-muted-foreground">
                Most common: {analyticsData.emotions.most_common}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Analytics */}
        <Tabs defaultValue="emotions" className="space-y-6">
          <TabsList className={`${isMobile ? 'grid w-full grid-cols-2' : ''}`}>
            <TabsTrigger value="emotions">Emotion Analysis</TabsTrigger>
            <TabsTrigger value="trends">Trends</TabsTrigger>
            <TabsTrigger value="engagement">User Engagement</TabsTrigger>
            <TabsTrigger value="sessions">Session Details</TabsTrigger>
          </TabsList>

          <TabsContent value="emotions" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Emotion Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {Object.entries(analyticsData.emotions.distribution).map(([emotion, percentage]) => (
                    <div key={emotion} className="flex items-center space-x-4">
                      <div className="w-20 text-sm font-medium capitalize">{emotion}</div>
                      <div className="flex-1">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${emotionColors[emotion] || 'bg-gray-500'}`}
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                      </div>
                      <div className="w-16 text-sm text-gray-600 text-right">
                        {percentage.toFixed(1)}%
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="trends" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Emotion Trends Over Time</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {emotionTrends.slice(-7).map((trend, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">{trend.date}</span>
                        <Badge variant="secondary">{trend.total_entries} entries</Badge>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {Object.entries(trend.percentages).map(([emotion, percentage]) => (
                          <div key={emotion} className="flex items-center space-x-1">
                            <div className={`w-3 h-3 rounded-full ${emotionColors[emotion] || 'bg-gray-500'}`}></div>
                            <span className="text-sm capitalize">{emotion}</span>
                            <span className="text-sm text-gray-500">({percentage.toFixed(1)}%)</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="engagement" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Top Users by Engagement</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {userEngagement.slice(0, 10).map((user, index) => (
                    <div key={user.user_id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                          {index + 1}
                        </div>
                        <div>
                          <div className="font-medium">{user.username}</div>
                          <div className="text-sm text-gray-500">
                            {user.sessions_count} sessions, {user.mood_entries_count} mood entries
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-blue-600">{user.engagement_score}</div>
                        <div className="text-sm text-gray-500">engagement score</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="sessions" className="space-y-6">
            <div className={`grid gap-6 ${isMobile ? 'grid-cols-1' : 'grid-cols-2'}`}>
              <Card>
                <CardHeader>
                  <CardTitle>Session Statistics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between">
                      <span>Total Sessions:</span>
                      <span className="font-bold">{analyticsData.sessions.total}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Completed:</span>
                      <span className="font-bold text-green-600">{analyticsData.sessions.completed}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Completion Rate:</span>
                      <span className="font-bold">{analyticsData.sessions.completion_rate.toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Avg Duration:</span>
                      <span className="font-bold">{analyticsData.sessions.average_duration_minutes.toFixed(1)}m</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between">
                      <span>Sessions (7 days):</span>
                      <span className="font-bold">{analyticsData.recent_activity.sessions_last_7_days}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Mood Entries (7 days):</span>
                      <span className="font-bold">{analyticsData.recent_activity.mood_entries_last_7_days}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
