from django.urls import path

from . import views

urlpatterns = [
    path('player-stats/<int:player_id>', views.get_player_game_stats_api_view),
    path('player-details/<int:player_id>', views.get_player_details_api_view),
]