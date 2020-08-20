from rest_framework import serializers

from games.models import Game, TeamStat, PlayerStat

class GameSerializer(serializers.ModelSerializer):

    game_name = serializers.SerializerMethodField()
    home_team = serializers.StringRelatedField()
    away_team = serializers.StringRelatedField()
    date = serializers.StringRelatedField()
    game_played = serializers.StringRelatedField()
    final_score = serializers.SerializerMethodField()
    game_winning_team = serializers.StringRelatedField()
    round_number = serializers.StringRelatedField()

    class Meta:
        model = Game
        fields =[
            'game_name',
            'home_team',
            'away_team',
            'date',
            'game_played',
            'round_number',
            'home_team_score',
            'away_team_score',
            'final_score',
            'game_winning_team'
        ]

    def get_game_name(self, obj):
        return obj.game_name

    def get_final_score(self, obj):
        return obj.final_score

class TeamStatSerializer(serializers.ModelSerializer):

    team = serializers.StringRelatedField()
    game = serializers.StringRelatedField()

    class Meta:
        model = TeamStat
        fields = [
            'team',
            'game',
            'points',
            'field_goals_made',
            'free_throws_made',
            'three_field_goals_made',
            'mins'
        ]

class PlayerStatSerializer(serializers.ModelSerializer):

    player = serializers.StringRelatedField()
    game = serializers.StringRelatedField()
    game_score = serializers.SerializerMethodField()

    class Meta:
        model = PlayerStat
        fields = [
            'player',
            'game',
            'is_starter',
            'points',
            'field_goals_made',
            'field_goals_attempted',
            'free_throws_made',
            'free_throws_attempted',
            'three_field_goals_made',
            'three_field_goals_attempted',
            'mins',
            'game_score'
        ]

    def get_game_score(self, obj):
        return obj.game_score