from DialogWithUser import DialogWithUser
from constants import PATIENT_STATUS, STATUS_UP_COMMANDS, YES_COMMANDS, STATUS_DOWN_COMMANDS, DISCHARGE_COMMANDS, \
    GET_STATUS_COMMANDS, NEW_PATIENT_STATUS_MSG, STATUS_DOWN_ERROR_MSG


class HospitalPatientStatus:

    def __init__(self, patients_db=None):
        self.patients_db = patients_db if patients_db else []

    def patient_status_up(self, patient_id: int) -> None:
        patient_index = patient_id - 1
        if self.patients_db[patient_index] == 3:
            result = input("Выписать пациента? (да/нет)")
            no_change_msg = f"Пациент остался в статусе '{PATIENT_STATUS[self.patients_db[patient_index]]}'"
            self.patient_discharge(patient_index) if result in YES_COMMANDS else DialogWithUser.send_msg_to_user(no_change_msg)
        else:
            self.patients_db[patient_index] = self.patients_db[patient_index] + 1
            DialogWithUser.send_msg_to_user(self._create_status_changed_msg(patient_index))

    def patient_status_down(self, patient_id: int) -> None:
        patient_index = patient_id - 1
        if self.patients_db[patient_index] == 0:
            DialogWithUser.send_msg_to_user(self._patient_status_down_error())
        else:
            self._patient_status_down_execute(patient_index)
            DialogWithUser.send_msg_to_user(self._create_status_changed_msg(patient_index))

    @staticmethod
    def _patient_status_down_error() -> str:
        return STATUS_DOWN_ERROR_MSG

    def _patient_status_down_execute(self, patient_id: int) -> None:
        self.patients_db[patient_id] = self.patients_db[patient_id] - 1

    def _create_status_changed_msg(self, patient_id: int) -> str:
        return NEW_PATIENT_STATUS_MSG.format(PATIENT_STATUS[self.patients_db[patient_id]])

    def patient_status_execute(self, command: str, patient_id: int) -> None:
        if command in GET_STATUS_COMMANDS:
            DialogWithUser.send_msg_to_user(f"Статус пациента: '{PATIENT_STATUS[self.patients_db[patient_id - 1]]}'")
        elif command in STATUS_UP_COMMANDS:
            self.patient_status_up(patient_id)
        elif command in STATUS_DOWN_COMMANDS:
            self.patient_status_down(patient_id)
        elif command in DISCHARGE_COMMANDS:
            self.patient_discharge(patient_id)

    def patient_discharge(self, patient_id: int) -> None:
        self.patients_db.pop(patient_id - 1)
        DialogWithUser.send_msg_to_user(f"Пациент выписан из больницы")
