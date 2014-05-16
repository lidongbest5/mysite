#!/bin/bash
ps aux | grep uwsgi | grep django | awk '{print $2}'|xargs kill -9
#cd /root/software/uwsgi
/root/software/uwsgi/uwsgi -x /home/django_uwsgi.xml > /home/django.log 2>&1 &

