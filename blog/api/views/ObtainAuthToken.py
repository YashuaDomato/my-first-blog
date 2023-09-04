from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as exc:
            if "Unable to log in with provided credentials" in str(exc):
                return Response({"message": "Invalid username/password"}, status=HTTP_400_BAD_REQUEST)
            else:
                raise

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

login = CustomAuthToken.as_view()

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(request)
        print(f"User {request.user}")
        user_token = Token.objects.get(user=request.user)
        user_token.delete()

        # Perform your logout logic here (e.g., logout the user from the session)

        return Response({"message": "Logged out successfully"})

logout  = LogoutView.as_view()





