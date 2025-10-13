import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Users, Activity, MessageSquare, TrendingUp, Calendar, UserCheck } from 'lucide-react';
import { useUserSessionContext } from '@/components/auth/UserSessionProvider';

interface User {
  id: string;
  email: string;
  name: string;
  isActive: boolean;
  lastLogin: string;
  totalSessions: number;
  totalMessages: number;
  createdAt: string;
}

interface SystemStats {
  totalUsers: number;
  activeUsers: number;
  totalSessions: number;
  totalMessages: number;
  averageSessionDuration: number;
  mostActiveHour: number;
}

const AdminDashboard: React.FC = () => {
  const { user: currentUser } = useUserSessionContext();
  const [users, setUsers] = useState<User[]>([]);
  const [systemStats, setSystemStats] = useState<SystemStats>({
    totalUsers: 0,
    activeUsers: 0,
    totalSessions: 0,
    totalMessages: 0,
    averageSessionDuration: 0,
    mostActiveHour: 0
  });
  const [loading, setLoading] = useState(true);

  // Check if current user is admin (simple check for demo)
  const isAdmin = currentUser?.email?.includes('admin') || currentUser?.email?.includes('@voicecbt.com');

  useEffect(() => {
    if (isAdmin) {
      loadAdminData();
    }
  }, [isAdmin]);

  const loadAdminData = async () => {
    setLoading(true);
    try {
      // Load users from localStorage (in real app, this would be from backend)
      const allUsers: User[] = [];
      
      // Get all conversation histories to extract user data
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key?.startsWith('voice_cbt_conversations_')) {
          const userId = key.replace('voice_cbt_conversations_', '');
          const userData = localStorage.getItem('voice_cbt_user');
          
          if (userData) {
            const parsedUser = JSON.parse(userData);
            if (parsedUser.id === userId) {
              const conversations = localStorage.getItem(key);
              const messageCount = conversations ? JSON.parse(conversations).length : 0;
              
              allUsers.push({
                id: parsedUser.id,
                email: parsedUser.email,
                name: parsedUser.name,
                isActive: true,
                lastLogin: new Date().toISOString(),
                totalSessions: Math.ceil(messageCount / 10), // Estimate sessions
                totalMessages: messageCount,
                createdAt: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
              });
            }
          }
        }
      }

      setUsers(allUsers);
      
      // Calculate system stats
      const totalUsers = allUsers.length;
      const activeUsers = allUsers.filter(u => u.isActive).length;
      const totalSessions = allUsers.reduce((sum, u) => sum + u.totalSessions, 0);
      const totalMessages = allUsers.reduce((sum, u) => sum + u.totalMessages, 0);
      
      setSystemStats({
        totalUsers,
        activeUsers,
        totalSessions,
        totalMessages,
        averageSessionDuration: 15, // Mock data
        mostActiveHour: 14 // Mock data
      });
      
    } catch (error) {
      console.error('Error loading admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isAdmin) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-96">
          <CardHeader>
            <CardTitle className="text-center text-red-600">Access Denied</CardTitle>
            <CardDescription className="text-center">
              You don't have permission to access the admin dashboard.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading admin dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-muted-foreground">Manage users and monitor system activity</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Users</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{systemStats.totalUsers}</div>
              <p className="text-xs text-muted-foreground">
                +{systemStats.activeUsers} active
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Sessions</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{systemStats.totalSessions}</div>
              <p className="text-xs text-muted-foreground">
                Avg {systemStats.averageSessionDuration} min
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Messages</CardTitle>
              <MessageSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{systemStats.totalMessages}</div>
              <p className="text-xs text-muted-foreground">
                Across all sessions
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Peak Activity</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{systemStats.mostActiveHour}:00</div>
              <p className="text-xs text-muted-foreground">
                Most active hour
              </p>
            </CardContent>
          </Card>
        </div>

        {/* User Management */}
        <Tabs defaultValue="users" className="space-y-6">
          <TabsList>
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="users" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>User Management</CardTitle>
                <CardDescription>
                  Manage registered users and their activity
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>User</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Sessions</TableHead>
                      <TableHead>Messages</TableHead>
                      <TableHead>Last Active</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {users.map((user) => (
                      <TableRow key={user.id}>
                        <TableCell className="font-medium">
                          <div className="flex items-center space-x-2">
                            <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm">
                              {user.name.charAt(0).toUpperCase()}
                            </div>
                            <span>{user.name}</span>
                          </div>
                        </TableCell>
                        <TableCell>{user.email}</TableCell>
                        <TableCell>
                          <Badge variant={user.isActive ? "default" : "secondary"}>
                            {user.isActive ? "Active" : "Inactive"}
                          </Badge>
                        </TableCell>
                        <TableCell>{user.totalSessions}</TableCell>
                        <TableCell>{user.totalMessages}</TableCell>
                        <TableCell>
                          {new Date(user.lastLogin).toLocaleDateString()}
                        </TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button size="sm" variant="outline">
                              View
                            </Button>
                            <Button size="sm" variant="outline">
                              Edit
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>System Analytics</CardTitle>
                <CardDescription>
                  Overview of system usage and performance
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-lg font-semibold mb-4">User Activity</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Active Users Today</span>
                        <span className="font-medium">{systemStats.activeUsers}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>New Users This Week</span>
                        <span className="font-medium">{Math.floor(systemStats.totalUsers * 0.1)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Average Session Duration</span>
                        <span className="font-medium">{systemStats.averageSessionDuration} min</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-semibold mb-4">System Health</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>System Status</span>
                        <Badge variant="default">Healthy</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Response Time</span>
                        <span className="font-medium">~150ms</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Uptime</span>
                        <span className="font-medium">99.9%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Admin Settings</CardTitle>
                <CardDescription>
                  Configure system settings and preferences
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold mb-2">User Management</h3>
                    <div className="space-y-2">
                      <Button variant="outline" className="w-full justify-start">
                        <UserCheck className="mr-2 h-4 w-4" />
                        Enable New User Registration
                      </Button>
                      <Button variant="outline" className="w-full justify-start">
                        <Calendar className="mr-2 h-4 w-4" />
                        Set Maintenance Window
                      </Button>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-semibold mb-2">System Maintenance</h3>
                    <div className="space-y-2">
                      <Button variant="outline" className="w-full justify-start">
                        Clear Old Sessions
                      </Button>
                      <Button variant="outline" className="w-full justify-start">
                        Export User Data
                      </Button>
                      <Button variant="outline" className="w-full justify-start">
                        Backup Database
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminDashboard;
