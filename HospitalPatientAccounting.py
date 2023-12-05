from typing import Union

from DialogWithUser import DialogWithUser
from HospitalStatistics import HospitalStatistics
from constants import PATIENT_STATUS, STATUS_UP_COMMANDS, YES_COMMANDS, STATUS_DOWN_COMMANDS, DISCHARGE_COMMANDS, \
    GET_STATUS_COMMANDS, STATISTICS_COMMANDS, COMMANDS, STOP_COMMANDS, NEW_PATIENT_STATUS_MSG, STATUS_DOWN_ERROR_MSG


class HospitalPatientAccounting:

    def __init__(self, patients_db=None):
        self.patients_db = patients_db if patients_db else [1 for _ in range(0, 200)]

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

    @staticmethod
    def get_patient_id() -> Union[int, None]:
        try:
            patient_id = int(DialogWithUser.get_msg_from_user("Введите ID пациента:"))
            if patient_id <= 0:
                raise ValueError
            elif patient_id > 200:
                DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
                return
            else:
                return patient_id
        except ValueError:
            DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
            return

    def execute_command(self, command: str) -> None:
        if command not in COMMANDS:
            DialogWithUser.send_msg_to_user("Неизвестная команда! Попробуйте еще раз!")
        elif command in STATISTICS_COMMANDS:
            HospitalStatistics(self.patients_db).calculate_statistics()
        else:
            patient_id = self.get_patient_id()
            self.patient_status_execute(command, patient_id) if patient_id else None

    @staticmethod
    def shut_down_hospital_accounting() -> None:
        DialogWithUser.send_msg_to_user("Сеанс завершён")
        exit()

    def start_hospital_accounting(self) -> None:
        while True:
            command = DialogWithUser.get_msg_from_user("Введите команду:")
            self.shut_down_hospital_accounting() if command in STOP_COMMANDS else self.execute_command(command)
