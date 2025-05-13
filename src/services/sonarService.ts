import apiClient from "./api";

export interface AnalysisResult {
  analysis: {
    summary: string;
    sentiment: string;
    key_entities: string[];
  };
  historical_matches: Array<{
    text: string;
    similarity: number;
    outcomes: {
      economic_impact: string;
      employment_change: string;
    };
  }>;
}

export const sonarService = {
  async analyzePolicy(policyText: string): Promise<AnalysisResult> {
    const response = await apiClient.post("/analyze", { text: policyText });
    return response.data;
  },

  async getHistoricalMatches(policyId: string): Promise<AnalysisResult['historical_matches']> {
    const response = await apiClient.get(`/policies/${policyId}/history`);
    return response.data;
  }
};
