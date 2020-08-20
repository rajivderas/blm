from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from games.api.serializers import GameSerializer, TeamStatSerializer
from games.models import Game, TeamStat, PlayerStat

from games.api.serializers import PlayerStatSerializer


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def list_all_games_api_view(request):
    user = request.user.id
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return JsonResponse({'all_games': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_team_stats_api_view(request, game_id=None):
    user = request.user.id
    game_team = get_object_or_404(TeamStat, game_id=game_id)
    print(game_team)
    team_stats = game_team.team_stats()
    serializer = TeamStatSerializer(team_stats)
    return JsonResponse({'team_stats': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_team_player_stats_api_view(request, game_id=None):
    user = request.user.id
    game_team = get_object_or_404(TeamStat, game_id=game_id)
    team_player_stats = game_team.team_players_stats()
    serializer = PlayerStatSerializer(team_player_stats, many=True)
    return JsonResponse({'team_player_stats': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_top_game_points_scorer_api_view(request, game_id=None):
    user = request.user.id
    game_team = get_object_or_404(TeamStat, game_id=game_id)
    top_scorers = game_team.top_game_points_scorer()

    return JsonResponse({'top_game_points_scorer': top_scorers}, safe=False, status=status.HTTP_200_OK)