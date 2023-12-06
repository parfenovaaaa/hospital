from typing import Union

from constants import YES_COMMANDS, DB_SIZE


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
        patient_id = int(DialogWithUser.get_msg_from_user("Введите ID пациента:"))
        if patient_id <= 0:
            raise ValueError
        elif patient_id > DB_SIZE:
            raise IndexError
        else:
            return patient_id

    @staticmethod
    def ask_discharge_patient():
        result = input("Выписать пациента? (да/нет)")
        if result in YES_COMMANDS:
            return True
        else:
            return False
