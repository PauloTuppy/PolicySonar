import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { format } from 'date-fns';

interface PolicySummaryProps {
  data: any;
}

const PolicySummary: React.FC<PolicySummaryProps> = ({ data }) => {
  const metrics = [
    { 
      name: 'GDP Impact', 
      value: data.base_projections.gdp_impact,
      uncertainty: data.uncertainty.gdp_impact,
      unit: '%'
    },
    { 
      name: 'Inflation Impact', 
      value: data.base_projections.inflation_impact,
      uncertainty: data.uncertainty.inflation_impact,
      unit: 'pp'
    },
    { 
      name: 'Employment Impact', 
      value: data.base_projections.employment_impact,
      uncertainty: data.uncertainty.employment_impact,
      unit: 'pp'
    }
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Key Policy Impacts</CardTitle>
        <div className="text-sm text-muted-foreground">
          Last updated: {format(new Date(data.timestamp), 'PPpp')}
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 md:grid-cols-3">
          {metrics.map((metric) => (
            <div key={metric.name} className="space-y-2">
              <h3 className="font-medium">{metric.name}</h3>
              <div className="text-2xl font-bold">
                {metric.value > 0 ? '+' : ''}{metric.value.toFixed(2)}{metric.unit}
              </div>
              <div className="flex gap-2">
                <Badge variant="secondary">
                  Range: {metric.uncertainty.p5.toFixed(2)} to {metric.uncertainty.p95.toFixed(2)}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default PolicySummary;
