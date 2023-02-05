if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
else
    echo "DJANGO_SUPERUSER_USERNAME not set. Skipping superuser creation."
fi

$@