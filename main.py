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

PATIENT_DB = [1 for i in range(0, 200)]


def calculate_statistics() -> None:
    counter = Counter(PATIENT_DB)
    print(f"В больнице сейчас {len(PATIENT_DB)} чел., из них:")
    [print(f"в статусе '{PATIENT_STATUS[i]}': {counter[i]} чел.") for i in range(0, 4) if counter[i] > 0]


def patient_status_execute(command: str, patient_id: int) -> None:
    new_patient_status_msg = "Новый статус пациента: '{}'"
    patient_status = PATIENT_DB[patient_id]

    if command in GET_STATUS_COMMANDS:
        print(f"Статус пациента: '{PATIENT_STATUS[patient_status]}'")
    elif command in STATUS_UP_COMMANDS:
        if patient_status == 3:
            print("Выписать пациента? (да/нет)")
            result = input()
            no_change_msg = f"Пациент остался в статусе '{PATIENT_STATUS[PATIENT_DB[patient_id]]}'"
            patient_discharge(patient_id) if result in YES_COMMANDS else print(no_change_msg)
        else:
            PATIENT_DB[patient_id] = PATIENT_DB[patient_id] + 1
            print(new_patient_status_msg.format(PATIENT_STATUS[PATIENT_DB[patient_id]]))
    elif command in STATUS_DOWN_COMMANDS:
        if patient_status == 0:
            print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
        else:
            PATIENT_DB[patient_id] = PATIENT_DB[patient_id] - 1
            print(new_patient_status_msg.format(PATIENT_STATUS[PATIENT_DB[patient_id]]))
    elif command in DISCHARGE_COMMANDS:
        patient_discharge(patient_id)


def patient_discharge(patient_id: int) -> None:
        PATIENT_DB.pop(patient_id)
        print(f"Пациент выписан")


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


def execute_command(command: str) -> None:
    if command not in COMMANDS:
        print("Неизвестная команда! Попробуйте еще раз!")
    elif command in STATISTICS_COMMANDS:
        calculate_statistics()
    else:
        try:
            patient_id = get_patient_id()
        except ValueError:
            print("Ошибка! ID пациента должно быть числом(целым и положительным)")
            return
        except AssertionError:
            print("Ошибка! Нет пациента с таким ID")
            return
        patient_status_execute(command, patient_id)


def start_hospital():
    while True:
        print("Введите команду:")
        command = input()
        exit() if command in STOP_COMMANDS else execute_command(command)


if __name__ == '__main__':
    start_hospital()
