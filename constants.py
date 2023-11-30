GET_STATUS_COMMANDS = ["get status", "узнать статус пациента", "1"]
STATUS_UP_COMMANDS = ["status up", "повысить статус пациента", "2"]
STATUS_DOWN_COMMANDS = ["status down", "понизить статус пациента", "3"]
DISCHARGE_COMMANDS = ["discharge", "выписать пациента", "4"]
STATISTICS_COMMANDS = ["calculate statistics", "рассчитать статистику", "5"]
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

NEW_PATIENT_STATUS_MSG = "Новый статус пациента: '{}'"
