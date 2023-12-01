from unittest.mock import patch

import pytest

from constants import PATIENT_STATUS
from main import HospitalPatientAccounting


@patch('builtins.print')
class TestsStatusDown:
    hpa = HospitalPatientAccounting()
    patient_id = 1

    def test_status_down_complete(self, mock_get):
        expected_msg = "Новый статус пациента: 'Тяжело болен'"
        self.hpa.patient_status_down(self.patient_id)
        assert mock_get.call_args_list[0][0][0] == expected_msg
        assert self.hpa.patients_db[self.patient_id] == 0

    def test_status_down_error(self, mock_get):
        expected_msg = "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)"
        self.hpa.patient_status_down(self.patient_id)
        self.hpa.patient_status_down(self.patient_id)
        assert mock_get.call_args_list[1][0][0] == expected_msg
        assert self.hpa.patients_db[self.patient_id] == 0


class TestsCalculateStatistics:
    hpa = HospitalPatientAccounting()

    @pytest.fixture(autouse=True)
    def clear_db(self):
        self.hpa.patients_db = [1 for _ in range(0, 200)]

    @pytest.mark.parametrize("status", [0, 1, 2, 3])
    def test_statistics_same_status(self, status):
        with patch('builtins.print') as mock_get:
            expected_msg = f"В больнице сейчас 200 чел., из них:\tв статусе '{PATIENT_STATUS[status]}': 200 чел."
            self.hpa.patients_db = [status for _ in range(0, 200)]
            self.hpa.calculate_statistics()
            actual_msg = "".join([mock_get.call_args_list[i][0][0] for i in range(len(mock_get.call_args_list))])
            assert expected_msg == actual_msg

    @pytest.mark.parametrize("status, expected_msg", [
        [0, "В больнице сейчас 200 чел., из них:\tв статусе 'Тяжело болен': 1 чел.\tв статусе 'Болен': 199 чел."],
        [2, "В больнице сейчас 200 чел., из них:\tв статусе 'Болен': 199 чел.\tв статусе 'Слегка болен': 1 чел."],
        [3, "В больнице сейчас 200 чел., из них:\tв статусе 'Болен': 199 чел.\tв статусе 'Готов к выписке': 1 чел."],
    ])
    def test_statistics_one_different_status(self, status, expected_msg):
        with patch('builtins.print') as mock_get:
            self.hpa.patients_db[1], expected_msg = status, expected_msg
            self.hpa.calculate_statistics()
            actual_msg = "".join([mock_get.call_args_list[i][0][0] for i in range(len(mock_get.call_args_list))])
            assert expected_msg == actual_msg

    def test_statistics_all_status(self):
        with patch('builtins.print') as mock_get:
            expected_msg = (
                "В больнице сейчас 200 чел., из них:\tв статусе 'Тяжело болен': 1 чел.\tв статусе 'Болен': 197 чел."
                "\tв статусе 'Слегка болен': 1 чел.\tв статусе 'Готов к выписке': 1 чел."
            )
            self.hpa.patients_db[0] = 0
            self.hpa.patients_db[2] = 2
            self.hpa.patients_db[3] = 3
            self.hpa.calculate_statistics()
            actual_msg = "".join([mock_get.call_args_list[i][0][0] for i in range(len(mock_get.call_args_list))])
            assert expected_msg == actual_msg

    @pytest.mark.parametrize("status, expected_msg", [
        [1, "В больнице сейчас 199 чел., из них:\tв статусе 'Болен': 199 чел."],
        [30, "В больнице сейчас 170 чел., из них:\tв статусе 'Болен': 170 чел."],
        [75, "В больнице сейчас 125 чел., из них:\tв статусе 'Болен': 125 чел."],
    ])
    def test_statistics_patients_count(self, status, expected_msg):
        with patch('builtins.print') as mock_get:
            to_del, expected_msg = status, expected_msg
            [self.hpa.patients_db.pop(1) for _ in range(to_del)]
            self.hpa.calculate_statistics()
            actual_msg = "".join([mock_get.call_args_list[i][0][0] for i in range(len(mock_get.call_args_list))])
            assert expected_msg == actual_msg

    def test_statistics_clear_db(self):
        with patch('builtins.print') as mock_get:
            expected_msg = "В больнице сейчас 0 чел., из них:"
            self.hpa.patients_db.clear()
            self.hpa.calculate_statistics()
            actual_msg = "".join([mock_get.call_args_list[i][0][0] for i in range(len(mock_get.call_args_list))])
            assert expected_msg == actual_msg
