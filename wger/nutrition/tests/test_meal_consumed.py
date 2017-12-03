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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.core.urlresolvers import reverse

from wger.core.tests.base_testcase import WorkoutManagerAddTestCase
from wger.core.tests.base_testcase import WorkoutManagerEditTestCase
from wger.nutrition.models import MealConsumed


class EditMealConsumedUnitTestCase(WorkoutManagerEditTestCase):
    '''
    Tests editing a meal consumed
    '''

    object_class = MealConsumed
    url = 'nutrition:meal_consumed:edit'
    pk = 4
    data = {'ingredient_consumed': 'Eggs and bacon'}


class AddMealConsumedUnitTestCase(WorkoutManagerAddTestCase):
    '''
    Tests adding a meal consumed
    '''

    object_class = MealConsumed
    url = reverse('nutrition:meal_consumed:add', kwargs={'meal_id': 3})
    data = {'ingredient_consumed': 'eggs and bacon'}
