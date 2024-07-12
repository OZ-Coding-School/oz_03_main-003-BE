from rest_framework import generics, permissions

from .models import User
from .serializers import UserProfileSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # 요청한 사용자를 반환하여 해당 사용자의 프로필을 조회 및 업데이트합니다.
        return self.request.user
