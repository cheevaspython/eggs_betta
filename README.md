docker-compose build

docker-compose up

127.0.0.1:8000/api/swag

Проект Пилигрим (направление яйца)

Система, помогающая контролировать создание заказов и автоматизировать продажи. Ведет учет и собирает статистику.

Программный продукт создан для облегчения работы различных отделов организации. Автоматизация процессов повышает уровень продаж, оптимизирует маркетинг и улучшает уровень взаимодействия между сотрудниками компании.

В общих чертах:
* User имеет роли, исходя из которых определяются возможности и задачи.
* Фин. директор, Superuser могут создавать и редактировать базу, редактировать статистику, пользоваться админкой. плюс имеют расширенные возможности доступа.
* менеджеры, логист и старший менеджер - создают и обрабатывают заказы.
* Гость введен для менеджеров вне штата с возможностью так же размещения заявки.
* заказы делятся на стадии: 
- заявка
- просчет
- подтвержденный просчет
- сделка
* сделка имеет статусы, следующие по хронологии выполнения.
* уведомления направляют usera к действию.
* в сделку и базу загружаются документы pdf

