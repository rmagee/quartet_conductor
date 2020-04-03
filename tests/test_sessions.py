#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from quartet_conductor import session


class TestSessions(TestCase):

    def test_a_start_session(self):
        session.create_session('ASDF123',
                               '012670')

    def test_a_start_session_twice(self):
        with self.assertRaises(session.SessionError):
            session.create_session('ASDF123',
                                   '012670')
            session.create_session('ASDF123',
                                   '012670')

    def test_b_get_session(self):
        for i in range(1,200):
            cur_session = session.get_session()
            print(cur_session.lot)
            print(cur_session.expiry)
            print(cur_session.state)
            print(cur_session.created)

    def tearDown(self):
        pass
