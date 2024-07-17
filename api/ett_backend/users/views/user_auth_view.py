from rest_framework import generics
from rest_framework.permissions import AllowAny
# from users.serializers import UserLogoutSerializer, UserDeleteSerializer
from rest_framework.response import Response
from rest_framework import status

# class UserLogoutView(generics.GenericAPIView):
#     serializer_class = UserLogoutSerializer
#     permission_classes = [AllowAny] #[IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         response = Response(
#             data={
#                 "message": "Logout successful"
#             },
#             status=status.HTTP_204_NO_CONTENT
#         )
#
#         response.delete_cookie("JWT_AUTH_ACCESS_COOKIE")
#         response.delete_cookie("JWT_AUTH_REFRESH_COOKIE")
#
#         return response
#
#
# class UserDeleteView(generics.GenericAPIView):
#     serializer_class = UserDeleteSerializer
#     permission_classes = [AllowAny] # [IsAuthenticated]
#
#     def delete(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         user = serializer.validated_data["user"]
#         user.delete()
#
#         response = Response(
#             data={
#                 "message": "User deleted successfully"
#             },
#             status=status.HTTP_204_NO_CONTENT
#         )
#
#         response.delete_cookie("JWT_AUTH_ACCESS_COOKIE")
#         response.delete_cookie("JWT_AUTH_REFRESH_COOKIE")
#
#         return response
