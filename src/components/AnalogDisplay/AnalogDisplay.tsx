import React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import Plot from "react-plotly.js"

export function AnalogDisplay() {
  const data = [
    {
      type: "indicator",
      mode: "gauge+number",
      value: 42,
      title: { text: "Policy Impact Score" },
      gauge: {
        axis: { range: [0, 100] },
        steps: [
          { range: [0, 25], color: "lightgray" },
          { range: [25, 50], color: "gray" },
          { range: [50, 75], color: "lightblue" },
          { range: [75, 100], color: "blue" }
        ]
      }
    }
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Policy Impact Visualization</CardTitle>
      </CardHeader>
      <CardContent>
        <Plot
          data={data}
          layout={{ width: 400, height: 300 }}
          config={{ displayModeBar: false }}
        />
      </CardContent>
    </Card>
  )
}
