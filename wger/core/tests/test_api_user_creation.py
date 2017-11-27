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

import logging

from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token

from wger.core.tests.base_testcase import WorkoutManagerTestCase

logger = logging.getLogger(__name__)


class RegistrationTestCase(WorkoutManagerTestCase):
    '''
    Tests registering a new user via API
    '''

    def setUp(self):
        '''
        Register and sign in an api user
        '''
        # login a user
        self.user_login('admin')
        user = User.objects.get(username='admin')
        add_user = Permission.objects.get(codename='add_user')
        change_user = Permission.objects.get(codename='change_user')
        user.user_permissions.add(add_user)
        user.user_permissions.add(change_user)
        user.save()
        # get api key for user
        self.client.get(reverse('core:user:api-key'))
        self.api_key = Token.objects.get(user=user)

    def test_api_register(self):

        registration_data = {'username': 'myusername',
                             'password': 'secret',
                             'email': 'test@test.com'
                             }
        # hit registration endpoint with proper registration data
        response = self.client.post(
            '/api/v2/register/',
            data=registration_data,
            headers={'Authorization': "Token " + str(self.api_key)})
        self.assertEqual(response.status_code, 201)

    def test_api_register_missing_field(self):

        registration_data = {
            'username': 'myusername',
            'email': 'myemail@mail.com'
        }
        # hit registration endpoint with incomplete data
        response = self.client.post(
            '/api/v2/register/',
            data=registration_data,
            headers={'Authentication': 'Token ' + str(self.api_key)}
        )
        self.assertEqual(response.status_code, 400)
