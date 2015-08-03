from itertools import islice
from celery import Celery
from imgurpython import ImgurClient
from smtplib import SMTPException
import logging

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

from ImgUr.models import Subscriber

logger = logging.getLogger(__name__)

app = Celery('ImgUr')
app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


def matches_reqs(item):
    return \
        not item.is_album and \
        not item.nsfw and \
        (item.ups / item.downs > 8)


def generate_email(name):
    client = ImgurClient(settings.IMGUR['CLIENT_ID'],
                         settings.IMGUR['CLIENT_SECRET'])
    gallery = client.gallery(sort='top', window='week', page=0)
    ctx = {
        'gallery': islice((item for item in gallery if matches_reqs(item)), 0, 10),
        'name': name,
    }
    return render_to_string('email.html', ctx)


@app.task
def send_email():
    for s in Subscriber.objects.all():
        email_content = generate_email(s.name)
        try:
            send_mail(subject="Look at the Picked Most Popular ImgUr Images for the Last Week",
                      message=None,
                      from_email='noreply@bestimgur.com',
                      recipient_list=[s.email],
                      html_message=email_content)
        except SMTPException as e:
            logger.warning(e)


