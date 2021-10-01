set -e

flask db upgrade
flask seed

gunicorn -c gunicorn.config.py serve:app