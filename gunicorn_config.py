# http://stackoverflow.com/questions/12858674/serving-a-request-from-gunicorn
workers = 3
bind = '127.0.0.1:5001'
pidfile = '/home/ubuntu/www/semantix/semantix.pid'
user = 'ubuntu'
daemon = True
errorlog = '/home/ubuntu/www/semantix/log/gunicorn-error.log'
accesslog = '/home/ubuntu/www/semantix/log/gunicorn-access.log'
proc_name = 'gunicorn-semantix'

