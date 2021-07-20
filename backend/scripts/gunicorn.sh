#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0
python manage.py loaddata admin_interface_theme_vanguard.json
gunicorn vanguard.wsgi -w 4 --worker-class gevent -b 0.0.0.0:8002 --chdir=/app