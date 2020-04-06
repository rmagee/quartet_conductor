# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _
from datetime import datetime

import threading

class Session(models.Model):
    _session = None
    _session_lock = threading.Lock()

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
    def create_session(cls, session):
        with cls._session_lock:
            cls._session = session
            cls._session.save()

    @classmethod
    def clear_session(cls):
        with cls._session_lock:
            cls._session = None

    @classmethod
    def get_session(cls):
        with cls._session_lock:
            return cls._session

class SessionField(models.Model):
    pass
