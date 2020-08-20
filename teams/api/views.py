from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from teams.api.serializers import TeamSerializer
from players.api.serializers import PlayerSerializer
from teams.models import Team
from players.models import UserRole


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_team_details_api_view(request, team_id=None):
    user = request.user.id
    team = get_object_or_404(Team, id=team_id)
    serializer = TeamSerializer(team)

    return JsonResponse({'team': serializer.data },safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def list_players_api_view(request, team_id=None):
    user_id = request.user.id
    user_role = get_object_or_404(UserRole, user_id=user_id)
    if user_role.role.type != 'P':
        team = get_object_or_404(Team, id=team_id)
        players = team.list_players()
        serializer = PlayerSerializer(players, many=True)
        return JsonResponse({'players': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': "Accsess Denied."}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_team_record_api_view(request, team_id=None, place=None):
    user_id = request.user.id
    user_role = get_object_or_404(UserRole, user_id=user_id)
    if user_role.role.type != 'P':
        team = get_object_or_404(Team, id=team_id)
        try:
            team_record = team.win_loss_record(place)
            return JsonResponse({'team_record': team_record},
                                safe=False, status=status.HTTP_200_OK)
        except:
            return JsonResponse({"error": "Place set game location parameter as either 'home', 'away' or 'all'."},
                status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': "Accsess Denied."}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_best_team_players_api_view(request, team_id=None, percentile=None):
    user_id = request.user.id
    user_role = get_object_or_404(UserRole, user_id=user_id)
    if user_role.role.type != 'P':
        team = get_object_or_404(Team, id=team_id)
        best_players = team.best_players(percentile)
        serializer = PlayerSerializer(best_players, many=True)
        return JsonResponse({'best_players_in_' + str(percentile) + '_percentile' : serializer.data},safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': "Accsess Denied."}, status=status.HTTP_403_FORBIDDEN)