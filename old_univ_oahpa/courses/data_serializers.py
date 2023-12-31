from rest_framework import serializers

from .models import ( CourseGoal
                    , Goal
                    , GoalParameter
                    , UserFeedbackLog
                    , UserGoalInstance
                    , CourseGoalGoal
                    )

__all__ = [
    'GoalParamSerializer',
    'GoalSerializer',
    'FeedbackLogSerializer',
    'StatusSerializer',
    'CourseGoalSerializer',
    'NotificationSerializer',
]

class GoalParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalParameter
        fields = ('parameter', 'value')

# TODO: edit/put
class GoalSerializer(serializers.ModelSerializer):
    begin_url = serializers.CharField(source='begin_url', read_only=True)
    assigned = serializers.CharField(source='assigned', read_only=True)
    params = GoalParamSerializer(many=True)
    # TODO: validate that name and desc aren't empty

    def transform_params(self, obj, value):
        """ Need to switch all these to dictionaries
        """
        if value is not None:
            return dict([(p.get('parameter'), p.get('value')) for p in value])
        return None

    class Meta:
        model = Goal
        fields = ('id', 'short_name', 'begin_url', 'course', 'params',
                  'main_type', 'sub_type', 'threshold', 'assigned',
                  'minimum_sets_attempted', 'correct_first_try')

class CourseGoalGoalSerializer(serializers.ModelSerializer):

    goal = GoalSerializer()

    class Meta:
        model = CourseGoalGoal
        fields = ('goal', )

class CourseGoalSerializer(serializers.ModelSerializer):

    goals = CourseGoalGoalSerializer(many=True, required=False)
    combined_name = serializers.CharField(source='combined_name', read_only=True)
    percent_goals_completed = serializers.FloatField(source='percent_goals_completed')

    def transform_goals(self, obj, value):
        # Remove the wrapping of {'goal': {}}
        if value is not None:
            value = [v.get('goal') for v in value]
        return value

    class Meta:
        model = Goal
        fields = ('id', 'course', 'created_by', 'short_name',
                  'combined_name', 'goals', 'threshold',
                  'percent_goals_completed')

class FeedbackLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFeedbackLog
        fields = ('feedback_texts', 'user_input', 'correct_answer', 'datetime', 'user')

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserGoalInstance
        fields = ('progress', 'rounds', 'total_answered', 'correct',
                  'last_attempt', 'grade', 'correct_first_try',
                  'is_complete')

from notifications.models import Notification

from django.contrib.contenttypes.models import ContentType

class TaggedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_native(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        from django.contrib.auth.models import User
        if isinstance(value, User):
            return 'User: ' + value.username
        raise Exception('Unexpected type of tagged object')

class NotificationSerializer(serializers.ModelSerializer):

    actor = TaggedObjectRelatedField('actor')

    class Meta:
        model = Notification
        fields = ('recipient',
                  'description',
                  'actor',
                  'target_object_id',
                  'level',
                  'public',
                  'recipient',
                  'timestamp',
                  'unread',
                  'id',
                  'verb',)
