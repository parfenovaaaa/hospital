from collections import Counter

GET_STATUS_COMMANDS = ["get status", "узнать статус", "1"]
STATUS_UP_COMMANDS = ["status up", "повысить статус", "2"]
STATUS_DOWN_COMMANDS = ["status down", "понизить статус", "3"]
DISCHARGE_COMMANDS = ["discharge", "выписать", "4"]
STATISTICS_COMMANDS = ["calculate statistics", "посчитать статистику", "5"]
STOP_COMMANDS = ["stop", "стоп"]
COMMANDS = (
        GET_STATUS_COMMANDS + STATUS_UP_COMMANDS + STATUS_DOWN_COMMANDS + DISCHARGE_COMMANDS + STATISTICS_COMMANDS
)
YES_COMMANDS = ["yes", "y", "да"]

PATIENT_STATUS = {
    0: "Тяжело болен",
    1: "Болен",
    2: "Слегка болен",
    3: "Готов к выписке",
}


class HospitalPatientAccounting:
    patients_db = [1 for i in range(0, 200)]

    def calculate_statistics(self) -> None:
        counter = Counter(self.patients_db)
        print(f"В больнице сейчас {len(self.patients_db)} чел., из них:")
        [print(f"\tв статусе '{PATIENT_STATUS[i]}': {counter[i]} чел.") for i in range(0, 4) if counter[i] > 0]

    def patient_status_execute(self, command: str, patient_id: int) -> None:
        new_patient_status_msg = "Новый статус пациента: '{}'"
        patient_status = self.patients_db[patient_id]

        if command in GET_STATUS_COMMANDS:
            print(f"Статус пациента: '{PATIENT_STATUS[patient_status]}'")
        elif command in STATUS_UP_COMMANDS:
            if patient_status == 3:
                print("Выписать пациента? (да/нет)")
                result = input()
                no_change_msg = f"Пациент остался в статусе '{PATIENT_STATUS[self.patients_db[patient_id]]}'"
                self.patient_discharge(patient_id) if result in YES_COMMANDS else print(no_change_msg)
            else:
                self.patients_db[patient_id] = self.patients_db[patient_id] + 1
                print(new_patient_status_msg.format(PATIENT_STATUS[self.patients_db[patient_id]]))
        elif command in STATUS_DOWN_COMMANDS:
            if patient_status == 0:
                print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
            else:
                self.patients_db[patient_id] = self.patients_db[patient_id] - 1
                print(new_patient_status_msg.format(PATIENT_STATUS[self.patients_db[patient_id]]))
        elif command in DISCHARGE_COMMANDS:
            self.patient_discharge(patient_id)

    def patient_discharge(self, patient_id: int) -> None:
        self.patients_db.pop(patient_id)
        print(f"Пациент выписан")

    @staticmethod
    def get_patient_id() -> int | None:
        print("Введите ID пациента:")
        patient_id = input()
        patient_id = int(patient_id)
        if patient_id <= 0:
            raise ValueError
        elif patient_id > 200:
            raise AssertionError
        else:
            return patient_id - 1

    def execute_command(self, command: str) -> None:
        if command not in COMMANDS:
            print("Неизвестная команда! Попробуйте еще раз!")
        elif command in STATISTICS_COMMANDS:
            self.calculate_statistics()
        else:
            try:
                patient_id = self.get_patient_id()
            except ValueError:
                print("Ошибка! ID пациента должно быть числом(целым и положительным)")
                return
            except AssertionError:
                print("Ошибка! Нет пациента с таким ID")
                return
            self.patient_status_execute(command, patient_id)

    def start_patient_accounting(self):
        while True:
            print("Введите команду:")
            command = input()
            exit() if command in STOP_COMMANDS else self.execute_command(command)


if __name__ == '__main__':
    hpa = HospitalPatientAccounting()
    hpa.start_patient_accounting()
