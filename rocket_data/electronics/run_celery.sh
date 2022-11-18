#!/bin/sh

sleep 10

celery -A electronics worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler

