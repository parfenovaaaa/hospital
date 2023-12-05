from typing import Union

from DialogWithUser import DialogWithUser
from HospitalPatientStatus import HospitalPatientStatus
from HospitalStatistics import HospitalStatistics
from constants import STATISTICS_COMMANDS, COMMANDS, STOP_COMMANDS


class HospitalPatientAccounting:

    def __init__(self, patients_db=None):
        self.patients_db = patients_db if patients_db else [1 for _ in range(0, 200)]

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
            HospitalPatientStatus(self.patients_db).patient_status_execute(command, patient_id) if patient_id else None

    @staticmethod
    def shut_down_hospital_accounting() -> None:
        DialogWithUser.send_msg_to_user("Сеанс завершён")
        exit()

    def start_hospital_accounting(self) -> None:
        while True:
            command = DialogWithUser.get_msg_from_user("Введите команду:")
            self.shut_down_hospital_accounting() if command in STOP_COMMANDS else self.execute_command(command)
