import requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User

class NaverOAuth2:
    """
    네이버 소셜 로그인 처리 클래스
    """
    def get_user_info(self, access_token):
        """
        네이버 액세스 토큰으로 사용자 정보 조회
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        # 네이버 사용자 정보 요청
        response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
        response.raise_for_status()
        user_data = response.json()
        
        # 응답 확인
        if user_data.get('resultcode') != '00':
            raise Exception(f"네이버 API 오류: {user_data.get('message')}")
        
        # 필요한 정보 추출
        response_data = user_data.get('response', {})
        
        user_info = {
            'social_id': response_data.get('id'),
            'email': response_data.get('email'),
            'nickname': response_data.get('nickname'),
            'profile_image': response_data.get('profile_image')
        }
        
        return user_info
    
    def login_or_create_user(self, user_info):
        """
        사용자 정보로 로그인 또는 회원가입 처리
        """
        social_id = user_info.get('social_id')
        
        # 기존 사용자 확인
        try:
            user = User.objects.get(social_provider='naver', social_id=social_id)
        except User.DoesNotExist:
            # 새 사용자 생성
            email = user_info.get('email', f'naver_{social_id}@example.com')
            username = f'naver_{social_id}'
            
            user = User.objects.create(
                username=username,
                email=email,
                social_provider='naver',
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