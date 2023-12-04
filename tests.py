from collections import Counter

from main import HospitalPatientAccounting, HospitalStatistics


class TestsStatusDown:
    def test_status_down_complete(self):
        hpa = HospitalPatientAccounting([3, 2, 3,])
        actual_msg = hpa.patient_status_down(patient_id=2)
        assert hpa.patients_db == [3, 1, 3]
        assert actual_msg == "Новый статус пациента: 'Болен'"

    def test_status_down_error(self):
        hpa = HospitalPatientAccounting([2, 0, 2,])
        actual_msg = hpa.patient_status_down(patient_id=2)
        assert hpa.patients_db == [2, 0, 2]
        assert "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)" == actual_msg


class TestsCalculateStatistics:
    def test_statistics_raw_data(self):
        hs = HospitalStatistics([2, 2, 3, 0])
        raw_data = hs.calculate_statistics_raw_data()
        assert raw_data["patients_amount"] == 4
        assert dict(raw_data["statistics"]) == {0: 1, 2: 2, 3: 1}

    def test_statistics_output(self):
        expected_statistics = {0: 1, 1: 2, 3: 1}
        expected_amount = 4
        hs = HospitalStatistics([1, 1, 3, 0])
        actual_msg = hs.create_calculate_statistics_output(Counter(expected_statistics), expected_amount)
        assert actual_msg.replace("\n\t", "") == (
            "В больнице сейчас 4 чел., из них:в статусе 'Тяжело болен': 1 чел.в статусе 'Болен': 2 чел."
            "в статусе 'Готов к выписке': 1 чел."
        )

    def test_statistics_raw_data_with_clear_db(self):
        hs = HospitalStatistics()
        hs.patients_db.clear()
        raw_data = hs.calculate_statistics_raw_data()
        assert raw_data["patients_amount"] == 0
        assert dict(raw_data["statistics"]) == {}

    def test_statistics_output_with_clear_db(self):
        hs = HospitalStatistics()
        hs.patients_db.clear()
        raw_data = hs.create_calculate_statistics_output(Counter({}), 0)
        assert raw_data == "В больнице сейчас 0 чел., из них:"
