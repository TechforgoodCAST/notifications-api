#!/bin/bash
case $NOTIFY_APP_NAME in
  api)
    unset GUNICORN_CMD_ARGS
    scripts/run_app_paas.sh gunicorn -c /home/vcap/app/gunicorn_config.py application
    ;;
  delivery-worker)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery worker --loglevel=INFO --concurrency=11 \
    -Q job-tasks,retry-tasks,create-letters-pdf-tasks,letter-tasks 2> /dev/null
    ;;
  delivery-worker-database)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery worker --loglevel=INFO --concurrency=11 \
    -Q database-tasks 2> /dev/null
    ;;
  delivery-worker-research)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery worker --loglevel=INFO --concurrency=5 \
    -Q research-mode-tasks 2> /dev/null
    ;;
  delivery-worker-sender)
    scripts/run_multi_worker_app_paas.sh celery multi start 3 -c 10 -A run_celery.notify_celery --loglevel=INFO \
    -Q send-sms-tasks,send-email-tasks
    ;;
  delivery-worker-periodic)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery worker --loglevel=INFO --concurrency=2 \
    -Q periodic-tasks,statistics-tasks 2> /dev/null
    ;;
  delivery-worker-priority)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery worker --loglevel=INFO --concurrency=5 \
    -Q priority-tasks 2> /dev/null
    ;;
  # Only consume the notify-internal-tasks queue on this app so that Notify messages are processed as a priority
  delivery-worker-internal)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery worker --loglevel=INFO --concurrency=11 \
    -Q notify-internal-tasks 2> /dev/null
    ;;
  delivery-worker-receipts)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery worker --loglevel=INFO --concurrency=11 \
    -Q ses-callbacks 2> /dev/null
    ;;
  delivery-worker-service-callbacks)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery worker --loglevel=INFO --concurrency=11 \
    -Q service-callbacks 2> /dev/null
    ;;
  delivery-celery-beat)
    scripts/run_app_paas.sh celery -A run_celery.notify_celery beat --loglevel=INFO
    ;;
  *)
    echo "Unknown notify_app_name $NOTIFY_APP_NAME"
    exit 1
    ;;
esac