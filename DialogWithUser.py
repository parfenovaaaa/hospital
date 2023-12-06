from typing import Union

from PatientIdError import PatientIdError
from constants import YES_COMMANDS


class DialogWithUser:
    @staticmethod
    def get_msg_from_user(msg_to_user: str) -> str:
        command = input(msg_to_user)
        return command

    @staticmethod
    def send_msg_to_user(msg: str) -> None:
        print(msg)

    @staticmethod
    def get_patient_id() -> Union[int, None]:
        try:
            patient_id = int(DialogWithUser.get_msg_from_user("Введите ID пациента:"))
            if patient_id <= 0:
                raise PatientIdError(value_error=True)
            else:
                return patient_id
        except ValueError:
            raise PatientIdError(value_error=True)

    @staticmethod
    def ask_discharge_patient():
        result = input("Выписать пациента? (да/нет)")
        if result in YES_COMMANDS:
            return True
        else:
            return False
