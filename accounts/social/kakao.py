import requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User

class KakaoOAuth2:
    """
    카카오 소셜 로그인 처리 클래스
    """
    def get_user_info(self, access_token):
        """
        카카오 액세스 토큰으로 사용자 정보 조회
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        
        # 카카오 사용자 정보 요청
        response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
        response.raise_for_status()
        user_data = response.json()
        
        # 필요한 정보 추출
        kakao_id = user_data.get('id')
        kakao_account = user_data.get('kakao_account', {})
        profile = kakao_account.get('profile', {})
        
        user_info = {
            'social_id': str(kakao_id),
            'email': kakao_account.get('email'),
            'nickname': profile.get('nickname'),
            'profile_image': profile.get('profile_image_url')
        }
        
        return user_info
    
    def login_or_create_user(self, user_info):
        """
        사용자 정보로 로그인 또는 회원가입 처리
        """
        social_id = user_info.get('social_id')
        
        # 기존 사용자 확인
        try:
            user = User.objects.get(social_provider='kakao', social_id=social_id)
        except User.DoesNotExist:
            # 새 사용자 생성
            email = user_info.get('email', f'kakao_{social_id}@example.com')
            username = f'kakao_{social_id}'
            
            user = User.objects.create(
                username=username,
                email=email,
                social_provider='kakao',
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