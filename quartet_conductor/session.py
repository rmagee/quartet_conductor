from enum import Enum
from logging import getLogger
from django.db.utils import IntegrityError
from quartet_conductor.models import Session
from quartet_capture.rules import RuleContext

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


def start_session(lot: str, expiry: str, origin_input: int,
                  rule_context: RuleContext = None,
                  ) -> Session:
    """
    Starts a session by passing in the log and expiration date.  Returns
    a Session model instance.  If a session is already running,
    a SessionRunningError will be raised.  If a session is not running but was not
    stopped gracefully, a SessionExistsError will be raised.
    :param lot: The lot number
    :param expiry: The expiration date
    :param origin_input: The identifier for the session, should be an IO port
        number responsible for triggering the session or something similar and
        unique.
    :param rule_context: If a session was initiated via a rule containing
        information necessary for IO map signals to gain access to, add the
        context to the new session.
    :return: A new Session model instance.
    """
    cur_session = Session(
        lot=lot,
        expiry=expiry,
        state=SessionState.RUNNING.value
    )
    if not Session.get_session(origin_input):
        # see if one was started and never stopped
        if Session.objects.filter(lot=lot,
                                  state=SessionState.RUNNING.value).exists():
            raise SessionExistsError('The session with lot %s was started '
                                     'and was never stopped gracefully.')
        # see if one was stopped
        elif Session.objects.filter(lot=lot,
                                    state=SessionState.PAUSED.value).exists():
            raise SessionStoppedError('The session being started already exits'
                                      'as a stopped session.  To restart, '
                                      'call the session_restart function.')

    if Session._sessions.get(origin_input) and Session._sessions.get(origin_input).lot == lot:
        raise SessionRunningError('The session with lot %s is already started.'
                                  % lot)

    Session.create_session(cur_session, origin_input, rule_context)
    return cur_session


def get_session(origin_input: int) -> Session:
    """
    Returns a session by it's origin input value or identifier.
    :return: A session model instance.
    """
    cur_session = Session.get_session(origin_input)
    if not cur_session:
        raise SessionNotActiveError('There is no currently running session.')
    return cur_session


def finish_session(lot: str) -> None:
    """
    Will mark a session state to FINISHED and remove the session from memory.
    :param lot: The lot of the session to finish.
    :return: None.
    """
    cur_session = Session.get_session() or Session.objects.get(lot=lot)
    cur_session.state = SessionState.FINISHED.value
    cur_session.save()
    Session.clear_session()
