sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/nginx.conf
sudo /etc/init.d/nginx restart
cd /home/box/web/
gunicorn -b 0.0.0.0:8080 hello:app
