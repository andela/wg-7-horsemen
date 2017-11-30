# -*- coding: utf-8 *-*

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import datetime

from django.utils.timezone import now
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission


class Command(BaseCommand):
    '''
    Helper admin command to allow users to create users
    '''

    help = 'Allow user to create users via api '

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

        # optional arguments
        parser.add_argument(
            '--disable',
            action='store_true',
            dest='disable',
            default=False,
            help='Disable permission to create users via API'
        )

    def handle(self, **options):

        for username in options['username']:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError('User  "%s" does not exist' % username)

            permission1 = Permission.objects.get(codename='add_user')
            permission2 = Permission.objects.get(codename='change_user')

            if options['disable']:
                user.user_permissions.remove(permission1)
                user.user_permissions.remove(permission2)
            else:
                user.user_permissions.add(permission1)
                user.user_permissions.add(permission2)

            user.save()

        self.stdout.write("User permissions have been updated")
