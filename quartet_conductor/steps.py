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
from quartet_conductor.session import get_session
from quartet_conductor.models import InputMap
from enum import Enum

class ContextKeys(Enum):
    """
    INPUT_NUMBER
    ------------
    Represents and IO block input.  This number will be sent into the rule
    via the capture interface and will be processed and placed on the
    RuleContext by the GetInputStep
    """
    INPUT_NUMBER = 'INPUT_NUMBER'

class InvalidInputError(Exception):
    """
    Raised when a bad input (above or below the avialable number of inputs (16))
    has been sent into the rule.
    """
    pass

class TemplateStep(TS):

    def execute(self, data, rule_context: RuleContext):
        ret = super().execute(data, rule_context)
        self.info('Converting the return text to ASCII')
        return ret.encode('ascii')

class GetSessionStep(rules.Step):
    """
    This step assumes that the data passed into the capture
    rule contains a single digit representing an IO port on a DIO
    module.  This digit will be placed on the context under the
    INPUT_NUMBER context key.
    """

    def execute(self, data, rule_context: RuleContext):
        self.info('Processing data %s', data)
        input = int(data)
        self.check_input(input)
        input_map = self.get_input_map(input)
        self.check_input(input_map.related_session_input)
        session = get_session(input_map.related_session_input)
        rule_context.context = session.context
        rule_context.context[ContextKeys.INPUT_NUMBER.value] = input
        self.info('Session context %s', rule_context)
        return data

    def check_input(self, input):
        if input < 1 or input > 16:
            raise InvalidInputError('%s is not a valid input.  Check your '
                                    'inbound input and your related input '
                                    'on your input map to ensure that the '
                                    'number is between one and 16.' % input)

    @property
    def declared_parameters(self):
        return {}

    def on_failure(self):
        pass

    def get_input_map(self, input: int):
        try:
            input_map = InputMap.objects.get(
                input_number=input
            )
            if input_map.related_session_input == None:
                raise InvalidInputError(
                    'The Input Map defined for this input (%s), does not '
                    'have a related session input defined.  Please define '
                    'the input that is responsible for starting a print '
                    'session.' % input
                )
            return input_map
        except InputMap.DoesNotExist:
            raise InvalidInputError('There is no input map defined for input '
                                    '%s' % input)


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



