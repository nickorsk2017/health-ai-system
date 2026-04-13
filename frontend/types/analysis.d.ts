declare namespace Entity {
  type CreateAnalysis = {
    user_id: string;
    analysis: string;
    date: string;
  };

  type AnalysisRecord = {
    user_id: string;
    analysis: string;
    date: string;
    created_at: string;
  };

  type RecordAnalysisResponse = {
    success: boolean;
  };
}
