from DialogWithUser import DialogWithUser
from HospitalPatientStatus import HospitalPatientStatus, patient_status_up
from HospitalStatistics import HospitalStatistics
from constants import STATISTICS_COMMANDS, COMMANDS, STOP_COMMANDS
from constants import STATUS_UP_COMMANDS, STATUS_DOWN_COMMANDS, DISCHARGE_COMMANDS, \
    GET_STATUS_COMMANDS


class HospitalPatientAccounting:

    @staticmethod
    def start_hospital_accounting() -> None:
        while True:
            command = DialogWithUser.get_msg_from_user("Введите команду:")
            if command in STOP_COMMANDS:
                DialogWithUser.send_msg_to_user("Сеанс завершён")
                break
            elif command not in COMMANDS:
                DialogWithUser.send_msg_to_user("Неизвестная команда! Попробуйте еще раз!")
            elif command in STATISTICS_COMMANDS:
                HospitalStatistics().calculate_statistics()
            if command in GET_STATUS_COMMANDS:
                HospitalPatientStatus().get_patient_status()
            elif command in STATUS_UP_COMMANDS:
                patient_status_up()
            elif command in STATUS_DOWN_COMMANDS:
                HospitalPatientStatus().patient_status_down()
            elif command in DISCHARGE_COMMANDS:
                HospitalPatientStatus().patient_discharge()

