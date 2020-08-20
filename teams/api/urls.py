from django.urls import path

from . import views

urlpatterns = [
    path('team-players/<int:team_id>', views.list_players_api_view),
    path('team-details/<int:team_id>', views.get_team_details_api_view),
    path('team-record/<int:team_id>/<str:place>', views.get_team_record_api_view),
    path('best-team-players/<int:team_id>/<int:percentile>', views.get_best_team_players_api_view)
]