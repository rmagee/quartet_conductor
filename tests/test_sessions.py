#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.test import TestCase

from quartet_capture.models import Task, Rule
from quartet_capture.tasks import execute_rule
from quartet_capture.rules import RuleContext
from quartet_conductor import models
from quartet_conductor import session
from quartet_conductor.videojet.steps import ContextFields
import time


class TestSessions(TestCase):

    def setUp(self) -> None:
        pass

    def test_a_start_session(self):
        rule_context = self.run_rule()
        lot, expiry = self.get_lot_expiry(rule_context)
        session.start_session(lot,
                              expiry,
                              2,
                              rule_context)

    def test_a_start_session_twice(self):
        rule_context = self.run_rule()
        lot, expiry = self.get_lot_expiry(rule_context)
        session.start_session(lot,
                              expiry,
                              2,
                              rule_context)
        self.assertEqual(lot, session.get_session(2).lot)
        session.start_session(lot,
                              expiry,
                              2,
                              rule_context)
        self.assertEqual(lot, session.get_session(2).lot)

    def run_rule(self):
        call_command('create_initialize_microscan_rule', delete=True)
        rule = Rule.objects.get(
            name='Initialize Microscan'
        )
        task = Task.objects.create(
            rule=rule,
            name='UnitTestTask'
        )
        time.sleep(1)
        return execute_rule('', task)

    def get_lot_expiry(self, rule_context: RuleContext):
        job_fields = rule_context.context.get(ContextFields.JOB_FIELDS.value)
        return job_fields['LOT'], job_fields['EXPIRY']

    def test_b_get_session(self):
        for i in range(1, 200):
            cur_session = session.get_session(2)
            print(cur_session.lot)
            print(cur_session.expiry)
            print(cur_session.state)
            print(cur_session.created)
            print(cur_session.context)

    def tearDown(self):
        pass
