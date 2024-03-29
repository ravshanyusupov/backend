#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0

python manage.py fill_database -a

python manage.py runserver 0.0.0.0:8000
