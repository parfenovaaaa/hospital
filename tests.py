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
    def test_statistics_same_status(self):
        expected_msg = f"В больнице сейчас 4 чел., из них:в статусе 'Болен': 4 чел."
        hs = HospitalStatistics([1, 1, 1, 1])
        actual_msg = hs.calculate_statistics()
        assert expected_msg == actual_msg.replace("\n\t", "")

    def test_statistics_all_status(self):
        expected_msg = (
            "В больнице сейчас 4 чел., из них:в статусе 'Тяжело болен': 1 чел.в статусе 'Болен': 1 чел."
            "в статусе 'Слегка болен': 1 чел.в статусе 'Готов к выписке': 1 чел."
        )
        hs = HospitalStatistics([0, 1, 2, 3])
        actual_msg = hs.calculate_statistics()
        assert expected_msg == actual_msg.replace("\n\t", "")

    def test_statistics_with_clear_db(self):
        expected_msg = "В больнице сейчас 0 чел., из них:"
        hs = HospitalStatistics([])
        hs.patients_db.clear()
        actual_msg = hs.calculate_statistics()
        assert expected_msg == actual_msg
