# **Проект Пилигрим.**

___
```
docker-compose -f docker-compose.test.yml up -d --build
```
___

- swagger  */docs*   
- redoc    */redoc*
- админка  */api/admin*
___

## Система для контроля учета продаж и сбора статистики. 

* Автоматизирует взаимодействие работников, исходя из их роли.
* В зависимости от роли у юзера различные права и задачи.
* Клиенты собраны по базам, имеют архивы с документами и контрактами.
* Менеджеры, закрепленные за клиентом, формируют заявки, которые
отображаются на сайтбаре слева и в разделах. 
* Эти задачи объединяются ими в просчет, его подтверждает главный менеджер, 
если маржа и условия подходят.
* После утверждения всех условий и полей — формируется сделка. 
* Сделка имеет свои статусы, которые продвигают активные в ней работники, 
куда входят менеджеры, логист, бухгалтер и финансовый директор. 
В итоге, выполняя нужные инструкции и подгружая документы,
сделка закрывается и переходит в статус закрытой.
* Закрытая сделка используется для квартальных отчетов. 
___
В прикрепленных к сущностям документах сохраняется документооборот и вся история.
На закладке «статистика» ведется учет финансовых взаиморасчетов с клиентами и отображаются графики, задолженность, депозиты, сальдо. 
___

> Работаем на гитлаб, тут выложено для примера бекэнда, докер yaml сделан так же для бека.
