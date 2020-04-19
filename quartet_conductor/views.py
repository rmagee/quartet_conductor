from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.views import generic

from quartet_conductor.forms import SessionForm, InputMapForm
from quartet_conductor import session
from quartet_conductor import models
from quartet_conductor import settings as conductor_settings

from logging import getLogger

logger = getLogger(__name__)


def start_session(request: HttpRequest):
    if request.method == 'POST':
        try:
            form = SessionForm(request.POST)
            if form.is_valid():
                session.start_session(request.POST.get('lot'),
                                      request.POST.get('expiry'))
                return HttpResponseRedirect('/conductor/running/')
        except session.SessionRunningError:
            return HttpResponseRedirect('/conductor/session/')
    else:
        form = SessionForm()

    return render(request, 'session.html', {'form': form})


def session_info(request: HttpRequest):
    if request.method == 'GET':
        current_session = session.get_session()
        if not current_session:
            return HttpResponseRedirect('/conductor/session/')
        else:
            form = SessionForm(instance=current_session)
            return render(request, "session_info.html",
                          {'session': current_session, 'form': form})


def input_map_detail(request: HttpRequest, id: int=None):
    if request.method == 'GET':
        input_map = models.InputMap.objects.get(id=id)
        form = InputMapForm(instance=input_map)
        form.update_field_styles()
        return render(request, "input_map.html",
                      {'form': form, 'input_map': input_map}
                      )


class InputMapView(generic.ListView):
    model = models.InputMap
    template_name = 'input_maps.html'
    paginate_by = conductor_settings.DEFAULT_PAGESIZE
