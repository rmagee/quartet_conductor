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


class CONTEXT_FIELDS(Enum):
    """
    JOB FIELDS
    ==========
    Any job fields retrieved from the printer will be in the JOB_FIELDS
    context key

    PRINTER_HOST
    ====
    The printer host name will be added to the context under this value.

    PRINTER_PORT
    ============
    The TCP port of the text communications to the printer will be added
    to the context with this value as an integer.

    SERIAL IDENTIFIER
    =================
    Usually the GTIN or SSCC/Company prefix field within a label.  This
    value is used to place a serialbox machine_name for a pool onto the
    context from a labe/job.

    """
    JOB_FIELDS = 'JOB_FIELDS'
    PRINTER_HOST = 'PRINTER_HOST'
    PRINTER_PORT = 'PRINTER_PORT'
    SERIAL_IDENTIFIER = 'SERIAL_IDENTIFIER'


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
            rule_context.context[CONTEXT_FIELDS.PRINTER_HOST.value] = self.host
            rule_context.context[CONTEXT_FIELDS.PRINTER_PORT.value] = self.port
            logger.info('Rule Context: %s', rule_context.context)
            self.info('%s: %s', __name__, rule_context.context)


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
        job_fields = rule_context.context.get(CONTEXT_FIELDS.JOB_FIELDS.value,
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
            CONTEXT_FIELDS.SERIAL_IDENTIFIER.value] = serial_identifier
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
