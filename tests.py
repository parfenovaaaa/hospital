from collections import Counter
from unittest.mock import MagicMock

from DialogWithUser import DialogWithUser
from HospitalStatistics import HospitalStatistics
from main import HospitalPatientAccounting


class TestsStatusDown:
    def test_status_down_complete(self):
        DialogWithUser.send_msg_to_user = MagicMock()
        hpa = HospitalPatientAccounting([3, 1, 3,])
        hpa.patient_status_down(patient_id=2)
        assert hpa.patients_db == [3, 0, 3]
        DialogWithUser.send_msg_to_user.assert_called_with("Новый статус пациента: 'Тяжело болен'")

    def test_status_down_error(self):
        DialogWithUser.send_msg_to_user = MagicMock()
        hpa = HospitalPatientAccounting([1, 0, 1,])
        hpa.patient_status_down(patient_id=2)
        assert hpa.patients_db == [1, 0, 1]
        DialogWithUser.send_msg_to_user.assert_called_with(
            "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)"
        )


class TestsCalculateStatistics:
    def test_statistics_raw_data(self):
        hs = HospitalStatistics([2, 2, 3, 0])
        raw_data = hs._get_calculate_statistics_data()
        assert raw_data["patients_amount"] == 4
        assert dict(raw_data["statistics"]) == {0: 1, 2: 2, 3: 1}

    def test_statistics_output(self):
        expected_statistics = {0: 1, 1: 2, 3: 1}
        expected_amount = 4
        hs = HospitalStatistics([1, 1, 3, 0])
        actual_msg = hs._create_calculate_statistics_output(Counter(expected_statistics), expected_amount)
        assert actual_msg.replace("\n\t", "") == (
            "В больнице сейчас 4 чел., из них:в статусе 'Тяжело болен': 1 чел.в статусе 'Болен': 2 чел."
            "в статусе 'Готов к выписке': 1 чел."
        )

    def test_statistics_raw_data_with_clear_db(self):
        hs = HospitalStatistics()
        statistics_data = hs._get_calculate_statistics_data()
        assert statistics_data["patients_amount"] == 0
        assert dict(statistics_data["statistics"]) == {}

    def test_statistics_output_with_clear_db(self):
        hs = HospitalStatistics()
        statistics_data = hs._create_calculate_statistics_output(Counter({}), 0)
        assert statistics_data == "В больнице сейчас 0 чел., из них:"
