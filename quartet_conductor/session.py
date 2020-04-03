
from enum import Enum
from quartet_conductor.models import Session



class SessionState(Enum):
    STARTED = 'STARTED'
    COMPLETE = 'COMPLETE'
    STOPPED = 'STOPPED'


def create_session(lot: str, expiry: str) -> Session:
    cur_session = Session(
        lot=lot,
        expiry=expiry
    )
    Session.create_session(cur_session)
    return cur_session

def get_session() -> Session:
    return Session.get_session()

