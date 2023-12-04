from collections import Counter
from typing import Dict

from DialogWithUser import DialogWithUser
from constants import PATIENT_STATUS


class HospitalStatistics:
    def __init__(self, patients_db=None):
        self.patients_db = patients_db if patients_db else []

    def calculate_statistics(self) -> None:
        raw_data = self._get_calculate_statistics_data()
        strings = self._create_calculate_statistics_output(raw_data["statistics"], raw_data["patients_amount"])
        DialogWithUser.send_msg_to_user(strings)

    def _get_calculate_statistics_data(self) -> Dict:
        return {"statistics": Counter(self.patients_db), "patients_amount": len(self.patients_db)}

    @staticmethod
    def _create_calculate_statistics_output(counter: Counter, patient_count: int) -> str:
        count_list = [f"\n\tв статусе '{PATIENT_STATUS[i]}': {counter[i]} чел." for i in range(0, 4) if counter[i] > 0]
        return f"В больнице сейчас {patient_count} чел., из них:" + "".join(count_list)
