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

from django.contrib import admin
from quartet_conductor import models

class SessionAdmin(admin.ModelAdmin):
    model = models.Session
    search_fields = ['lot', 'expiry']

class InputMapAdmin(admin.ModelAdmin):
    model = models.InputMap
    search_fields = ['rule__name', 'input_number']
    list_display = ['rule', 'input_number', 'related_session_input']


def register_to_site(admin_site: admin.AdminSite):
    admin_site.register(models.Session, SessionAdmin)
    admin_site.register(models.InputMap, InputMapAdmin)
