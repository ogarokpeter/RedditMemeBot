# Reddit Meme Bot for Facebook Messenger

## Description

A bot for Facebook Messenger that aggregates and presents to a user new and/or interesting posts from Reddit. It can show a specified number of posts from all Reddit, or from certain channels. It also supports subscriptions: a user can subscrive to certain channels via the bot, and get updates from these channels every time she/he is on Messenger. The stores user data persistently in a Redis database.

Users can communicate with the bot via hardcore CLI it parses. To see all supported commands, type '--help'.

Bot was implemented as a task in my university. The description of the task (in Russian) is below.

## How to run

Requirements: you need to have [localtunnel](https://github.com/localtunnel/localtunnel) and [Redis](https://redis.io/) installed, as well as python packages from the requirements.txt file.

Main steps to run a bot are described [here](https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html): you need a Facebook developer account, a Reddit developer account and a webhook. To obtain the webhook, run localtunnel and update webhook link in Facebook interface. Then run Redis to create a database. After that, you can run a bot by typing

```$ python3 app.py```

To ensure stability, the best thing is to run a bot on a server or a cloud instance.

## Description of the task (Russian)

### Постановка задачи
Напишите и разверните Faсebook Messenger бота для агрегации мемов.

Ваш бот должен уметь по команде отправлять пользователю интересный контент. 
В каком виде он должен его отправлять, и что именно является интересным - остаётся на ваше усмотрение.

Как усложнение задания - бот должен оказывать сервис подписки.
То есть предлагать пользователю подписаться на некие ресурсы. 
Когда пользователь заходит на Facebook - бот предлагает ему ознакомиться со всем произошедшим на этих ресурсоах со времени последнего общения пользователя и бота.
Ну или с самым интересным контентом, ведь интернеты так бездонны =)


В качестве источника интересного контента мы предлагаем разобраться с Web API Reddit.
https://www.reddit.com/dev/api


### Как решать задачу
1. Разверните локально web-сервис, который поддержит протокол взаимодействия с Facebook Messgenger.
https://developers.facebook.com/docs/messenger-platform
Научитесь получать текстовые сообщения, и отправлять на них в ответ.
Facebook требует чтобы ваш сервис работал по SSL , 
поэтому для локальной отладки вам понадобится утилита для туннелирования, например https://localtunnel.github.io/www/ .
Пример работы с туннелем есть в официальной доке Facebook https://developers.facebook.com/docs/messenger-platform/getting-started/test-drive
https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html – хороший туториал по созданию бота

2. Выберите что именно бот будет отправлять пользователю, и в каком виде.
Разберитесь как это получать по Web API.
В качестве источника интересного контента мы предлагаем разобраться с Web API Reddit.
https://www.reddit.com/dev/api
Разберитесь как это оправлять пользователю.
Реализуйте это! Убедитесь локально, что всё работает. На фейсбуке хорошенечко пообщайтесь с вашим ботом.

3. Выложить веб-сервис в продакшен.
Эта часть обязательна!
Мы предлагаем использовать Яндекс.Облако https://cloud.yandex.ru/
либо PythonAnywhere https://www.pythonanywhere.com/.
Не забудьте после этого обновить адрес веб-хука в настройках бота!

4. Персистентное хранилище.
Чтобы не продолбать пользовательские данные, надо их надёжно хранить.
Предлаем разобраться как это можно сделать на примере Redis.
https://redis.io/
Эта часть не является обязательной, если не смогли/не успели разобраться как это сделать - 
задание просто оценивается из меньшего числа баллов.

5. Соберите все зависимости проекта (называния всех используемых питонячих пакетов и их версии)в файлик requirements.txt
Что это такое см документацию https://pip.pypa.io/en/stable/user_guide/#requirements-files


----
### Как сдавать задачу
#### submit.py
Необходимо положить код бота и отчёт в папку с задачей.
Отчёт надо положить в файлик report.md, настоятельно рекомендуется разобраться в форматировании 
[Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

Код можно класть в произвольные папочки.

Дальше надо просто выполнить `python3 ../submit.py` как обычно.

Проверить что именно отправилось на проверку можно в своём приватном репозитори в ветке с задачей, 
ссылка на него есть на главной странице проверяющей системы в шапке.

Задачу надо сдать в систему до дедлайна, система выдаст 1 балл и проверит лишь что вы в срок сдали задание.
Проверка будет проходить в ручном режиме. Баллы проставят в табличку с оценками после проверки всех работ

#### выдать админский доступ к вашему приложению на Facebook для преподавателей курса
Публикация бота для широкой публики - некий бюрократический процесс, 
который может затянуться или вовсе не закончиться успехом. 

Чтобы мы смогли оценить ваши продуктовые фичи, вы можете добавить преподавателей в администраторы приложения.
TODO: инструкция как это сделать.

### Критерии оценки
Максимальный балл за задание - 200 баллов.
Сверх этого за задачу возможны бонусы. 
Бонусы - это баллы, которые идут в числитель накопительной оценки за курс, но не в знаменатель.


#### Что влияет на оценку
1. Самое главное - It's alive! Бот работает, с ним можно поговорить, он присылает свеженькие приколы. 
~70 баллов

2.  Качество отчёта. ~30 
Опишите какие продуктовые фичи вы реализовали (что бот умеет), вашу реализацию, как захостили, какие проблемы решили.
Эту часть сложно формализовать, оценивается понятность, интересность, фантазия, находчивость,
настойчивость в достижении цели и самореклама, конечно.

3. Реализация. Какие фичи поддержаны. Насколько надёжно работает.  ~70 баллов

4. Cтиль кода (аккуратность, модульность, честные понятные имена, PEP8) - ~30 баллов.



Бонусы: за классные продуктовые фичи и подвиги в реализации!
До 150 баллов, хотя зависит от того насколько вы нас удивите.

