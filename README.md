# Расписание пар ФУ при Правительстве РФ по SMS

### Таблицы в Redis
1. Номер телефона -> группа (main)
2. Группа -> id группы (main) 
3. Номер телефона -> id группы (FIFO)
4. id группы -> расписание (main) <-------- НЕ СДЕЛАНО

### Общий алгоритм
Чтоб не потерять
1. Запускается Redis со снапшота
2. Запускается Flask с sender'ом, когда необходимо (в 7 утра(?)), то заносит в FIFO-таблицу №3 данные с 1 и 2. Иногда делает перерывы, чтоб оператор все не забанил.
3. Sender принимает данные в очереди, берет данные о расписании с FIN_API и отправляет их на GSM-модуль

### Общая архитектура

<img src="https://github.com/GeorgiyDemo/FAtimetable/blob/master/other/diagram.png" width="673" height="422">


