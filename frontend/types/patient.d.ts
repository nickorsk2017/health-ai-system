declare namespace Entity {
  type Gender = "male" | "female" | "other";

  type MockPatient = {
    id: string;
    name: string;
    date_of_birth?: string;
    gender?: Gender;
  };

  type NewPatientForm = {
    name: string;
    date_of_birth: string;
    gender: Gender;
  };
}
