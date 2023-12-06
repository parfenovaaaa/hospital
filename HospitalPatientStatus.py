from DialogWithUser import DialogWithUser
from PatientsDB import PatientsDB


def patient_status_up() -> None:
    try:
        patient_id = DialogWithUser.get_patient_id()
        if PatientsDB().can_make_status_up(patient_id):
            PatientsDB().make_patient_status_up(patient_id)
            status = PatientsDB().get_patient_status_by_id(patient_id)
            DialogWithUser.send_msg_to_user(f"Новый статус пациента: '{status}'")
        else:
            if DialogWithUser.ask_discharge_patient():
                PatientsDB().discharge_patient_by_id(patient_id)
                DialogWithUser.send_msg_to_user(f"Пациент выписан из больницы")
            else:
                status = PatientsDB().get_patient_status_by_id(patient_id)
                DialogWithUser.send_msg_to_user(f"Пациент остался в статусе '{status}'")
    except ValueError:
        DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
        return
    except IndexError:
        DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
        return


class HospitalPatientStatus:
    @staticmethod
    def get_patient_status():
        try:
            patient_id = DialogWithUser.get_patient_id()
            DialogWithUser.send_msg_to_user(f"Статус пациента: '{PatientsDB().get_patient_status_by_id(patient_id)}'")
        except ValueError:
            DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
            return
        except IndexError:
            DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
            return

    @staticmethod
    def patient_status_down() -> None:
        try:
            patient_id = DialogWithUser.get_patient_id()
            if PatientsDB().can_make_status_down(patient_id):
                PatientsDB().make_patient_status_down(patient_id)
                status = PatientsDB().get_patient_status_by_id(patient_id)
                DialogWithUser.send_msg_to_user(f"Новый статус пациента: '{status}'")
            else:
                DialogWithUser.send_msg_to_user("Ошибка. Нельзя понизить самый низкий статус(наши пациенты не умирают)")
        except ValueError:
            DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
            return
        except IndexError:
            DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
            return

    @staticmethod
    def patient_discharge(patient_id=None) -> None:
        try:
            patient_id = patient_id if patient_id else DialogWithUser.get_patient_id()
            PatientsDB().discharge_patient_by_id(patient_id)
            DialogWithUser.send_msg_to_user(f"Пациент выписан из больницы")
        except ValueError:
            DialogWithUser.send_msg_to_user("Ошибка! ID пациента должно быть числом(целым и положительным)")
            return
        except IndexError:
            DialogWithUser.send_msg_to_user("Ошибка! Нет пациента с таким ID")
            return
