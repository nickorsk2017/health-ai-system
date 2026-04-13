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
    | "pulmonology";

  type CreateVisit = {
    user_id: string;
    doctor_type: DoctorType;
    visit_at: string;
    subjective: string;
    objective: string;
    assessment: string;
    plan: string;
  };

  type VisitRecord = {
    visit_id: string;
    user_id: string;
    doctor_type: string;
    visit_at: string;
    subjective: string;
    objective: string;
    assessment: string;
    plan: string;
    created_at: string;
  };

  type RecordVisitResponse = {
    success: boolean;
    visit_id: string;
  };
}
