# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2019 SerialLab Corp.  All rights reserved.

from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from quartet_capture import rules
from quartet_capture.models import Task, Rule
from quartet_capture.tasks import execute_queued_task, execute_rule

from telnetlib import Telnet

from quartet_conductor import session
from quartet_conductor import models
from quartet_conductor import steps

from quartet_conductor.videojet.inputs import InputMonitor

class UnitTestIM(InputMonitor):
    def get_session_data(self):
        self.session = session.start_session('W6G', '2211')


class TestMicroscanVideojet(TestCase):

    def test_intialize_scanner(self):
        input_monitor = UnitTestIM(host=settings.TELNET_HOST,
                                   port=settings.TELNET_PORT)
        input_monitor.get_session_data()
        input_monitor.intialize_scanner()

    def test_rule(self):
        call_command('create_initialize_microscan_rule', delete=True)
        rule = Rule.objects.get(
            name='Initialize Microscan'
        )
        task = Task.objects.create(
            rule=rule,
            name='UnitTestTask'
        )
        execute_rule('',task)

    def test_read_printer_settings(self):
        with Telnet('printer', 777, timeout=5) as client:
            data = 'GJD|rob|'.encode('ascii') + "\r".encode('ascii')
            client.write(data)  # only output matches
            ret = client.read_until(
                '\r'.encode('ascii')
            )
            client.close()
            ret = ret.decode('ascii').split('|')
            dict = {}
            for item in ret:
                if '=' in item:
                    name, val = item.split("=")
                    dict[name] = val
            print(dict)
