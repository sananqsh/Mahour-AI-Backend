from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ChatSerializer
from .services import call_llm

class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    """
    POST /api/chat/
    {
      "user_prompt": "Hello, how are you?",
      "prompt_template": "You are a funny assistant. {user_prompt}"
    }
    """
    def post(self, request, *args, **kwargs):
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_prompt = serializer.validated_data['user_prompt']
        history = serializer.validated_data.get('history')
        prompt_template = serializer.validated_data.get('prompt_template')

        try:
            llm_response = call_llm(user_prompt, prompt_template, history)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response(
            {"response": llm_response},
            status=status.HTTP_200_OK
        )
