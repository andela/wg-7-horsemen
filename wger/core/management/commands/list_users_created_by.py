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
from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    Helper admin command to list all users created by a certain user via API
    '''

    help = 'list  all users created via API by a given user '

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, **options):

        for username in options['username']:
            try:
                user = User.objects.get(username=username)
                profiles = UserProfile.objects.filter(created_by=user)
            except User.DoesNotExist:
                raise CommandError('User  "%s" does not exist' % username)

            for profile in profiles:
                self.stdout.write("username: %s" % profile.user.username)
