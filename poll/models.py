import json
from django.db import models
from django.utils import timezone as dt


DEF_CHAR_FIELD_LENGTH = 200


class ClientPollManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            start_date__gte=dt.localdate(),
            finish_date__gte=dt.localdate()
            )


class Poll(models.Model):
    title = models.CharField(max_length=DEF_CHAR_FIELD_LENGTH)
    start_date = models.DateField()
    finish_date = models.DateField()
    description = models.TextField()

    objects = models.Manager()
    client_objects = ClientPollManager()

    @property
    def ordered_question_ids(self):
        return self.get_pollquestion_order()

    @property
    def questions_json(self):
        json_data = []
        for question in self.pollquestion_set.all():
            json_data.append({'pollTemplateQuestionId':question.pk, 'title':question.title, 'choices':question.answer_choices})
        return json_data

    
class PollQuestion(models.Model):
    '''
    Holds common question data
    -   answer_choices: will hold the options for answer. 
        Might be Single or Multiple choices (held in the same JSON field as: 
        choiceType: 'SNGL' or 'MLTPL')
        If field empty means that answer should be Text.
    If we need to evaluate the user response then answer_choices should have some flag that would 
    set the weight to the answer. Not implemented because has not been specced.
    '''
    # TXT = 0
    SNGL = 1
    MLTPL = 2

    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)

    title = models.CharField(max_length=DEF_CHAR_FIELD_LENGTH)
    
    answer_choices = models.JSONField(null=True, blank=True)

    class Meta:
        order_with_respect_to = 'poll'

    @property
    def choice_type(self):
        if self.answer_choices:
            answer_choices = json.loads(self.answer_choices)
            return answer_choices.get('choiceType', None)
        return None

    # class Meta:
    #     abstract = True
    # question_type = models.CharField(max_lenght=5, choices=(('TXT', 'Text'), ('SNGL', 'Single choice'), ('MLT', 'Multi choice')))


# class TextPollQuestion(PollQuestion):
#     pass


# class SNGLPollQuestion(PollQuestion):
#     '''
#     Would have 1 or more options to choose from.
#     Usage: Poll may select only one of the options
#     '''
#     options = models.ManyToManyField('PollQuestionOption')


# class MLTPLPollQuestion(PollQuestion):
#     '''
#     Would have 1 or more options to choose from.
#     Usage: Poll may select one ore more of the options
#     '''
#     options = models.ManyToManyField('PollQuestionOption')


# class PollQuestionOption(PollQuestion):
#     '''
#     The question oprion in case of SingleChoice or MultipleChoice
#     '''
#     option_body = models.CharField(max_length=DEF_CHAR_FIELD_LENGTH)