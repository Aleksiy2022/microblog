# Microblog Application

## Описание
Microblog - это веб-приложение, реализующее функционал микроблога, где пользователи могут создавать и управлять своими 
твитами, взаимодействовать с другими пользователями и просматривать ленты твитов.

## Функционал

1. Пользователь может добавить новый твит.
2. Пользователь может удалить свой твит.
3. Пользователь может зафоловить другого пользователя.
4. Пользователь может отписаться от другого пользователя.
5. Пользователь может отмечать твит как понравившийся.
6. Пользователь может убрать отметку «Нравится».
7. Пользователь может получить ленту из твитов.
8. Твит может содержать картинку.

## Установка и запуск приложения

1. Установите Docker на вашей машине, если он еще не установлен. Подробные инструкции доступны по ссылке:
Docker Installation Guide (https://docs.docker.com/get-docker/)
2. Если вы находитесь в регионе, где Docker заблокирован,  то изучите данный материал. 
https://proglib.io/p/docker-ushel-iz-rf-instrukciya-po-vosstanovleniyu-dostupa-k-docker-hub-dlya-polzovateley-iz-rossii-2024-05-30
3. После успешной установке Docker, чтобы развернуть проект, находясь в корневой дирректории проекта выполните 
следующую команду: 

      `docker compose up -d.`
4. После успешного запуска контейнеров приложение будет доступно по адресу http://localhost/

## Запуск тестов

1. Для запуска тестов на локальной машине может понадобиться доступ к папке, созданной докером для хранения данных БД. 
Для этого выполните команду:
   `docker exec -it <container_id> chmod -R 777 /var`
Замените `<container_id>` на идентификатор контейнера с вашим приложением.
2. Установите виртуально окружение с интерпритатором python версии 3.12
3. Установите poetry командой: `pip install poetry`
4. Установите необходимые зависимости командой: `poetry install`
5. Запустите тесты на локальной машине командой: `pytest`