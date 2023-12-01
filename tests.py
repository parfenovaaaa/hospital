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

    two_patients_data_template = (
            "В больнице сейчас 200 чел., из них:\n\tв статусе 'Тяжело болен': 1 чел."
            "\n\tв статусе 'Болен': 198 чел.\n\tв статусе '{}': 1 чел."
    )

    @pytest.fixture(autouse=True)
    def clear_db(self):
        self.hs.patients_db = [1 for _ in range(0, 200)]

    @pytest.mark.parametrize("status", [0, 1, 2, 3])
    def test_statistics_same_status(self, status):
        expected_msg = f"В больнице сейчас 200 чел., из них:\n\tв статусе '{PATIENT_STATUS[status]}': 200 чел."
        self.hs.patients_db = [status for _ in range(0, 200)]
        actual_msg = self.hs.calculate_statistics()
        assert expected_msg == actual_msg

    @pytest.mark.parametrize("status", [2, 3], )
    def test_statistics_with_two_status(self, status):
        expected_msg = (
            "В больнице сейчас 200 чел., из них:\n\tв статусе 'Тяжело болен': 1 чел."
            f"\n\tв статусе 'Болен': 198 чел.\n\tв статусе '{PATIENT_STATUS[status]}': 1 чел."
        )
        self.hs.patients_db[0] = 0
        self.hs.patients_db[1] = status
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

    @pytest.mark.parametrize("count", [30, 100, 128])
    def test_statistics_patients_count(self, count):
        actual_count = 200 - count
        expected_msg = f"В больнице сейчас {actual_count} чел., из них:\n\tв статусе 'Болен': {actual_count} чел."
        [self.hs.patients_db.pop(1) for _ in range(count)]
        actual_msg = self.hs.calculate_statistics()
        assert expected_msg == actual_msg
        assert actual_count == len(self.hs.patients_db)

    def test_statistics_with_clear_db(self):
        expected_msg = "В больнице сейчас 0 чел., из них:"
        self.hs.patients_db.clear()
        actual_msg = self.hs.calculate_statistics()
        assert expected_msg == actual_msg
