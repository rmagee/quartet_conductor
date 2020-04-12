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
from quartet_capture.rules import Step
from quartet_capture.rules import RuleContext
from quartet_conductor.steps import TelnetStep
from enum import Enum

from logging import getLogger

logger = getLogger(__name__)


class ContextFields(Enum):
    """
    JOB FIELDS
    ==========
    Any job fields retrieved from the printer will be in the JOB_FIELDS
    context key

    PRINTER_HOST
    ============
    The printer host name will be added to the context under this value.

    PRINTER_PORT
    ============
    The TCP port of the text communications to the printer will be added
    to the context with this value as an integer.

    SERIAL_IDENTIFIER
    =================
    Usually the GTIN or SSCC/Company prefix field within a label.  This
    value is used to place a serialbox machine_name for a pool onto the
    context from a labe/job.

    IO_PORT
    =======
    If the printer will be responding to IO port input signals to print,
    then supply the IO block input number here.  This can be used by other
    components that need to access the printer to understand which printer to
    use when input signals are detected.

    """
    JOB_FIELDS = 'JOB_FIELDS'
    PRINTER_HOST = 'PRINTER_HOST'
    PRINTER_PORT = 'PRINTER_PORT'
    SERIAL_IDENTIFIER = 'SERIAL_IDENTIFIER'
    IO_PORT = 'IO_PORT'


class JobFieldsStep(TelnetStep):
    """
    Will issue a telnet command and then read the reply and return
    to the channel as the data.

    This Step will also add the printer host and port to the context along
    with the IO Port that it will respond to for print commands.
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
        self.input_port = int(self.get_or_create_parameter(
            'IO Port', '2',
            'The input port that the printer will respond to if applicable.'
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
            rule_context.context[ContextFields.JOB_FIELDS.value] = dict
            rule_context.context[ContextFields.PRINTER_HOST.value] = self.host
            rule_context.context[ContextFields.PRINTER_PORT.value] = self.port
            rule_context.context[ContextFields.IO_PORT.value] = self.input_port
            logger.info('Rule Context: %s', rule_context.context)
            self.info('%s: %s', __name__, rule_context.context)

    @property
    def declared_parameters(self):
        parms = super().declared_parameters()
        parms['IO Port'] = 'The input port that the printer will respond to ' \
                           'if applicable.'


class NoJobFieldsError(Exception):
    """
    Raised if no job fields are found in the context.
    """
    pass


class GetSerialIdentifierStep(Step):
    """
    Will pull out the serial identifer out of the printer data and put it
    on the context.  This is what is used by serialbox to pull out the
    serial numbers.
    """

    def __init__(self, db_task: models.Task, **kwargs):
        super().__init__(db_task, **kwargs)
        self.serial_identifier_field = self.get_or_create_parameter(
            "Serial Identifier Field", "GTIN",
            "The field that contains the GTIN or "
            "serial portion of the label being "
            "printed."
        )

    def execute(self, data, rule_context: RuleContext):
        job_fields = rule_context.context.get(ContextFields.JOB_FIELDS.value,
                                              None)
        if not job_fields:
            raise NoJobFieldsError('There are no job fields in the context.'
                                   ' Make sure the printer is communicating '
                                   'correctly and that your job fields '
                                   'match your configured step parameters.')
        serial_identifier = job_fields.get(self.serial_identifier_field, None)
        if not serial_identifier:
            raise NoJobFieldsError('The step could not find a job field '
                                   'with the key %s' %
                                   self.serial_identifier_field)
        self.info('Placing %s on the context for serial identifier',
                  serial_identifier)
        rule_context.context[
            ContextFields.SERIAL_IDENTIFIER.value] = serial_identifier
        return data

    def on_failure(self):
        pass

    @property
    def declared_parameters(self):
        return {
            "Serial Identifier Field": "The field that contains the GTIN or "
                                       "serial portion of the label being "
                                       "printed."
        }


class StartSessionStep(Step):
    """
    Clears out any existing sessions and starts a new one with the
    current printer, serial identifier and IO port ready for lookup.
    """

    def execute(self, data, rule_context: RuleContext):
        pass

    @property
    def declared_parameters(self):
        return {}

    def on_failure(self):
        self.info('On failured called.')
