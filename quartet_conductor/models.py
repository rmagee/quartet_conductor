# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

class Session(models.Model):
    lot = models.CharField(
        max_length=20,
        null=False,
        blank=False,
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


class SessionField(models.Model):
    pass
