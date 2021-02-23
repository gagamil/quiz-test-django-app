import json
from django.db import models


DEF_CHAR_FIELD_LENGTH = 200


class Poll(models.Model):
    title = models.CharField(max_length=DEF_CHAR_FIELD_LENGTH)
    start_date = models.DateField()
    finish_date = models.DateField()
    description = models.TextField()

class PollQuestion(models.Model):
    '''
    Holds common question data
    -   answer_choices: will hold the options for answer. 
        Might be Single or Multiple choices (held in the same JSON field as: 
        choiceType: 'SNGL' or 'MLTPL')
        If field empty means that answer should be Text.
    '''
    # TXT = 0
    SNGL = 1
    MLTPL = 2

    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)

    title = models.CharField(max_length=DEF_CHAR_FIELD_LENGTH)

    answer_choices = models.JSONField(null=True, blank=True)

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