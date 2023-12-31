from courses.models import create_activity_log_from_drill_logs
from django.contrib.auth.models import AnonymousUser

class GradingMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ Mark view as being able to be graded or not.
        """

        setattr(request, 'graded_view', False)

        if view_func.__module__.startswith('django.contrib.admin.'):
            setattr(request, 'graded_view', False)
        else:
            setattr(request, 'graded_view', True)

    def increment_session_answer_counts(self, request):

        # NB: Incrementing the session variable for set tried happens in

        # Increment individual question/answer tries

        for log in request.user_logs_generated:
            if log.correct in request.session['question_try_count']:
                # Increment and add to answered, thus count stops
                # incrementing after this round.
                if not request.session['answered'].get(log.correct,
                                                       False):
                    request.session['question_try_count'][log.correct] += 1
                    request.session['answered'][log.correct] = True
                else:
                    pass
            else:
                request.session['question_try_count'][log.correct] = 1

        request.session.modified = True
        return request

    def reset_increments(self, request):
        # If 'set_completed' is in the session variable, 
        # then need to clear variables for the next go around.

        new_set = request.session.get('new_game')
        prev_new_set = request.session['prev_new_game']
        new_sets = new_set and prev_new_set

        if request.session.get('set_completed', False) or new_sets:
            request.session['question_try_count'] = {}
            request.session['question_set_count'] += 1
            request.session['answered'] = {}

    def request_goal_instances(self, request):
        from .models import UserGoalInstance
        current_user_goal = request.session.get('current_user_goal', False)

        if not current_user_goal:
            return False

        return UserGoalInstance.objects.filter( user=request.user
                                              , id=current_user_goal
                                              , opened=True
                                              )\
                                       .order_by('-last_attempt')

    def exit_goal_tracking(self, request):
        """ If there's a problem deleting one of these keys there's
        something really wrong, no need for try blocks.
        """

        del request.session['current_user_goal']
        del request.session['current_exercise_params']
        del request.session['previous_exercise_params']

    def process_response(self, request, response):
        """ Here the goal is to process the grading that pertains to the
        user's current activity, which is marked on the session object,
        and store it in the courses activity log model. """

        from .models import Goal, UserGoalInstance

        # If there's no session, we can't do anything
        if not hasattr(request, 'session'):
            return response

        # Increment a variable to determine if the user has navigated
        # away.

        if request.session.get('navigated_away', False):
            if request.session['navigated_away'] > 0:
                request.session['navigated_away'] += 1
            if request.session['navigated_away'] > 2:
                request.session['navigated_away'] = 0

        if not hasattr(request, 'graded_view'):
            return response

        user_isnt_anon = request.user.is_authenticated()
        request_logs_exist = hasattr(request, 'user_logs_generated')

        current_user_goal = request.session.get('current_user_goal', False)

        if request_logs_exist and user_isnt_anon and current_user_goal:
            current = request.session.get('current_exercise_params', False)
            previous = request.session.get('previous_exercise_params', False)
            # This test is sometimes wrong when switching in and out of
            # a goal.
            if current and previous:
                is_sahka = ('sahka' in current) and ('sahka' in previous)
                is_vasta = ('vasta' in current) and ('vasta' in previous)

                same_dialogue = current.startswith(previous)
                sahka_condition = is_sahka and same_dialogue

                user_navigated_away = (current != previous) and (not sahka_condition)

                if user_navigated_away:
                    # print " -- user navigated to new page, stop tracking --"

                    user_goal_instance = self.request_goal_instances(request)

                    # Mark this instance as no longer being active.
                    if user_goal_instance is not None and len(user_goal_instance) > 0:
                        user_goal_instance[0].opened = False
                        user_goal_instance[0].save()

                    request.session['previous_exercise_params'] = current

                    self.exit_goal_tracking(request)

                    if request.session.get('navigated_away', False):
                        request.session['navigated_away'] += 1

                    return response

            self.increment_session_answer_counts(request)

            ual = create_activity_log_from_drill_logs(request, request.user,
                                                      request.user_logs_generated,
                                                      current_user_goal=current_user_goal)

            self.reset_increments(request)

            ugi = UserGoalInstance.objects.get(id=current_user_goal)
            goal = ugi.goal

            result = ugi.evaluate_instance()

            if result is not None:
                try: result.pop('progress_pretty')
                except: pass

                try: result.pop('correct_minus_first')
                except: pass

                try: result.pop('correct_later_tries')
                except: pass
                result['rounds'] = request.session['question_set_count']

                user_goal_instance = UserGoalInstance.objects.filter(user=request.user, goal=goal, opened=True)
                if not user_goal_instance:
                    UserGoalInstance.objects.create(user=request.user,
                                                    goal=goal, **result)
                else:
                    user_goal_instance.update(**result)

                complete = goal.is_complete(user_goal_instance[0])

        request.session['previous_exercise_params'] = \
                request.session.get('current_exercise_params', False)

        request.session['prev_new_game'] = \
                request.session.get('new_game', False)

        return response

# vim: set ts=4 sw=4 tw=72 syntax=python :
