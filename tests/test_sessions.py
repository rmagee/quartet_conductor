#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from quartet_conductor import session


class TestSessions(TestCase):

    def setUp(self):
        session.create_session_db()

    def test_a_start_session(self):
        session.start_session('ASDF123', '012670')

    def test_b_get_session(self):
        for i in range(1,200):
            session.get_session()

    def tearDown(self):
        pass
