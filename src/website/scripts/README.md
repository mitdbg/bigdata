Setup website in /opt

    mkdir /opt/apps
    cd /opt/apps
    virtualenv bigdata-env
    cd bigdata-env
    source bin/activate
    pip install django django-registration psycopg2 python-dateutil markdown
    ln -s <LOCATION OF website/> site

ensure that logs directory exists in site/

uwsgi and nginx config scripts.

    cp uwsgi.conf /etc/init/uwsgi.conf
    cp nginx.conf /etc/nginx/nginx.conf
    cp site.conf /etc/nginx/conf.d/site.conf

