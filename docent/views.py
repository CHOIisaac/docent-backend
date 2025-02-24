from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_api(request):
    """
    프론트엔드 연동 테스트를 위한 간단한 API
    """
    data = {
        'message': '연동 테스트 성공!',
        'status': 'success',
        'data': {
            'items': [
                {'id': 1, 'name': '테스트 아이템 1'},
                {'id': 2, 'name': '테스트 아이템 2'},
                {'id': 3, 'name': '테스트 아이템 3'}
            ]
        }
    }
    return Response(data)
