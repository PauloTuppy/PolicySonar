import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import PolicyChart from './PolicyChart';
import PolicySummary from './PolicySummary';
import PolicyComparison from './PolicyComparison';

interface PolicyDashboardProps {
  simulationData: any;
  comparisonData?: any[];
}

const PolicyDashboard: React.FC<PolicyDashboardProps> = ({ 
  simulationData,
  comparisonData = []
}) => {
  return (
    <div className="space-y-6">
      <Tabs defaultValue="analysis" className="w-full">
        <TabsList>
          <TabsTrigger value="analysis">Impact Analysis</TabsTrigger>
          <TabsTrigger value="summary">Key Metrics</TabsTrigger>
          {comparisonData.length > 0 && (
            <TabsTrigger value="comparison">Policy Comparison</TabsTrigger>
          )}
        </TabsList>

        <TabsContent value="analysis">
          <div className="grid gap-6 md:grid-cols-2">
            <PolicyChart 
              simulationData={simulationData} 
              timeframe="medium" 
            />
            <PolicyChart 
              simulationData={simulationData} 
              timeframe="long" 
            />
          </div>
        </TabsContent>

        <TabsContent value="summary">
          <PolicySummary data={simulationData} />
        </TabsContent>

        {comparisonData.length > 0 && (
          <TabsContent value="comparison">
            <PolicyComparison 
              currentData={simulationData} 
              comparisonData={comparisonData} 
            />
          </TabsContent>
        )}
      </Tabs>
    </div>
  );
};

export default PolicyDashboard;
