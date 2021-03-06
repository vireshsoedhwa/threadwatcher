#!/bin/sh

set -e

>&2 echo "Make Database migrations"
python manage.py makemigrations v1
echo "-------------------------------------------------------------------------------------------\n"


>&2 echo "Run Database migrations"
python manage.py migrate
echo "-------------------------------------------------------------------------------------------\n"



>&2 echo "Start Django Q task Scheduler"
python manage.py qcluster &
echo "-------------------------------------------------------------------------------------------\n"

>&2 echo "create task"
echo "from django_q.tasks import schedule; import arrow; schedule('v1.tasks.get_all_ylyl_threads',
         schedule_type=Schedule.MINUTES,
         minutes=5,
         repeats=-1,
         next_run=arrow.utcnow())"

>&2 echo "Create temporary superuser"
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com','admin')" | python manage.py shell

echo "-------------------------------------------------------------------------------------------\n"

# Start Django dev server
>&2 echo "Starting Django runserver..."
# while true; do sleep 12 ; echo "foreground"; done
exec "$@"