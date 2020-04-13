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
# .
from quartet_capture.models import Rule, Step, StepParameter
from quartet_conductor.models import InputMap
from quartet_templates.models import Template
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
import os

class Command(BaseCommand):
    help = _('Will create the rule, steps and logic necessary to initialize '
             'a microscan reader.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            help='Delete any maps and overwrite.'
        )

    def handle(self, *args, **options):
        answer = options['delete']
        if answer:
            pass


        # put the session context on the context

        # render the label

        # send the label to the printer

        # create the input map

        # map this input to the rule created above
        InputMap.objects.create(

        )


