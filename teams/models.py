from django.db import models
from django.db.models import Avg, Sum
from django.utils.functional import cached_property
from django.urls import reverse
from django.conf import settings
import math

from players.models import Player, PlayerStat
from games.models import Game


class Coach(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_coach', on_delete=models.CASCADE)

    @cached_property
    def full_name(self):
        return '{first_name} {last_name}'.format(first_name=self.user.first_name,
                                                 last_name=self.user.last_name)

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.user.first_name,
                                                              last_name=self.user.last_name)


class Team(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=64,
        blank=False,
        null=False
    )
    code = models.CharField(
        verbose_name='Code',
        max_length=5,
        blank=True,
        null=True
    )
    captain = models.ForeignKey(
        'players.Player',
        related_name='team_captain',
        verbose_name='Captain',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    coach = models.OneToOneField(
        'teams.Coach',
        related_name='team_coach',
        verbose_name='Coach',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['name']

    @cached_property
    def number_of_games_played(self):
        return Game.objects.team(self).happened().count()

    @cached_property
    def number_of_players(self):
        return Player.objects.filter(team=self).count()


    def list_players(self):
        return Player.objects.filter(team=self)


    def best_players(self, percentile):
        print(percentile)
        ordered_player_points = PlayerStat.objects.team(self).filter(is_starter=True).exclude(mins=0
                                                                    ).values(
                                                                        'player_id'
                                                                    ).annotate(
                                                                        player_points_sum=Sum('points')
                                                                    ).order_by(
                                                                        'player_points_sum'
                                                                    )

        nth_percentile = int(math.ceil((len(ordered_player_points) * percentile) / 100)-1)
        print(nth_percentile)
        print(ordered_player_points)
        best_players = []
        for index, item in enumerate(ordered_player_points):
            index += 1
            if index > nth_percentile:
                player = Player.objects.get(id=item['player_id'])
                best_players.append(player)

                print(best_players)

        return best_players;


    def win_loss_record(self, place):
        games = Game.objects.happened()

        if place == 'all':
            wins = games.team(self).filter(game_winning_team=self).count()
            loses = games.team(self).exclude(game_winning_team=self).count()
        elif place == 'home':
            wins = games.filter(home_team=self).filter(game_winning_team=self).count()
            loses = games.filter(home_team=self).exclude(game_winning_team=self).count()
        elif place == 'away':
            wins = games.filter(away_team=self).filter(game_winning_team=self).count()
            loses = games.filter(away_team=self).exclude(game_winning_team=self).count()
        else:
            raise Exception("Place specify game location 'home', 'away' or 'all' ")

        try:
            points_for = games.team(self).aggregate(Sum('home_team_score'))['home_team_score__sum']
            points_against = games.team(self).aggregate(Sum('away_team_score'))['away_team_score__sum']
            exponent = 13.91
            percentage = float('{0:.3f}'.format(points_for ** exponent / (points_for ** exponent +
                                                                          points_against ** exponent)))
        except ZeroDivisionError:
            return 0.0

        return {'team':self.__str__(), 'wins': wins, 'loses': loses, 'percentage': percentage}


    def get_absolute_url(self):
        return reverse('teams:team_page', args=[str(self.name.replace(' ', '_'))])


    def __str__(self):
        return '{name} ({code})'.format(name=self.name, code=self.code)