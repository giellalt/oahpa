# -*- coding: utf-8 -*-

# TODO: middleware for watching for displaying the survey
#
#  - must consider option that multiple surveys could be present at
#    any time
#
#  - must consider that existing users who haven't been surveyed
#    need to be surveyed on some login

from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group

##
## Survey
##

question_types = [
    ('text', 'freeform text',),
    ('choice', 'single choice',),
    ('multichoice', 'multiple choice',),
    ('boolean', 'yes/no',),
]

## Survey definition

class Survey(models.Model):
    """ Main survey object
    """
    title = models.CharField(max_length=50)
    description = models.TextField()

    # TODO: target a particular course or courses, or all users.

    def __unicode__(self):
        return self.title

    def serialize_survey(self):
        """ Return a list of lists representing rows and columns of a CSV.
        """
        questions = [(a.id, a.question_text, a.question_type) for a in
                     self.questions.all().order_by('id')]

        question_columns = ["%s (%s)" % (text.encode('utf-8'), _type.encode('utf-8'))
                            for (_id, text, _type) in questions]

        columns = [
            'user',
            'completed',
        ] + question_columns

        answer_rows = []

        responses = self.usersurvey_set.all()

        for r in responses:
            answers = r.user_answers.all().order_by('id')
            user_answer_values = []

            for (q, text, _type) in questions:
                ans = answers.filter(question_id=q)
                # TODO: answers are currently the choice IDs, need to grab
                # proper answer for these.

                # TODO: if question type is freeform, serialize answer,
                # otherwise confirm that it's an int and search for the
                # answer value.
                if ans.exists():
                    user_answer_values.append(ans[0].answer_text.encode('utf-8'))
                else:
                    user_answer_values.append("NO ANSWER")

            row = [
                r.user_anonymized,
                r.completed.strftime('%Y.%d.%m'), # strftime
            ] + user_answer_values

            answer_rows.append(row)

        all_rows = [columns] + answer_rows
        return all_rows

TYPE_H = """<strong>NB</strong>: For single and multiple choice
answers, you must specify answer options. Yes/no and Freeform need no
choices. """

class SurveyQuestion(models.Model):
    """ Contains the survey question, and question type. Connects to any
    possible answer objects.
    """
    # TODO: Internationalization language
    survey = models.ForeignKey('Survey', related_name='questions')

    # required boolean field

    required = models.BooleanField(default=True)

    question_text = models.TextField()
    question_type = models.CharField(max_length=18, choices=question_types, help_text=TYPE_H)

    def __unicode__(self):
        if len(self.question_text) > 15:
            return "%s: %s" % (self.survey, self.question_text[0:15])
        else:
            return "%s: %s" % (self.survey, self.question_text)

# TODO: translation

#   https://github.com/deschler/django-modeltranslation
#   https://github.com/Yaco-Sistemas/django-transmeta/
#   https://pythonhosted.org/django-translatable/

# class SurveyQuestionTranslations(models.Model):
#     question = models.ForeignKey('SurveyQuestion')
#
#     language = models.CharField(max_length=5)
#     text = models.TextField()

class SurveyQuestionAnswerValue(models.Model):
    """ A model for defining answer values for question types that allow
    for a choice. UserSurveyQuestionAnswer will only be auto-populated
    from this, not related by foreignkey
    """
    question = models.ForeignKey(SurveyQuestion, related_name='answer_values')
    answer_text = models.TextField()

    def __unicode__(self):
        return "(%s) %s: %s" % (self.question.question_type,
                                self.question.question_text,
                                self.answer_text)

## User survey results

class UserSurvey(models.Model):
    """ This is the user survey instance, to connect individual user
    answers together.
    """
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)
    # TODO: anonymize user in export process
    # TODO: store anonymized by hash, prevent duplicates by checking
    # unique on hash.

    completed = models.DateTimeField(auto_now_add=True)

    @property
    def user_anonymized(self):
        return abs(hash(self.user.username))

    class Meta:
        unique_together = ('user', 'survey', )

class UserSurveyQuestionAnswer(models.Model):
    """ This object will store user answers, regardless of whether it
    comes from a database-specified choice, or user-entered free text.
    """

    user_survey = models.ForeignKey(UserSurvey, related_name="user_answers")
    question = models.ForeignKey(SurveyQuestion)
    answer_text = models.TextField()
