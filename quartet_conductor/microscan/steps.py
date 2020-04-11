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

from enum import Enum

from quartet_capture import models
from quartet_capture.rules import RuleContext, Step
from quartet_conductor.videojet.steps import CONTEXT_FIELDS
from quartet_conductor.microscan.utils import convert_command_value


class CONTEXT_KEYS(Enum):
    """
    MATCH_STRING is the match string to send to the scanner to
    match barcode values against.
    """
    MATCH_STRING = 'match_string'


class MatchStringCommandStep(Step):
    """
    Converts the fields in the context into commands that the scanner
    will understand and places them on the context under the
    match_string key..
    """

    def __init__(self, db_task: models.Task, **kwargs):
        super().__init__(db_task, **kwargs)
        match_string_keys = self.get_or_create_parameter(
            'Match String Keys',
            'EXPIRY,LOT',
            'The fields to pull from the printer and '
            'send to the scanner as wildcard match '
            'strings.  They must be declared in the '
            'order in which you expect to see them '
            'in a barcode.'
        )
        self.match_string_keys = match_string_keys.split(',')

    def execute(self, data, rule_context: RuleContext):
        job_fields = rule_context.context.get(CONTEXT_FIELDS.JOB_FIELDS.value)
        match_string = ''
        for key in self.match_string_keys:
            match_string = '%s*%s' % (
                match_string, job_fields.get(key, '').strip())
        match_string += "*"
        if job_fields:
            rule_context.context[
                CONTEXT_KEYS.MATCH_STRING.value] = convert_command_value(
                match_string)
        return data

    @property
    def declared_parameters(self):
        return {'Match String Fields': 'A comma delimited list of fields to '
                                       'pull from the printer and use as '
                                       'match string data.'}

    def on_failure(self):
        self.info('On failured called.')
