import requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User

class GoogleOAuth2:
    """
    구글 소셜 로그인 처리 클래스
    """
    def get_user_info(self, access_token):
        """
        구글 액세스 토큰으로 사용자 정보 조회
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        # 구글 사용자 정보 요청
        response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers)
        response.raise_for_status()
        user_data = response.json()
        
        # 필요한 정보 추출
        user_info = {
            'social_id': user_data.get('sub'),
            'email': user_data.get('email'),
            'nickname': user_data.get('name'),
            'profile_image': user_data.get('picture')
        }
        
        return user_info
    
    def login_or_create_user(self, user_info):
        """
        사용자 정보로 로그인 또는 회원가입 처리
        """
        social_id = user_info.get('social_id')
        
        # 기존 사용자 확인
        try:
            user = User.objects.get(social_provider='google', social_id=social_id)
        except User.DoesNotExist:
            # 새 사용자 생성
            email = user_info.get('email', f'google_{social_id}@example.com')
            username = f'google_{social_id}'
            
            user = User.objects.create(
                username=username,
                email=email,
                social_provider='google',
                social_id=social_id,
                nickname=user_info.get('nickname'),
                profile_image=user_info.get('profile_image')
            )
            
            # 이메일이 있는 경우 인증된 것으로 처리
            if user_info.get('email'):
                user.is_active = True
                user.save()
        
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'nickname': user.nickname,
                'profile_image': user.profile_image
            }
        } 