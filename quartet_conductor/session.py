from enum import Enum
from logging import getLogger
from django.db.utils import IntegrityError
from quartet_conductor.models import Session

logger = getLogger(__name__)

class SessionState(Enum):
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    PAUSED = 'PAUSED'


class SessionRunningError(Exception):
    """
    Raised when the system tries to start a session that is already running.
    """
    pass

class SessionStoppedError(Exception):
    """
    Raised when a new session is created that matches a session that has been
    stopped but not completed.
    """
    pass

class SessionExistsError(Exception):
    """
    Raised when a session that is being started was already started but was
    never stopped gracefully (i.e., a power shutdown, crash or something
    similar).
    """
    pass

class SessionNotActiveError(Exception):
    """
    Raised when a session that is being started was already started but was
    never stopped gracefully (i.e., a power shutdown, crash or something
    similar).
    """
    pass

class SessionStateError(Exception):
    """
    Raised if a session is being acted on while it's current state is
    incompatible with the action
    """
    pass


def start_session(lot: str, expiry: str) -> Session:
    """
    Starts a session by passing in the log and expiration date.  Returns
    a Session model instance.  If a session is already running,
    a SessionRunningError will be raised.  If a session is not running but was not
    stopped gracefully, a SessionExistsError will be raised.
    :param lot: The lot number
    :param expiry: The expiration date
    :return:
    """
    cur_session = Session(
        lot=lot,
        expiry=expiry,
        state=SessionState.RUNNING.value
    )
    if not Session.get_session():
        # see if one was started and never stopped
        if Session.objects.filter(lot=lot, state=SessionState.RUNNING.value).exists():
            raise SessionExistsError('The session with lot %s was started '
                                     'and was never stopped gracefully.')
        # see if one was stopped
        elif Session.objects.filter(lot=lot, state=SessionState.PAUSED.value).exists():
            raise SessionStoppedError('The session being started already exits'
                                      'as a stopped session.  To restart, '
                                      'call the session_restart function.')

    if Session._session and Session._session.lot == lot:
        raise SessionRunningError('The session with lot %s is already started.'
                                  % lot)

    Session.create_session(cur_session)
    return cur_session


def get_session() -> Session:
    cur_session = Session.get_session()
    if not cur_session:
        raise SessionNotActiveError('There is no currently running session.')
    return cur_session

def pause_session(lot: str):
    """
    Stops a session based on lot number.
    :param lot: Lot number of the session to stop.  If there is no session
    currently active, will rais a
    :return: None
    """
    cur_session = get_session()
    cur_session.state = SessionState.PAUSED.value
    cur_session.save()
    Session.clear_session()

def restart_session(lot: str):
    """
    Will attempt to restart a session identified by lot.  IF the session is
    not found or is not in a paused state a SessionExistsError will be raised.
    :param lot: The lot number that identifies the paused session.
    :return: The restarted session will be returned.
    """
    cur_session = Session.get_session()
    if cur_session:
        raise SessionExistsError('There is already an active session with '
                                 'lot %s active. Please stop or finish this '
                                 'session before starting a new one.' %
                                 cur_session.lot)
    try:
        cur_session = Session.objects.get(lot=lot, state=SessionState.PAUSED.value)
        cur_session.state = SessionState.RUNNING.value
        Session.create_session(cur_session)
        return cur_session
    except Session.DoesNotExist:
        raise SessionStateError('The session for lot %s either does not exist '
                                'or it is not in a PAUSED state.' % lot)

def finish_session(lot: str):
    """
    Will mark a session state to FINISHED and remove the session from memory.
    :param lot: The lot of the session to finish.
    :return: None.
    """
    cur_session = Session.get_session() or Session.objects.get(lot=lot)
    cur_session.state = SessionState.FINISHED.value
    cur_session.save()
    Session.clear_session()


