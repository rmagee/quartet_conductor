# -*- coding: utf-8 -*-
import threading
from django.db import models
from django.utils.translation import gettext as _

from quartet_capture.models import Rule
from quartet_capture.rules import RuleContext

from logging import getLogger

logger = getLogger()


class Session(models.Model):
    _sessions = {}
    _session_locks = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}

    STATE_CHOICES = [
        ('RUNNING', 'Running'),
        ('PAUSED', 'Paused'),
        ('FINISHED', 'Finished')
    ]
    lot = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('Lot'),
        help_text=('The session lot number')
    )
    expiry = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        verbose_name=_('Expiry'),
        help_text=_('The expiration date.')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
        help_text=('Date and time that the session was created.')
    )
    state = models.CharField(
        max_length=50,
        verbose_name=_("State"),
        help_text=_("The current state of the session."),
        null=False,
        blank=False,
        choices=STATE_CHOICES,
        default='RUNNING'
    )

    @classmethod
    def create_session(cls, session, origin_input: int,
                       rule_context: RuleContext = None,
                       ):
        with cls._session_locks:
            logger.debug(
                'Adding session with origin input %s and rule_context',
                origin_input, rule_context.context)
            session.context = rule_context
            cls._sessions[origin_input] = session
            session.save()

    @classmethod
    def clear_session(cls, origin_input: int):
        with cls._session_locks:
            logger.debug('Clearing session with origin input %s', int)
            cls._sessions.pop(origin_input, None)
            logger.debug('Session clear.')

    @classmethod
    def get_session(cls, origin_input: int):
        with cls._session_locks:
            return cls._sessions.get(origin_input, None)


class InputMap(models.Model):
    input_number = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name=_('Input Number'),
        help_text=_('The input number to map the rule and input text to.'),
        default=7
    )
    rule = models.ForeignKey(
        Rule,
        null=False,
        blank=False,
        verbose_name=_('Rule'),
        help_text=_('The rule to execute when the input is high.'),
        on_delete=models.CASCADE
    )
    rule_data = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Rule Data'),
        help_text=_('Any data to send to the rule when running it. The format'
                    'depends on what the rule expects. ')
    )
    related_session_input = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Related Session Input'),
        help_text=_('If a session is started via another input and that '
                    'session contains data necessary for this mapping input '
                    'map\'s rule to run then assign that input here.')
    )
