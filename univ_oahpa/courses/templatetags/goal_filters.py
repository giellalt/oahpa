﻿from django import template

register = template.Library()

@register.filter(name='complete_for')
def complete_for(a, user):
    return a.user_completed(user)

@register.filter(name='goal_instances_for')
def goal_instances_for(goal, user):
    return goal.usergoalinstance_set.filter(user=user).order_by('-last_attempt')

@register.filter(name='format_percent')
def format_percent(_float):
    _perc = "%s" % round(_float, 2)
    return _perc + '%'

@register.filter(name='goals')
def goals(coursegoal):
    """ Return a list of goals, skipping the related thing. """
    return (c.goal for c in coursegoal.goals.all())

@register.filter(name='cumulative_progress')
def cumulative_progress(coursegoal, user):
    return coursegoal.progress_for(user)

@register.filter(name='goals_with_progress')
def goals_with_progress(coursegoal, student):
    """ Return a list of goals with user progress, skipping the related thing. """
    from courses.models import Goal
    user = student.user
    gs = []
    for g in Goal.objects.filter(coursegoalgoal__coursegoal=coursegoal):
        if len(g.usergoalinstance_set.filter(user_id=user.id)) > 0:
            gs.append(g)
    return gs
