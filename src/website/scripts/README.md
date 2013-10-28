Setup website in /opt

    mkdir /opt/apps
    cd /opt/apps
    virtualenv bigdata-env
    cd bigdata-env
    source bin/activate
    pip install django django-registration psycopg2 python-dateutil markdown
    # maybe also install globally?
    ln -s <LOCATION OF website/> site


ensure that logs directory exists in site/

add settings.py in site/website/

setup database

uwsgi and nginx config scripts.

    cp uwsgi.conf /etc/init/uwsgi.conf
    cp nginx.conf /etc/nginx/nginx.conf
    cp site.conf /etc/nginx/conf.d/site.conf

Then start them

    sudo /etc/init.d/nginx start
    sudo start uwsgi

Make sure running uwsgi 1.9
