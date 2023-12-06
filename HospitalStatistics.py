from collections import Counter
from DialogWithUser import DialogWithUser
from PatientsDB import PatientsDB
from constants import PATIENT_STATUS


class HospitalStatistics:

    def calculate_statistics(self) -> None:
        raw_data = PatientsDB().get_calculate_statistics_data()
        strings = self._create_calculate_statistics_output(raw_data["statistics"], raw_data["patients_amount"])
        DialogWithUser.send_msg_to_user(strings)

    @staticmethod
    def _create_calculate_statistics_output(counter: Counter, patient_count: int) -> str:
        count_list = [f"\n\tв статусе '{PATIENT_STATUS[i]}': {counter[i]} чел." for i in range(0, 4) if counter[i] > 0]
        return f"В больнице сейчас {patient_count} чел., из них:" + "".join(count_list)
