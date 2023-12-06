

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
    распознает команду "рассчитать статистику" и делегирует выполнение расчета статистики классу HospitalStatistics,
    у него есть понимание когда запросить у пользователя id пациента
    запрашивает у пользователя id пациента
        1. преобразует введенную строку в число 
        2. обрабатывает ситуацию, когда не число и сообщает пользователю об ошибке
        3. проверяет, что число не меньше 0 и сообщает пользователю об ошибке
        4. проверят что пациент с таким id существует в бд  и сообщает пользователю об ошибке
    если команда известная, не "расчет статистики" и id пациента корректный, то делегирует выполнение команды классу HospitalPatientStatus(передав команду в виде строки и id пациента)
    прерывает цикл в случае команды "стоп" 

    Содержит базу пациентов
    получает базу в конструкторе 
    если база не передана, сам ее создает и наполняет значениями

    С кем взаимодействует:
      HospitalStatistics
      HospitalPatientStatus
      DialogWithUser


## HospitalPatientStatus:

    преобразет id пациента в индекс базы пациентов
    обрабатывает полученную команду 
      1 - если команда "узнать статус пациента", сообщает пользователю статус пациента 
      2 - если команда "повысить статус пациента"
          - если начальный статус пациента равен 3 - "Готов к выписке", предлагает пользователю выписать пациента
              если получает команду да, делегирует выписку пациента методу выписки пациента
              если получает команду нет (все кроме да считается как нет), сообщает пользователю о сохранении текущего статуса пользователю
          - если начальный статус пациента меньше 3 
              увеличивает значение статуса пациента в базе пациентов 
              сообщает пользователю об изменении статуса
      3 - если команда "понизить статус пациента"
          - если начальный статус пациента равен 0 - "Тяжело болен"
              сообщает пользователю о невозможности изменения статуса пациента
          - если начальный статус пациента больше 0 
              уменьшает значение статуса пациента в базе пациентов 
              сообщает пользователю об изменении статуса
      4 - если команда "выписать пациента"
          удаляет запись о пациенте из базы пациентов 
          сообщает пользователю о выписке пациента 

    Содержит базу пациентов
    получает базу в конструкторе 
    если база не передана, сам пустую создает 

    С кем взаимодействует:
      DialogWithUser



## HospitalStatistics:
 
    Рассчитывает общее кол-во пациентов в базе и подсчитывает кол-во пациентов по каждому из статусов существующих в базе 
    создает строку с расчитанной статистикой о пациентах
    сообщает пользователю рассчитанную статистику 

    Содержит базу пациентов
    получает базу в конструкторе 
    если база не передана, сам пустую создает 

    С кем взаимодействует:
      DialogWithUser

## DialogWithUser:

    Класс взаимодействия с пользователем 

    Выводит пользователю сообщение с запросом получения новых данных и возвращает введенные пользователем данные 
    Вывод пользователю обработанных данныч 

    Ни о чем не знает 
    Ни с кем не взаимодействует 


tests.py:
- TestsStatus: 
  - тесты статусов
- TestsCalculateStatistics
  - тесты статистики 