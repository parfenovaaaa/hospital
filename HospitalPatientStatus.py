from DialogWithUser import DialogWithUser
from PatientsDB import PatientsDB


def patient_status_up() -> None:
    try:
        index = DialogWithUser.get_patient_id() - 1
        if PatientsDB().can_make_status_up(index):
            PatientsDB().make_patient_status_up(index)
            DialogWithUser.send_msg_to_user(f"Новый статус пациента: '{PatientsDB().get_patient_status_by_id(index)}'")
        else:
            if DialogWithUser.ask_discharge_patient():
                PatientsDB().discharge_patient_by_id(index)
                DialogWithUser.send_msg_to_user(f"Пациент выписан из больницы")
            else:
                status = PatientsDB().get_patient_status_by_id(index)
                DialogWithUser.send_msg_to_user(f"Пациент остался в статусе '{status}'")
    except (TypeError, ValueError):
        DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
        return
    except IndexError:
        DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
        return


class HospitalPatientStatus:
    @staticmethod
    def get_patient_status():
        try:
            index = DialogWithUser.get_patient_id()
            DialogWithUser.send_msg_to_user(f"Статус пациента: '{PatientsDB().get_patient_status_by_id(index)}'")
        except (TypeError, ValueError):
            DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
            return
        except IndexError:
            DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
            return

    @staticmethod
    def patient_status_down() -> None:
        try:
            patient_index = DialogWithUser.get_patient_id() - 1
            if PatientsDB().can_make_status_down(patient_index):
                PatientsDB().make_patient_status_down(patient_index)
                status = PatientsDB().get_patient_status_by_id(patient_index)
                DialogWithUser.send_msg_to_user(f"Новый статус пациента: '{status}'")
            else:
                DialogWithUser.send_msg_to_user("Ошибка. Нельзя понизить самый низкий статус(наши пациенты не умирают)")
        except (TypeError, ValueError):
            DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
            return
        except IndexError:
            DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
            return

    @staticmethod
    def patient_discharge(patient_id=None) -> None:
        try:
            patient_index = patient_id if patient_id else DialogWithUser.get_patient_id() - 1
            PatientsDB().discharge_patient_by_id(patient_index)
            DialogWithUser.send_msg_to_user(f"Пациент выписан из больницы")
        except (TypeError, ValueError):
            DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
            return
        except IndexError:
            DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
            return
