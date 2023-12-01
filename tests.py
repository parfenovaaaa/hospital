import pytest

from constants import NEW_PATIENT_STATUS_MSG, PATIENT_STATUS, STATUS_DOWN_ERROR_MSG
from main import HospitalPatientAccounting, HospitalStatistics


class TestsStatusDown:
    patient_id = 1
    hpa = HospitalPatientAccounting()

    def test_status_down_complete(self):
        actual_msg = self.hpa.patient_status_down(self.patient_id)
        assert NEW_PATIENT_STATUS_MSG.format(PATIENT_STATUS[0]) == actual_msg
        assert self.hpa.patients_db[1] == 0

    def test_status_down_error(self):
        self.hpa.patient_status_down(self.patient_id)
        actual_msg = self.hpa.patient_status_down(self.patient_id)
        assert STATUS_DOWN_ERROR_MSG == actual_msg
        assert self.hpa.patients_db[1] == 0


class TestsCalculateStatistics:
    hs = HospitalStatistics()

    all_patients_data_template = "В больнице сейчас 200 чел., из них:\n\tв статусе '{}': 200 чел."
    two_patients_data_template = (
            "В больнице сейчас 200 чел., из них:\n\tв статусе 'Тяжело болен': 1 чел."
            "\n\tв статусе 'Болен': 198 чел.\n\tв статусе '{}': 1 чел."
    )

    @pytest.fixture(autouse=True)
    def clear_db(self):
        self.hs.patients_db = [1 for _ in range(0, 200)]

    @pytest.mark.parametrize(
        "all_patients_data",
        [
            [0, all_patients_data_template.format(PATIENT_STATUS[0])],
            [1, all_patients_data_template.format(PATIENT_STATUS[1])],
            [2, all_patients_data_template.format(PATIENT_STATUS[2])],
            [3, all_patients_data_template.format(PATIENT_STATUS[3])]
        ],
    )
    def test_all_patient_statistics(self, all_patients_data):
        status, expected_msg = all_patients_data
        self.hs.patients_db = [status for _ in range(0, 200)]
        actual_msg = self.hs.calculate_statistics()
        assert expected_msg == actual_msg

    @pytest.mark.parametrize(
        "two_patients_data",
        [[2, two_patients_data_template.format(PATIENT_STATUS[2])], [3, two_patients_data_template.format(PATIENT_STATUS[3])]],
    )
    def test_statistics_with_change_status(self, two_patients_data):
        self.hs.patients_db[0] = 0
        self.hs.patients_db[1], expected_msg = two_patients_data
        actual_msg = self.hs.calculate_statistics()
        assert expected_msg == actual_msg

    def test_statistics_all_status(self):
        expected_msg = (
            "В больнице сейчас 200 чел., из них:\n\tв статусе 'Тяжело болен': 1 чел.\n\tв статусе 'Болен': 197 чел."
            "\n\tв статусе 'Слегка болен': 1 чел.\n\tв статусе 'Готов к выписке': 1 чел."
        )
        self.hs.patients_db[0] = 0
        self.hs.patients_db[1] = 2
        self.hs.patients_db[2] = 3
        actual_msg = self.hs.calculate_statistics()
        assert expected_msg == actual_msg

    def test_statistics_with_clear_db(self):
        expected_msg = "В больнице сейчас 0 чел., из них:"
        self.hs.patients_db.clear()
        actual_msg = self.hs.calculate_statistics()
        assert expected_msg == actual_msg
