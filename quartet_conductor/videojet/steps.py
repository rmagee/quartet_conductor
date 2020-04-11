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
# Copyright 2020 SerialLab Corp.  All rights reserved.
from telnetlib import Telnet

from quartet_capture import models
from quartet_capture.rules import RuleContext
from quartet_conductor.steps import TelnetStep
from enum import Enum

class CONTEXT_FIELDS(Enum):
    """
    Any job fields retrieved from the printer will be in the JOB_FIELDS
    context key
    """
    JOB_FIELDS = 'JOB_FIELDS'

class JobFieldsStep(TelnetStep):
    """
    Will issue a telnet command and then read the reply and return
    to the channel as the data.
    """

    def __init__(self, db_task: models.Task, **kwargs):
        super().__init__(db_task, **kwargs)
        self.host = self.get_or_create_parameter(
            'Host', 'printer',
            'The host name or IP address of the videojet printer.'
                                                 )
        self.port = int(self.get_or_create_parameter(
            'Port', '777',
            'The text communications port that was enabled on the printer.'
        ))

    def execute(self, data, rule_context: RuleContext):
        with Telnet(self.host, self.port) as client:
            self.info('Getting data from host %s on port %s...',
                      self.host, self.port)
            data = 'GJD\r'.encode('ascii')
            client.write(data)  # only output matches
            ret = client.read_until('\r'.encode('ascii'))
            self.info('Data retrieved: %s', ret)
            client.close()
            ret = ret.decode('ascii').split('|')
            dict = {}
            for item in ret:
                if '=' in item:
                    name, val = item.split("=")
                    dict[name] = val
            self.info('Fields: %s', dict)
            rule_context.context[CONTEXT_FIELDS.JOB_FIELDS.value] = dict
