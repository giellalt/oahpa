from django.template import RequestContext
from django.shortcuts import render
import datetime

from rusfeedback.models import FeedbackForm


def feedback(request):
	"""
		Form submit view which creates feedback entry in database. 
	"""
	
	context = {}
	
	if request.method == 'POST':
		feedback_form = FeedbackForm(request.POST) # A form bound to the POST data
		
		if feedback_form.is_valid():
			feedback_form.save(commit=False)
			
			feedback_form.date = datetime.date.today()
			today = datetime.date.today()
			
			feedback_form.save()
		
	else:
		feedback_form = FeedbackForm()
	
	template = 'feedback.html'
	context['form'] = feedback_form
	
	return render(request, template, context)

