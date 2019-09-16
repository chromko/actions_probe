#!/bin/sh
set -ex;
### Some ad-hoc init scripts
# python app/manage.py db upgrade
exec "$@"
