from rest_framework import serializers

from players.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    team = serializers.StringRelatedField()
    number_of_games = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields =[
            'full_name',
            'team',
            'jersey_number',
            'height',
            'number_of_games',
            'average_score'
        ]

    def get_number_of_games(self, obj):
        return obj.number_of_games

    def get_average_score(self, obj):
        return obj.average_score

    def get_points_scored_as_percentage(self, obj):
        return obj.points_scored_as_percentage