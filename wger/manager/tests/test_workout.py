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

from django.core.urlresolvers import reverse

from wger.core.tests import api_base_test
from wger.core.tests.base_testcase import WorkoutManagerDeleteTestCase
from wger.core.tests.base_testcase import WorkoutManagerEditTestCase
from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.manager.models import Workout


class WorkoutShareButtonTestCase(WorkoutManagerTestCase):
    '''
    Test that the share button is correctly displayed and hidden
    '''

    def test_share_button(self):
        workout = Workout.objects.get(pk=1)

        response = self.client.get(workout.get_absolute_url())
        self.assertFalse(response.context['show_shariff'])

        self.user_login('admin')
        response = self.client.get(workout.get_absolute_url())
        self.assertTrue(response.context['show_shariff'])

        self.user_login('test')
        response = self.client.get(workout.get_absolute_url())
        self.assertFalse(response.context['show_shariff'])


class WorkoutAccessTestCase(WorkoutManagerTestCase):
    '''
    Test accessing the workout page
    '''

    def test_access_shared(self):
        '''
        Test accessing the URL of a shared workout
        '''
        workout = Workout.objects.get(pk=1)

        self.user_login('admin')
        response = self.client.get(workout.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.user_login('test')
        response = self.client.get(workout.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.user_logout()
        response = self.client.get(workout.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_access_not_shared(self):
        '''
        Test accessing the URL of a private workout
        '''
        workout = Workout.objects.get(pk=3)

        self.user_login('admin')
        response = self.client.get(workout.get_absolute_url())
        self.assertEqual(response.status_code, 403)

        self.user_login('test')
        response = self.client.get(workout.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.user_logout()
        response = self.client.get(workout.get_absolute_url())
        self.assertEqual(response.status_code, 403)


class AddWorkoutTestCase(WorkoutManagerTestCase):
    '''
    Tests adding a Workout
    '''

    def create_workout(self):
        '''
        Helper function to test creating workouts
        '''

        # Create a workout
        count_before = Workout.objects.count()
        response = self.client.get(reverse('manager:workout:add'))
        count_after = Workout.objects.count()

        # There is always a redirect
        self.assertEqual(response.status_code, 302)

        # Test creating workout
        self.assertGreater(count_after, count_before)

        # Test accessing workout
        response = self.client.get(reverse('manager:workout:view', kwargs={'pk': 1}))

        workout = Workout.objects.get(pk=1)
        self.assertEqual(response.context['workout'], workout)
        self.assertEqual(response.status_code, 200)

    def test_create_workout_logged_in(self):
        '''
        Test creating a workout a logged in user
        '''

        self.user_login()
        self.create_workout()
        self.user_logout()


class ExportWorkoutTestCase(WorkoutManagerTestCase):
    '''
    Tests exporting a Workout
    '''

    def export_workout(self):
        '''
        Helper function to test exporting workouts
        '''

        # Create a workout
        self.client.get(reverse('manager:workout:add'))

        ui_response = self.client.get(reverse('manager:workout:export', kwargs={'pk': 1}))

        # Test that the export form was rendered
        self.assertEqual(ui_response.status_code, 200)
        self.assertIn(
            b'<input type="submit" value="Export" id="form-save" class="btn btn-default btn-block"',
            ui_response.content
        )

        response = self.client.post(reverse('manager:workout:export', kwargs={'pk': 1}))
        # Test status
        self.assertEqual(response.status_code, 200)
        # Test content type
        self.assertIn(
            b'"model": "manager.workout"',
            response.content
        )

    def test_export_workout_logged_in(self):
        '''
        Test creating a workout a logged in user
        '''

        self.user_login()
        self.export_workout()
        self.user_logout()


class ExportAllWorkoutsTestCase(WorkoutManagerTestCase):
    '''
    Tests exporting all Workouts
    '''

    def export_all_workouts(self):
        '''
        Helper function to test exporting all workouts
        '''

        # Create a workout
        self.client.get(reverse('manager:workout:add'))

        ui_response = self.client.get(reverse('manager:workout:export_all'))

        # Test that the export form was rendered
        self.assertEqual(ui_response.status_code, 200)
        self.assertIn(
            b'<input type="submit" value="Export" id="form-save" class="btn btn-default btn-block"',
            ui_response.content
        )

        response = self.client.post(reverse('manager:workout:export_all'))
        # Test status
        self.assertEqual(response.status_code, 200)
        # Test content type
        self.assertIn(b'"model": "manager.workout"', response.content)

    def test_export_workout_logged_in(self):
        '''
        Test creating a workout a logged in user
        '''

        self.user_login()
        self.export_all_workouts()
        self.user_logout()


class ImportWorkoutsTestCase(WorkoutManagerTestCase):
    '''
    Tests importing Workouts
    '''

    def import_workouts(self):
        '''
        Helper function to test importing workouts
        '''

        # Create a workout
        self.client.get(reverse('manager:workout:add'))

        ui_response = self.client.get(reverse('manager:workout:wk_import'))

        # Test that the import form was rendered
        self.assertEqual(ui_response.status_code, 200)
        self.assertIn(
            b'<input type="submit" value="Import" id="form-save" class="btn btn-default btn-block"',
            ui_response.content
        )

    def test_import_workout_logged_in(self):
        '''
        Test creating a workout a logged in user
        '''

        self.user_login()
        self.import_workouts()
        self.user_logout()


class DeleteTestWorkoutTestCase(WorkoutManagerDeleteTestCase):
    '''
    Tests deleting a Workout
    '''

    object_class = Workout
    url = 'manager:workout:delete'
    pk = 3
    user_success = 'test'
    user_fail = 'admin'


class EditWorkoutTestCase(WorkoutManagerEditTestCase):
    '''
    Tests editing a Workout
    '''

    object_class = Workout
    url = 'manager:workout:edit'
    pk = 3
    user_success = 'test'
    user_fail = 'admin'
    data = {'comment': 'A new comment', 'cycle': 'Microcycle'}


class WorkoutOverviewTestCase(WorkoutManagerTestCase):
    '''
    Tests the workout overview
    '''

    def get_workout_overview(self):
        '''
        Helper function to test the workout overview
        '''

        response = self.client.get(reverse('manager:workout:overview'))

        # Page exists
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['workouts']), 2)

    def test_dashboard_logged_in(self):
        '''
        Test creating a workout a logged in user
        '''
        self.user_login()
        self.get_workout_overview()


class WorkoutModelTestCase(WorkoutManagerTestCase):
    '''
    Tests other functionality from the model
    '''

    def test_unicode(self):
        '''
        Test the unicode representation
        '''

        workout = Workout()
        workout.creation_date = datetime.date.today()
        self.assertEqual('{0}'.format(workout),
                         '{0} ({1})'.format(u'Workout', datetime.date.today()))

        workout.comment = u'my description'
        self.assertEqual('{0}'.format(workout), u'my description')


class WorkoutApiTestCase(api_base_test.ApiBaseResourceTestCase):
    '''
    Tests the workout overview resource
    '''
    pk = 3
    resource = Workout
    private_resource = True
    special_endpoints = ('canonical_representation',)
    data = {'comment': 'A new comment'}
