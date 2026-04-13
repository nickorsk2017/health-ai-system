declare namespace Entity {
  type CreateAnalysis = {
    user_id: string;
    analysis: string;
    date: string;
  };

  type AnalysisRecord = {
    analysis_id: string;
    user_id: string;
    analysis_text: string | null;
    analysis_date: string | null;
    created_at: string;
  };

  type UpdateAnalysis = {
    analysis_text: string | null;
    analysis_date: string | null;
  };

  type MutateAnalysisResponse = {
    success: boolean;
  };

  type RecordAnalysisResponse = {
    success: boolean;
  };

  type AnalysisByPromptRequest = {
    user_id: string;
    prompt: string;
  };

  type AnalysisByPromptResponse = {
    success: boolean;
    list_missing_analysis: string[];
  };
}
