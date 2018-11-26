from django.conf import settings

def display_survey_notice(request):
    return {
        'display_survey_notice': request.session.get('display_survey_notice', False),
        'survey_ids_available': request.session.get('survey_ids_available', False),
    }
