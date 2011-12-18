# from univ_oahpa.courses.models import CourseMembership
from django.contrib.auth.models import User, Group
from models import UserProfile
from django.db.models import Avg, Max, Min, Count

# This causes an error on sync with a fresh db, so catch the error because this
# group does not need to be created if the script is called from the
# commandline.
from django.db.utils import DatabaseError

try: 
	instructor_group = Group.objects.get(name='Instructors')
except DatabaseError:
	pass
except Group.DoesNotExist:
	instructor_group = Group.objects.create(name='Instructors')
	root = User.objects.get(pk=1)
	instructor_group.user_set.add(root)
	instructor_group.save()

# Problems when using loaddata, which we may want to use more often.
try:
	from functools import wraps
except ImportError:
	from django.utils.functional import wraps

import inspect

def disable_for_loaddata(signal_handler):
	""" Disable a function when Django is called via loaddata.
	"""
	@wraps(signal_handler)
	def wrapper(*args, **kwargs):
		for fr in inspect.stack():
			if inspect.getmodulename(fr[1]) in ['loaddata', 'manage']:
				return
		signal_handler(*args, **kwargs)
	return wrapper

@disable_for_loaddata
def aggregate_grades(sender, **kwargs):
	""" This aggregates all of the users grades into a UserGradeSummary
		which will then be displayed to instructors.
	""" 

	grade_object = kwargs['instance']
	prof = grade_object.user
	activity = grade_object.game

	gradesummary, _ = prof.usergradesummary_set.get_or_create(game=activity)
	grades = prof.usergrade_set.filter(game=activity)
	game_count = grades.count()

	if game_count > 0:
		stats = grades.aggregate(grade_max=Max('score'),
								grade_min=Min('score'),
								grade_avg=Avg('score'))

		gradesummary.average = stats['grade_avg']
		gradesummary.maximum = stats['grade_max']
		gradesummary.minimum = stats['grade_min']
		gradesummary.count = game_count
		gradesummary.save()

@disable_for_loaddata
def create_profile(sender, **kwargs):
	""" This signal creates UserProfile objects when the Django
		user models are saved.
	"""
	user_obj = kwargs['instance']
	profile, created = UserProfile.objects.get_or_create(user=user_obj)
	if created:
		profile.save()
	return True

@disable_for_loaddata
def grant_admin(sender, **kwargs):
	""" Course instructors gain access via is_staff. If extra permissions
		need to be assigned, this should be done here.
	"""

	course = kwargs['instance']
	instructors = course.courserelationship_set.filter(relationship_type__name='Instructors')
	instructors = [i.user for i in instructors]

	for i in instructors:
		i.is_staff = True
		i.groups.add(instructor_group)
		i.save()
	
	return True

@disable_for_loaddata
def copy_date(sender, **kwargs):
	""" Copy the date from the user's course, if it exists. If the date
	existent on the object is not the same as the course, we assume that a user
	has modified it and will not copy the date over.
	
	The model is only saved if a change has been made, that way there is no
	endless loop. """

	courserelationship = kwargs['instance']
	course = courserelationship.course
	user = courserelationship.user
	previous = courserelationship.end_date

	if course.end_date:
		# if these are not equal, must assume a user is modifying the date
		# to not be the course end date, so we don't want to change it.
		if courserelationship.end_date != course.end_date:
			return False
		courserelationship.end_date = course.end_date
	
	if previous != courserelationship.end_date:
		courserelationship.save()

	return True
	
@disable_for_loaddata
def user_presave(sender, instance, **kwargs):
	""" Increments user login count.
	"""
	user = instance
	
	try:
		userprofile = instance.get_profile()
	except UserProfile.DoesNotExist:
		return False
	
	try:
		if instance.last_login:
			old = instance.__class__.objects.get(pk=instance.pk)
			if instance.last_login != old.last_login:
				userprofile.userlogin_set.create(timestamp=instance.last_login)
	
		userprofile.login_count = userprofile.userlogin_set.all().count()
		userprofile.last_login = user.last_login
		userprofile.save()
	except User.DoesNotExist:
		pass
	
	return True

