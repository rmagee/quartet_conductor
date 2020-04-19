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

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from quartet_capture.models import Rule, Step


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
            qs = Rule.objects.filter(name='VideoJet Print')
            print('Deleting %s Rules' % qs.count())
            qs.delete()

        # create the print label rule
        print_rule = Rule.objects.create(
            name='VideoJet Print',
            description='Sends a print command to a videojet printer.'
        )
        # look up the IO map to get the session id to use, then place
        # the session's context on the rule context
        get_io_map_step = Step.objects.create(
            name='Get Session',
            description='Use the IO map for the inbound IO port to grab an '
                        'active printing session.',
            step_class='quartet_conductor.steps.GetSessionStep',
            order=5,
            rule=print_rule
        )
        # render the label
        render_label_step = Step.objects.create(
            name='Send Printer Commands',
            description='Sends the serial number and print command to the '
                        'printer.',
            step_class='quartet_conductor.videojet.steps.PrintLabelStep',
            order=10,
            rule=print_rule
        )

