from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

from .serializers import ChatSerializer
from .services import call_llm

logger = logging.getLogger(__name__)

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
        logger.info("POST request received to /api/chat/")
        logger.debug(f"Request data: {request.data}")
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_prompt = serializer.validated_data['user_prompt']
        prompt_template = serializer.validated_data.get('prompt_template')
        logger.info(f"Processing request - user_prompt: {user_prompt[:50]}...")
        logger.debug(f"Using prompt_template: {prompt_template}")

        try:
            llm_response = call_llm(user_prompt, prompt_template)
            logger.info("LLM call completed successfully")
            logger.debug(llm_response)
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response(
            {"response": llm_response},
            status=status.HTTP_200_OK
        )
