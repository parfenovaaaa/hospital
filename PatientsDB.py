from collections import Counter
from typing import Dict

from constants import DB_SIZE, PATIENT_STATUS


class PatientsDB:
    patients_db = [1 for _ in range(0, DB_SIZE)]

    def get_patient_status_by_id(self, patient_id) -> int:
        return PATIENT_STATUS[self.patients_db[patient_id - 1]]

    def can_make_status_up(self, patient_id) -> bool:
        if self.patients_db[patient_id - 1] == 3:
            return False
        else:
            return True

    def make_patient_status_up(self, patient_id):
        patient_index = patient_id - 1
        self.patients_db[patient_index] = self.patients_db[patient_index] + 1

    def can_make_status_down(self, patient_id) -> bool:
        if self.patients_db[patient_id - 1] == 0:
            return False
        else:
            return True

    def make_patient_status_down(self, patient_id):
        patient_index = patient_id - 1
        self.patients_db[patient_index] = self.patients_db[patient_index] - 1

    def discharge_patient_by_id(self, patient_id):
        self.patients_db.pop(patient_id - 1)

    def get_calculate_statistics_data(self) -> Dict:
        return {"statistics": Counter(self.patients_db), "patients_amount": len(self.patients_db)}
