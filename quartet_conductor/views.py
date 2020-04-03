from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest

from quartet_conductor.forms import SessionForm

from logging import getLogger

logger = getLogger(__name__)


def start_session(request: HttpRequest):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            logger.debug('The form is valid, starting the session.')
            return HttpResponseRedirect('/conductor/running/')
    else:
        form = SessionForm()
        print('******************************')
    return render(request, 'session.html', {'form': form})
