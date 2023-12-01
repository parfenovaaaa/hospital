
from unittest.mock import patch

import pytest

from main import HospitalPatientAccounting


@pytest.fixture(autouse=True)
def clear_db():
    HospitalPatientAccounting.patients_db = [1 for i in range(0, 200)]


@patch('builtins.print')
class TestsStatusDown:
    def test_status_down_new_status(self, mock_get):
        expected_msg = "Новый статус пациента: 'Тяжело болен'"
        patient_id = 1
        hpa = HospitalPatientAccounting()
        hpa.patient_status_down(patient_id)
        assert mock_get.call_args_list[0][0][0] == expected_msg

    def test_status_down_status_error(self, mock_get):
        expected_msg = "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)"
        patient_id = 1
        hpa = HospitalPatientAccounting()
        hpa.patient_status_down(patient_id)
        hpa.patient_status_down(patient_id)
        assert mock_get.call_args_list[1][0][0] == expected_msg


class TestsCalculateStatistics:
    def test_calculate_statistics_all_parients(self):
        with patch('builtins.print') as mock_get:
            expected_msg = "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Болен': 200 чел."
            hpa = HospitalPatientAccounting()
            hpa.calculate_statistics()
            actual_msg = ""
            for i in range(len(mock_get.call_args_list)):
                actual_msg = actual_msg + mock_get.call_args_list[i][0][0]
            assert expected_msg == actual_msg

    @pytest.mark.parametrize("data", [
        [0, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Тяжело болен': 1 чел." + "\tв статусе 'Болен': 199 чел."],
        [2, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Болен': 199 чел." + "\tв статусе 'Слегка болен': 1 чел."],
        [3, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Болен': 199 чел." + "\tв статусе 'Готов к выписке': 1 чел."],
    ])
    def test_calculate_statistics_3(self, data):
        with patch('builtins.print') as mock_get:
            hpa = HospitalPatientAccounting()
            hpa.patients_db[1], expected_msg = data
            hpa.calculate_statistics()
            actual_msg = ""
            for i in range(len(mock_get.call_args_list)):
                actual_msg = actual_msg + mock_get.call_args_list[i][0][0]
            assert expected_msg == actual_msg


    @pytest.mark.parametrize("data", [
        [0, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Тяжело болен': 2 чел." + "\tв статусе 'Болен': 198 чел."],
        [2, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Тяжело болен': 1 чел." + "\tв статусе 'Болен': 198 чел." + "\tв статусе 'Слегка болен': 1 чел."],
        [3, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Тяжело болен': 1 чел." + "\tв статусе 'Болен': 198 чел." + "\tв статусе 'Готов к выписке': 1 чел."],
    ])
    def test_calculate_statistics_23(self, data):
        with patch('builtins.print') as mock_get:
            hpa = HospitalPatientAccounting()
            hpa.patients_db[0] = 0
            hpa.patients_db[1], expected_msg = data
            hpa.calculate_statistics()
            actual_msg = ""
            for i in range(len(mock_get.call_args_list)):
                actual_msg = actual_msg + mock_get.call_args_list[i][0][0]
            assert expected_msg == actual_msg


    @pytest.mark.parametrize("data", [
        [0, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Тяжело болен': 3 чел." + "\tв статусе 'Болен': 197 чел."],
        [2, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Тяжело болен': 2 чел." + "\tв статусе 'Болен': 197 чел." + "\tв статусе 'Слегка болен': 1 чел."],
        [3, "В больнице сейчас 200 чел., из них:" + "\tв статусе 'Тяжело болен': 2 чел." + "\tв статусе 'Болен': 197 чел." + "\tв статусе 'Готов к выписке': 1 чел."],
    ])
    def test_calculate_statistics_3(self, data):
        with patch('builtins.print') as mock_get:
            hpa = HospitalPatientAccounting()
            hpa.patients_db[0] = 0
            hpa.patients_db[2] = 0
            hpa.patients_db[1], expected_msg = data
            hpa.calculate_statistics()
            actual_msg = ""
            for i in range(len(mock_get.call_args_list)):
                actual_msg = actual_msg + mock_get.call_args_list[i][0][0]
            assert expected_msg == actual_msg

    @pytest.mark.parametrize("data", [
        [1, "В больнице сейчас 199 чел., из них:" + "\tв статусе 'Болен': 199 чел."],
        [30, "В больнице сейчас 170 чел., из них:" + "\tв статусе 'Болен': 170 чел."],
        [75, "В больнице сейчас 125 чел., из них:" + "\tв статусе 'Болен': 125 чел."],
    ])
    @patch('builtins.print')
    def test_calculate_statistics_dicharged(self, mock_get, data):
        to_del, expected_msg = data
        hpa = HospitalPatientAccounting()
        [hpa.patients_db.pop(1) for i in range(to_del)]
        hpa.calculate_statistics()
        actual_msg = ""
        for i in range(len(mock_get.call_args_list)):
            actual_msg = actual_msg + mock_get.call_args_list[i][0][0]
        assert expected_msg == actual_msg

    @patch('builtins.print')
    def test_calculate_statistics_clear_db(self, mock_get):
        expected_msg = "В больнице сейчас 0 чел., из них:"
        hpa = HospitalPatientAccounting()
        hpa.patients_db.clear()
        hpa.calculate_statistics()
        actual_msg = ""
        for i in range(len(mock_get.call_args_list)):
            actual_msg = actual_msg + mock_get.call_args_list[i][0][0]
        assert expected_msg == actual_msg

