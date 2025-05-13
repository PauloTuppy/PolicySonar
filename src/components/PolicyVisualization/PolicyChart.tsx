import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { format } from 'date-fns';

interface EconomicImpact {
  gdp_impact: number;
  inflation_impact: number;
  employment_impact: number;
}

interface UncertaintyRange {
  mean: number;
  median: number;
  p5: number;
  p95: number;
}

interface SimulationData {
  base_projections: EconomicImpact;
  uncertainty: {
    gdp_impact: UncertaintyRange;
    inflation_impact: UncertaintyRange;
    employment_impact: UncertaintyRange;
  };
  equity_impacts: Record<string, any>;
  timestamp: string;
}

interface PolicyChartProps {
  simulationData: SimulationData;
  timeframe: 'short' | 'medium' | 'long';
}

const PolicyChart: React.FC<PolicyChartProps> = ({ simulationData, timeframe }) => {
  const [metric, setMetric] = useState<keyof EconomicImpact>('gdp_impact');
  const [chartType, setChartType] = useState<'projection' | 'distribution' | 'equity'>('projection');

  const generateTimePeriods = () => {
    const years = timeframe === 'short' ? 2 : timeframe === 'medium' ? 5 : 10;
    return Array.from({ length: years + 1 }, (_, i) => new Date().getFullYear() + i);
  };

  const timePeriods = generateTimePeriods();

  const generateProjectionData = () => {
    const baseValue = simulationData.base_projections[metric];
    const uncertainty = simulationData.uncertainty[metric];

    return {
      meanValues: timePeriods.map((_, i) => i === 0 ? 0 : Number((baseValue * i).toFixed(2))),
      lowerBound: timePeriods.map((_, i) => i === 0 ? 0 : Number((uncertainty.p5 * i).toFixed(2))),
      upperBound: timePeriods.map((_, i) => i === 0 ? 0 : Number((uncertainty.p95 * i).toFixed(2))),
    };
  };

  const { meanValues, lowerBound, upperBound } = generateProjectionData();

  const getMetricTitle = () => {
    const titles = {
      gdp_impact: 'GDP Impact',
      inflation_impact: 'Inflation Impact',
      employment_impact: 'Employment Impact'
    };
    return titles[metric] || 'Economic Impact';
  };

  const renderProjectionChart = () => (
    <Plot
      data={[
        {
          x: timePeriods,
          y: meanValues,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Projected Impact',
          line: { color: '#3b82f6', width: 3 }
        },
        {
          x: [...timePeriods, ...timePeriods.slice().reverse()],
          y: [...upperBound, ...lowerBound.slice().reverse()],
          fill: 'toself',
          fillcolor: 'rgba(59, 130, 246, 0.2)',
          line: { color: 'transparent' },
          name: '90% Confidence Interval'
        }
      ]}
      layout={{
        title: `${getMetricTitle()} Projection`,
        xaxis: { title: 'Year', tickmode: 'array', tickvals: timePeriods },
        yaxis: { title: `${getMetricTitle()} (%)` },
        margin: { t: 40, l: 50, r: 30, b: 50 },
        hovermode: 'closest'
      }}
      config={{ responsive: true }}
    />
  );

  const renderDistributionChart = () => (
    <Plot
      data={[
        {
          type: 'violin',
          y: [simulationData.uncertainty[metric].p5, simulationData.uncertainty[metric].mean, 
              simulationData.uncertainty[metric].p95],
          name: 'Impact Distribution',
          box: { visible: true },
          line: { color: '#3b82f6' },
          fillcolor: 'rgba(59, 130, 246, 0.2)'
        }
      ]}
      layout={{
        title: `${getMetricTitle()} Uncertainty Distribution`,
        yaxis: { title: `${getMetricTitle()} (%)` },
        margin: { t: 40, l: 50, r: 30, b: 50 }
      }}
    />
  );

  const renderEquityChart = () => (
    <Plot
      data={Object.entries(simulationData.equity_impacts).map(([group, value]) => ({
        x: [group],
        y: [value[metric]],
        type: 'bar',
        name: group
      }))}
      layout={{
        title: `${getMetricTitle()} by Demographic Group`,
        yaxis: { title: `${getMetricTitle()} (%)` },
        margin: { t: 40, l: 50, r: 30, b: 100 },
        barmode: 'group'
      }}
    />
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Policy Impact Analysis</CardTitle>
        <div className="flex gap-4 mt-4">
          <Select value={metric} onValueChange={(value) => setMetric(value as keyof EconomicImpact)}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select metric" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="gdp_impact">GDP Impact</SelectItem>
              <SelectItem value="inflation_impact">Inflation Impact</SelectItem>
              <SelectItem value="employment_impact">Employment Impact</SelectItem>
            </SelectContent>
          </Select>

          <Select value={chartType} onValueChange={(value) => setChartType(value as any)}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Chart type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="projection">Projection</SelectItem>
              <SelectItem value="distribution">Uncertainty</SelectItem>
              <SelectItem value="equity">Equity Impact</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardHeader>
      <CardContent className="h-[500px]">
        <Tabs value={chartType}>
          <TabsContent value="projection">{renderProjectionChart()}</TabsContent>
          <TabsContent value="distribution">{renderDistributionChart()}</TabsContent>
          <TabsContent value="equity">{renderEquityChart()}</TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default PolicyChart;
