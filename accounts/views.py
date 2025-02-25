from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .social.kakao import KakaoOAuth2
from .social.google import GoogleOAuth2
from .social.naver import NaverOAuth2

class SocialLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        provider = request.data.get('provider')
        access_token = request.data.get('access_token')
        
        if not provider or not access_token:
            return Response({
                'error': '제공자와 액세스 토큰이 필요합니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 소셜 로그인 제공자 선택
        social_auth = self._get_social_auth_provider(provider)
        if not social_auth:
            return Response({
                'error': '지원하지 않는 소셜 로그인입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 소셜 사용자 정보 조회
            user_info = social_auth.get_user_info(access_token)
            
            # 로그인 또는 회원가입 처리 및 JWT 토큰 발급
            token_data = social_auth.login_or_create_user(user_info)
            
            return Response(token_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_social_auth_provider(self, provider):
        """소셜 로그인 제공자 객체 반환"""
        if provider == 'kakao':
            return KakaoOAuth2()
        elif provider == 'google':
            return GoogleOAuth2()
        elif provider == 'naver':
            return NaverOAuth2()
        return None 