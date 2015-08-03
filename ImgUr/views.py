from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest

from .forms import SubscriberForm
from .models import Subscriber



def index(request):
    form = SubscriberForm(request.POST or None)
    if form.is_valid():
        form.save()

    ctx = {
        'form': form,  # to display errors if any
    }

    return render(request, 'index.html', ctx)

def unsubscribe(request):
    email = request.GET.get('email')
    if not email:
        return HttpResponseBadRequest()
    Subscriber.objects.filter(email=email).delete()

    return redirect('index')
