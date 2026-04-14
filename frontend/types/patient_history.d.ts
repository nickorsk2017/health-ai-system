declare namespace Entity {
  type DoctorType =
    | "oncology"
    | "gastroenterology"
    | "cardiology"
    | "hematology"
    | "nephrology"
    | "nutrition"
    | "endocrinology"
    | "mental_health"
    | "pulmonology"
    | "general_practitioner";

  type CreatePatientHistory = {
    user_id: string;
    doctor_type: DoctorType;
    history_date: string;
    subjective: string;
    objective: string;
    assessment: string;
    plan: string;
  };

  type PatientHistoryRecord = {
    history_id: string;
    user_id: string;
    doctor_type: string;
    history_date: string;
    subjective: string;
    objective: string;
    assessment: string;
    plan: string;
    created_at: string;
  };

  type RecordPatientHistoryResponse = {
    success: boolean;
    history_id: string;
  };

  type HistoryFromPromptRequest = {
    user_id: string;
    prompt: string;
  };

  type HistoryFromPromptResponse = {
    success: boolean;
    count: number;
  };

  type UpdatePatientHistory = {
    history_date: string;
    subjective: string;
    objective: string;
    assessment: string;
    plan: string;
  };

  type MutatePatientHistoryResponse = {
    success: boolean;
  };
}
