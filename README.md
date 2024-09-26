### Тестовое задание на вакансию Python developer в команду OracleStat

#### Задание
CLI приложение:

1) Получает на вход N строк.
2) Итерируется по этим строкам и определяет, является ли эта строка ссылкой или нет.
3) Если эта строка не ссылка, выводится уведомление: Строка "X" не является ссылкой.
4) Если является ссылкой, то
	1) Приложение должно определить какие методы доступны по этой ссылки
		1) Проверяются все http методы.
		2) Доступным считается метод, обработка которого завершилась не 405 ошибкой.
	3) Передаваемые данные и ошибки от сервера не важны.
	4) Выполнив запрос приложение сохраняет код ответа.
6) Результатом работы приложением будет словарь, состоящий из ссылок и информации о доступных метода.

### Тайминг

на выполнение ушло 2-3 часа