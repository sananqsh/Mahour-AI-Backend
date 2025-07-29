from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    user_prompt = serializers.CharField(
        help_text='The text you want to send to the LLM.'
    )
    prompt_template = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Optional template using "{user_prompt}" to interpolate.'
    )
