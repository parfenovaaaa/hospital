

Структура:

    -hospital 
        - logic
            - HospitalAccounting.py
            - HospitalPatientStatus.py
            - HospitalStatistics.py
        - tests
            - test.py
        -utils
            - constants.py
            - DialogWithUser.py
        - main.py

## HospitalAccounting:

    В цикле ожидает команду от пользователя, 
    обрабатывает ситуацию с неизвестной командой , 
    распознает команду "рассчитать статистику" и делигирует выполнение расчета статистики классу HospitalStatistics,
    у него есть понимание когда запросить у пользователя id пациента
    запрашивает у пользователя id пациента
        1. преобразует введенную строку в число 
        2. обрабатывает ситуацию, когда не число и сообщает пользователю об ошибке
        3. проверяет, что число не меньше 0 и сообщает пользователю об ошибке
        4. проверят что пациент с таким id существует в бд  и сообщает пользователю об ошибке
    если команда известная, не "рассчет статистики" и id пациента корректный, то делигирует выполнение команды классу HospitalPatientStatus(передав команду в виде строки и id пациента)
    прерывает цикл в случае команды "стоп" 

    Содержит базу пациентов
    получает базу в конструкторе 
    если база не передана, сам ее создает и наполняет значениями

    С кем взаимодействует:
      HospitalStatistics
      HospitalPatientStatus
      DialogWithUser


## HospitalPatientStatus:

    обрабатывает полученную команду
      если команда "узнать статус пациента", сообщает пользователю статус пациента 
    если команда "повысить статус пациента", делигирует методу повышения статуса пациента 
    если команда "понизить статус пациента", делигирует методу понижения статуса пациента 
    если команда "выписать пациента", делигирует методу выписки пациента 

    Обрабатывает команду "повысить статус пациента"
      если начальный статус пациета равен 3 - "Готов к выписке", предлагает пользователю выписать пациента
        если получает команду да, делирирует выписку пациента методу выписки пациента
        если получает любую другую команду, сообщает пользователю о сохранении текущего статуса пользователю
      если начальный статус пациента меньше 3 
        увеличивает значение статуса пациента в базе пациентов 
        сообщает пользователю об изменении статуса 

    обрабатывает команду "понизить статус пациента"
      если начальный статус пациета равен 0 - "Тяжело болен"
        сообщает пользователю о невозможности изменения статуса пациента
      если начальный статус пациета больше 0
        уменьшает значение статуса пациента в базе пациентов 
        сообщает пользователю об изменении статуса

    обрабатывает команду "выписать пациента"
      удаляет запичь пациента из базы пациентов 
      сообщает пользователю о выписке пациента 

    Содержит базу пациентов
    получает базу в конструкторе 
    если база не передана, сам пустую создает 

    С кем взаимодействует:
      DialogWithUser



## HospitalStatistics:

    Класс расчета статистики 
    Рассчитывет общее кол-во пациетов в базе и подсчитывает кол-во пациентов по статусам 
    создает строку с рассчетом статистики пациентов 
    сообщает пользователю расчитанную статистику 

    Содержит базу пациентов
    получает базу в конструкторе 
    если база не передана, сам пустую создает 

    С кем взаимодействует:
      DialogWithUser

## DialogWithUser:

    Класс взаимодействия с пользователем 

    Выводит пользователю сообщение с запросом получения новых данных и обрабатывает введенные пользователем данные 
    Вывод пользователю полученные данные 

    Ни о чем не знает 
    Ни с кем не взаимодействует 


tests.py:
- TestsStatus: 
  - тесты статусов
- TestsCalculateStatistics
  - тесты статистики 