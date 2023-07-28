wsgi_app =  "mysite.wsgi:application"

loglevel = "info"

workers = 2

bind = "0.0.0.0:8000"

reload = True

accesslog = errorlog = "/var/log/gunicorn/dev.log"

capture_output = True

pidfile = "/var/run/gunicorn/gunicon.pid"

daemon = True


