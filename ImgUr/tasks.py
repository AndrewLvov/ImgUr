from requests.exceptions import ConnectionError
from itertools import islice
from imgurpython import ImgurClient
from smtplib import SMTPException

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

from ImgUr.models import Subscriber

from celery_init import app

import logging
from celery.utils.log import get_task_logger
genericLogger = get_task_logger(__name__)
genericLogger.setLevel(logging.INFO)

def matches_reqs(item):
    return \
        not item.is_album and \
        not item.nsfw and \
        (item.ups / item.downs > 8)


def generate_email(current_site, name, email, images):
    # Images is  a generator, we need to convert it to list first
    images = list(images)
    # fix images sizes to 640x640 max by adding prefix 'm' to resource name
    for image in images:
        parts = image.link.split('.')
        parts[-2] += 'l'
        image.link = '.'.join(parts)

    ctx = {
        # we need to build absolute url to be accessible from email
        'current_site': current_site,
        'name': name,
        'email': email,
        'images': images,
    }
    return render_to_string('email.html', ctx)


@app.task()
def send_email():
    genericLogger.info('Started send_email task')
    client = ImgurClient(settings.IMGUR['CLIENT_ID'],
                         settings.IMGUR['CLIENT_SECRET'])
    try:
        gallery = client.gallery(sort='top', window='week', page=0)
    except ConnectionError:
        genericLogger.error('Connection error')
        return
    images = islice((item for item in gallery if matches_reqs(item)), 0, 10)
    for s in Subscriber.objects.all():
        genericLogger.info('Started user {}'.format(s.email))
        email_content = generate_email(settings.HOST, s.name, s.email, images)
        try:
            send_mail(subject="Enjoy Most Popular ImgUr Images for the Last Week",
                      message="",
                      from_email='noreply@bestimgur.com',
                      recipient_list=[s.email],
                      html_message=email_content)
            genericLogger.info('Sent email to {}'.format(s.email))
        except SMTPException as e:
            # invalid email ?
            genericLogger.error(e)

