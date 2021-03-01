from rest_framework import serializers

from .models import ClientPoll, ClientPollAnswer


USER_ID_FIELD_LENGTH = 40 # equals DRF auth token.key length - not brilliant but at least something...


class ClientPollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPollAnswer
        fields = ['client_poll', 'answer']

class ClientPollCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(min_length=USER_ID_FIELD_LENGTH, max_length=USER_ID_FIELD_LENGTH, required=True)
    class Meta:
        model = ClientPoll
        fields = ['poll_template', 'user']


class ClientPollAnswerCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(min_length=USER_ID_FIELD_LENGTH, max_length=USER_ID_FIELD_LENGTH, required=True)
    class Meta:
        model = ClientPollAnswer
        fields = ['client_poll', 'answer', 'user']
    
    def validate(self, data):
        """
        Check that answer questions match ClientPoll questions.
        """
        client_poll = data['client_poll']
        answers = data['answer']
        # print('ClientPollAnswerCreateSerializer::validate',client_poll.questions)
        if(len(client_poll.questions) != len(answers)):
            raise serializers.ValidationError("Not enough answers! Gimme more...")

        for answer in answers:
            search_id = answer['pollTemplateQuestionId']
            # print('search_id', search_id)
            question = next((x for x in client_poll.questions if x['pollTemplateQuestionId'] == search_id), None)
            # if question:
            #     print('question', question['pollTemplateQuestionId'])
            if not question:
                raise serializers.ValidationError("Sorry, no such poll question in this poll.")

        return data