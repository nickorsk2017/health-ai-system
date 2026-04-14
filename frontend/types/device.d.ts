declare namespace Entity {
  type DeviceType = "apple_health" | "oura_ring";

  type Device = {
    id: string;
    user_id: string;
    type_device: DeviceType;
    diagnosis_mock: string | null;
    created_at: string;
    last_sync: string | null;
  };

  type AddDeviceForm = {
    type_device: DeviceType;
    diagnosis_mock: string;
  };

  type AddDeviceResponse = {
    success: boolean;
    device_id: string;
  };
}
