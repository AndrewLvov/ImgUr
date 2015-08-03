from django.shortcuts import render

from .forms import SubscriberForm


def index(request):
    form = SubscriberForm(request.POST or None)
    if form.is_valid():
        form.save()

    ctx = {}

    return render(request, 'index.html', ctx)
