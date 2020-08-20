from rest_framework import serializers
from teams.models import Team


class TeamSerializer(serializers.ModelSerializer):
    captain = serializers.StringRelatedField()
    coach = serializers.StringRelatedField()
    number_of_players = serializers.SerializerMethodField()
    number_of_games_played = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields =[
            'name',
            'code',
            'captain',
            'coach',
            'number_of_players',
            'number_of_games_played'
        ]

    def get_number_of_players(self, obj):
        return obj.number_of_players

    def get_number_of_games_played(self, obj):
        return obj.number_of_games_played