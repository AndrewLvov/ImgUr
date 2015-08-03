from django.forms.models import ModelForm

from .models import Subscriber


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ('name', 'email',)
