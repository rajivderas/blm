from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from players.models import Player, UserRole
from players.api.serializers import PlayerSerializer

from games.api.serializers import PlayerStatSerializer


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_player_details_api_view(request, player_id=None):
    user_id = request.user.id
    user_role = get_object_or_404(UserRole, user_id=user_id)

    if user_role.role.type != 'P':
        player = get_object_or_404(Player, id=player_id)
        serializer = PlayerSerializer(player)
        return JsonResponse({'player': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': "Accsess Denied."}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_player_game_stats_api_view(request, player_id=None):
    user_id = request.user.id
    user_role = get_object_or_404(UserRole, user_id=user_id)

    if user_role.role.type != 'P':
        player = get_object_or_404(Player, id=player_id)
        stats = player.game_stats()
        serializer = PlayerStatSerializer(stats)
        return JsonResponse({'player_stats': serializer.data}, safe=False,
                            status=status.HTTP_200_OK)

    else:
        return JsonResponse({'error': "Accsess Denied."}, status=status.HTTP_403_FORBIDDEN)
