# Backend для сайта [DESC-Studio](https://desc-studio.online/index.html)
### Backend написан на фреймворе FastAPI. Для корректной работы необходим python версии 3.9 и выше. Создайте виртуальное окружение, и установите необходимые библиотеки командой `pip install -r requirements.txt`
## Для корректной аутентификации и авторизации необходимы приватный и публичный ключ в формате PEM. Перейдите в своем терминале в папку backend/auth/certs, и введите две следующих команды: 
  1. openssl genrsa -out jwt-private.pem 2048
  2. openssl rsa -in jwt-private.pem -outform pem -pubout -out jwt-public.pem
# БД
## Создайте файл .env в директории 'db'. Пропишите туда следующие данные
  1. DB_HOST=
  2. DB_PORT=
  3. DB_USER=
  4. DB_PASS=
  5. DB_NAME=



## Запуск
# Для запуска необзодимо перети в папку backend/app, и в терминале прописать `python main.py`. Посмотреть все endpoint можно по этому url: http://127.0.0.1:8000/docs

