from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest

from quartet_conductor.forms import SessionForm
from quartet_conductor import session

from logging import getLogger

logger = getLogger(__name__)


def start_session(request: HttpRequest):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session.start_session(request.POST.get('lot'),
                                  request.POST.get('expiry'))
            return HttpResponseRedirect('/conductor/running/')
    else:
        form = SessionForm()
        session.create_session_db()
    return render(request, 'session.html', {'form': form})


def session_info(request: HttpRequest):
    if request.method == 'GET':
        current_session = session.get_session()
        if not session:
            return HttpResponseRedirect('/session/')
        else:
            return render(request, "session_info.html",
                          {'session': current_session})
