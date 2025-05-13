import { PolicyInput } from "@/components/PolicyInput/PolicyInput"
import { AnalogDisplay } from "@/components/AnalogDisplay/AnalogDisplay"
import { SimulationResults } from "@/components/SimulationResults/SimulationResults"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

function App() {
  return (
    <div className="container mx-auto p-4 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>PolicySonar Dashboard</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <PolicyInput />
            <AnalogDisplay />
          </div>
          <SimulationResults />
        </CardContent>
      </Card>
    </div>
  )
}

export default App
