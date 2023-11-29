from collections import Counter

GET_STATUS_COMMANDS = ["Get status", "1"]
STATUS_UP_COMMANDS = ["status up", "2"]
STATUS_DOWN_COMMANDS = ["status down", "3"]
DISCHARGE_COMMANDS = ["discharge", "4"]
STATISTICS_COMMANDS = ["calculate statistics", "5"]
STOP_COMMANDS = ["stop"]
COMMANDS = (
        GET_STATUS_COMMANDS + STATUS_UP_COMMANDS + STATUS_DOWN_COMMANDS + DISCHARGE_COMMANDS + STATISTICS_COMMANDS + STOP_COMMANDS
)
YES_COMMANDS = ["yes", "y", "да"]

PATIENT_STATUS = {
    0: "Тяжело болен",
    1: "Болен",
    2: "Слегка болен",
    3: "Готов к выписке",
}

PATIENT_DB = [1 for i in range(0, 200)]


def check_patient_id(patient_id):
    patient_id = int(patient_id)
    if patient_id < 0:
        raise ValueError
    elif patient_id > 200:
        print("Ошибка! Нет пациента с таким ID")  #  TODO  а как прервать то
    else:
        return patient_id


def calculate_statistics():
    counter = Counter(PATIENT_DB)
    statistics = []
    [statistics.append(f"в статусе '{PATIENT_STATUS[i]}': {counter[i]} чел.") for i in range(0, 4) if counter[i] > 0]
    print(statistics)


def patient_status_execute(command):
    print("Please, input patient id:")
    patient_id = input()
    try:
        patient_id = check_patient_id(patient_id)
    except ValueError:
        print("Ошибка! ID пациента должно быть числом(целым и положительным)")
        return
    patient_status = PATIENT_DB[patient_id]
    if command in GET_STATUS_COMMANDS:
        print(f"Статус пациента: {PATIENT_STATUS[patient_status]}")
    elif command in STATUS_UP_COMMANDS:
        if patient_status == 3:
            print("Выписать пациента?")
            result = input()
            if result in YES_COMMANDS:
                patient_discharge(patient_id)
            else:
                print("Пациент остался в статусе ")
                return
        else:
            PATIENT_DB[patient_id] = PATIENT_DB[patient_id] + 1
            print(f"Новый ствтус {PATIENT_STATUS[PATIENT_DB[patient_id]]} ")
    elif command in STATUS_DOWN_COMMANDS:
        if patient_status == 0:
            print("Не может умиреть ")
        else:
            PATIENT_DB[patient_id] = PATIENT_DB[patient_id] - 1
            print(f"Новый ствтус {PATIENT_STATUS[PATIENT_DB[patient_id]]} ")
    elif command in DISCHARGE_COMMANDS:
        patient_discharge(patient_id)


def patient_discharge(patient_id):
        PATIENT_DB.pop(patient_id)
        print(f"Пациент выписан")


def execute_command(command: str):
    if command not in COMMANDS:
        print("Неизвестная команда! Попробуйте еще раз!")
    elif command in STATISTICS_COMMANDS:
        calculate_statistics()
    else:
        patient_status_execute(command)


def start_hospital():
    while True:
        print("Please, input command:")
        command = input()
        exit() if command in STOP_COMMANDS else execute_command(command)


if __name__ == '__main__':
    start_hospital()
