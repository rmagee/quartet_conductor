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

from quartet_capture import rules, models
from quartet_capture.rules import RuleContext
from quartet_templates.steps import TemplateStep as TS
from telnetlib import Telnet


class TemplateStep(TS):

    def execute(self, data, rule_context: RuleContext):
        ret = super().execute(data, rule_context)
        self.info('Converting the return text to ASCII')
        return ret.encode('ascii')


class TelnetStep(rules.Step):
    """
    Sends the data from the channel to a Telnet endpoint and disconnects.
    """

    def __init__(self, db_task: models.Task, **kwargs):
        super().__init__(db_task, **kwargs)

    def execute(self, data, rule_context: RuleContext):
        self.init_params()
        with Telnet(self.host, self.port) as client:
            self.info('Writing data %s', data)
            client.write(data)  # only output matches
            client.close()

    def init_params(self):
        self.host = self.get_or_create_parameter(
            'Host', 'scanner.local',
            'The IP address or host name of the '
            'system to send data to.'
        )
        self.port = int(self.get_or_create_parameter(
            'Port', '23',
            'The port to send data to.'
        ))

    @property
    def declared_parameters(self):
        return {
            'Host': 'The host to send data to.',
            'Port': 'The telnet port on the host.'
        }

    def on_failure(self):
        pass



