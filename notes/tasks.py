from celery import shared_task
from django.db.models import F
from django.utils.timezone import now

from .models import Note


@shared_task
def purge_notes():
    Note.objects.filter(times_read__gte=F('allowed_reads')).delete()
    Note.objects.filter(expires_at__lt=now()).delete()
