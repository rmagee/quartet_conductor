#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from quartet_conductor import session
from quartet_conductor import models


class TestSessions(TestCase):

    def test_a_start_session(self):
        session.start_session('ASDF123',
                              '012670')

    def test_a_start_session_twice(self):
        with self.assertRaises(session.SessionRunningError):
            session.start_session('ASDF123',
                                  '012670')
            session.start_session('ASDF123',
                                  '012670')

    def test_start_no_stop(self):
        models.Session.clear_session()
        session.start_session('ASDF123', '012670')
        models.Session.clear_session()
        with self.assertRaises(session.SessionExistsError):
            session.start_session('ASDF123', '012670')

    def test_b_get_session(self):
        for i in range(1, 200):
            cur_session = session.get_session()
            print(cur_session.lot)
            print(cur_session.expiry)
            print(cur_session.state)
            print(cur_session.created)

    def test_stop_then_start(self):
        cur_session = session.start_session('ASDF123', '012670')
        session.pause_session(cur_session.lot)
        with self.assertRaises(session.SessionStoppedError):
            session.start_session('ASDF123', '012670')

    def test_start_pause_restart_finish(self):
        cur_session = session.start_session('ASDF123', '012670')
        session.pause_session(cur_session.lot)
        models.Session.objects.get(
            lot='ASDF123',
            state=session.SessionState.PAUSED.value

        )
        with self.assertRaises(session.SessionNotActiveError):
            session.get_session()
        cur_session = session.restart_session(lot='ASDF123')
        session.finish_session(lot='ASDF123')
        with self.assertRaises(session.SessionStateError):
            session.restart_session(lot=cur_session.lot)


    def tearDown(self):
        pass
