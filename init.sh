sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/nginx.conf
sudo /etc/init.d/nginx restart
cd /home/box/web/
gunicorn -b 0.0.0.0:8080 hello:app &
cd ask/
gunicorn -b 0.0.0.0:8000 ask.wsgi:application
sudo mysql -uroot -e "create database stepic_web;" # создание базы данных stepic_web
sudo mysql -uroot -e "CREATE USER 'egreth'@'localhost' IDENTIFIED BY 'password';" # создание пользователя egreth с паролем password
sudo mysql -uroot -e "GRANT ALL ON stepic_web.* TO 'egreth'@'localhost';" # выдача прав пользователю
