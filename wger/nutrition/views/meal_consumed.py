# -*- coding: utf-8 -*-

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

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy
from django.views.generic import CreateView, UpdateView

from wger.nutrition.forms import MealConsumedForm
from wger.nutrition.models import Meal, MealConsumed
from wger.utils.generic_views import WgerFormMixin


logger = logging.getLogger(__name__)


class MealConsumedCreateView(WgerFormMixin, CreateView):
    '''
    Generic view to create a new meal consumed
    '''

    model = MealConsumed
    form_class = MealConsumedForm
    template_name = 'meal_consumed/form.html'

    def dispatch(self, request, *args, **kwargs):
        '''
        Check that the user owns the meal
        '''
        meal = get_object_or_404(Meal, pk=kwargs['meal_id'])
        if meal.plan.user == request.user:
            self.meal = meal
            return super(MealConsumedCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('nutrition:plan:view', kwargs={'id': self.meal.plan.id})

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(MealConsumedCreateView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('nutrition:meal_consumed:add',
                                         kwargs={'meal_id': self.meal.id})
        context['ingredient_searchfield'] = self.request.POST.get('ingredient_searchfield', '')
        return context

    def form_valid(self, form):
        '''
        Manually set the corresponding meal
        '''
        form.instance.meal = self.meal
        form.instance.order = 1
        return super(MealConsumedCreateView, self).form_valid(form)


class MealConsumedEditView(WgerFormMixin, UpdateView):
    '''
    Generic view to update an existing meal consumed
    '''

    model = MealConsumed
    form_class = MealConsumedForm
    title = ugettext_lazy('Edit meal item')
    form_action_urlname = 'nutrition:meal_consumed:edit'
    template_name = 'meal_consumed/form.html'

    def get_success_url(self):
        return reverse('nutrition:plan:view', kwargs={'id': self.object.meal.plan.id})


@login_required
def delete_meal_consumed(request, meal_consumed_id):
    '''
    Deletes the meal consumed with the given ID
    '''

    # select the meal consumed
    meal_consumed = get_object_or_404(MealConsumed, pk=meal_consumed_id)
    plan = meal_consumed.meal.plan

    #  Delete if the user is the owner
    if plan.user == request.user:
        meal_consumed.delete()
        return HttpResponseRedirect(reverse('nutrition:plan:view', kwargs={'id': plan.id}))
    else:
        return HttpResponseForbidden()
