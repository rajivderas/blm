from django.urls import path

from . import views

urlpatterns = [
    path('team-stats/<int:game_id>', views.get_team_stats_api_view),
    path('all-games', views.list_all_games_api_view),
    path('team-player-stats/<int:game_id>', views.get_team_player_stats_api_view),
    path('top-game-points-scorer/<int:game_id>', views.get_top_game_points_scorer_api_view)
]