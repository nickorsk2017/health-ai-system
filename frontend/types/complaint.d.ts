declare namespace Entity {
  type ComplaintStatus = "unread" | "read" | "appointment";

  type Complaint = {
    complaint_id: string;
    user_id: string;
    problem_health: string;
    date_public: string;
    status: ComplaintStatus;
    created_at: string;
  };

  type CreateComplaint = {
    problem_health: string;
    date_public: string;
  };

  type UpdateComplaint = {
    problem_health: string;
    date_public: string;
  };

  type ComplaintByPromptRequest = {
    user_id: string;
    prompt: string;
  };
}
