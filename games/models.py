from django.db import models
from collections import OrderedDict
from django.urls import reverse
from django.db.models import Q, Sum
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError


class GameQuerySet(models.QuerySet):
    def team(self, team):
        return self.filter(Q(home_team=team) | Q(away_team=team))

    def happened(self):
        return self.filter(game_played=True)


class Game(models.Model):
    QF = 'QF'
    SF = 'SF'
    FI = 'FI'
    WI = 'WI'

    ROUNDS = [
        (QF, 'Quarter Final'),
        (SF, 'Semi Final'),
        (FI, 'Final'),
        (WI, 'Winner')
    ]

    home_team = models.ForeignKey(
        'teams.Team', related_name='home_team',
        verbose_name='Home Team',
        on_delete=models.CASCADE
    )

    away_team = models.ForeignKey(
        'teams.Team', related_name='away_team',
        verbose_name='Away Team',
        on_delete=models.CASCADE
    )

    date = models.DateField(
        verbose_name='Date'
    )

    game_played = models.BooleanField(
        verbose_name='Did the game played?',
        default=False
    )

    round_number = models.CharField(
        max_length=2,
        choices=ROUNDS,
        default=QF,
        verbose_name='Round Type'
    )

    home_team_score = models.PositiveIntegerField(
        null=False, blank=False,
        default=0,
        verbose_name='Home Team Score'
    )

    away_team_score = models.PositiveIntegerField(
        null=False, blank=False,
        default=0,
        verbose_name='Away Team Score'
    )

    game_winning_team = models.ForeignKey(
        'teams.Team', related_name='game_winning_team',
        verbose_name='Game Winner',
        null=True, blank=True,
        on_delete=models.CASCADE
    )

    objects = GameQuerySet.as_manager()

    class Meta:
        ordering = ['date']
        unique_together = ('away_team', 'home_team', 'date')

    @cached_property
    def final_score(self):
        if self.game_played:
            final_score = {'home_team': self.home_team_score,
                           'away_team': self.away_team_score}
            return final_score
        else:
            return None

    @cached_property
    def game_name(self):
        return '{away_team} at {home_team} ({date})'.format(away_team=self.away_team.code,
                                                            home_team=self.home_team.code,
                                                            date=self.date.strftime("%d.%m.%Y"))

    def get_absolute_url(self):
        return reverse('game:game_page', args=[self.date.strftime("%Y-%m-%d"),
                                               self.away_team.code,
                                               self.home_team.code])

    def __str__(self):
        return '{away_team} at {home_team} ({date})'.format(away_team=self.away_team.name,
                                                            home_team=self.home_team.name,
                                                            date=self.date.strftime("%d.%m.%Y"))

    def clean(self):
        if self.away_team == self.home_team:
            raise ValidationError("Team should have an opposition Team.")

        if TeamStat.objects.filter(game=self).count() not in [0, 2]:
            raise ValidationError("Game has to be played by 2 teams.")


class PlayerStatQuerySet(models.QuerySet):
    def game(self, game):
        return self.filter(game=game)

    def team(self, team):
        return self.filter(player__team=team)


class PlayerStat(models.Model):
    player = models.ForeignKey(
        'players.Player', related_name='player',
        verbose_name='Player',
        on_delete=models.CASCADE
    )

    game = models.ForeignKey(
        'games.Game', related_name='game',
        verbose_name='Game',
        on_delete=models.CASCADE
    )

    is_starter = models.BooleanField(
        verbose_name='Is starter?',
        default=False,
    )

    # https://en.wikipedia.org/wiki/Basketball_statistics
    points = models.PositiveIntegerField(verbose_name='PTS', default=0)
    field_goals_made = models.PositiveIntegerField(verbose_name='FGM', default=0)
    field_goals_attempted = models.PositiveIntegerField(verbose_name='FGA', default=0)
    free_throws_made = models.PositiveIntegerField(verbose_name='FTM', default=0)
    free_throws_attempted = models.PositiveIntegerField(verbose_name='FTA', default=0)
    three_field_goals_made = models.PositiveIntegerField(verbose_name='3FGM', default=0)
    three_field_goals_attempted = models.PositiveIntegerField(verbose_name='3FGA', default=0)
    mins = models.PositiveIntegerField(verbose_name='MIN', default=0)

    objects = PlayerStatQuerySet.as_manager()

    class Meta:
        unique_together = ('player', 'game',)

    @cached_property
    def game_score(self):
        game_score = self.points + (0.4 * self.field_goals_made) - (0.7 * self.field_goals_attempted) - (0.4 * (self.free_throws_attempted - self.free_throws_made))
        return game_score

    def __str__(self):
        return '{player} ({game})'.format(player=self.player.full_name, game=self.game.game_name)

    def save(self, *args, **kwargs):
        self.points = self.free_throws_made + (self.field_goals_made - self.three_field_goals_made) * 2 + self.three_field_goals_made * 3
        super(PlayerStat, self).save(*args, **kwargs)


class TeamStat(models.Model):
    team = models.ForeignKey(
        'teams.Team', related_name='team_stat',
        verbose_name='Team',
        on_delete=models.CASCADE
    )

    game = models.ForeignKey(
        'games.Game', related_name='game_stat',
        verbose_name='Game',
        on_delete=models.CASCADE
    )

    points = models.PositiveIntegerField(verbose_name='Points', default=0)
    field_goals_made = models.PositiveIntegerField(verbose_name='FGM', default=0)
    free_throws_made = models.PositiveIntegerField(verbose_name='FTM', default=0)
    three_field_goals_made = models.PositiveIntegerField(verbose_name='3FGM', default=0)
    mins = models.PositiveIntegerField(verbose_name='MIN', default=0)

    class Meta:
        unique_together = ('team', 'game')


    def top_game_points_scorer(self):
        team_player_stats = PlayerStat.objects.game(self.game).team(self.team)
        player_stats = team_player_stats.order_by('-points')[0]

        value = getattr(player_stats, 'points')
        n = team_player_stats.filter(**{'points': value}).count()

        if n > 1:
            return str(n) + ' players', str(value) + " points "
        elif n == 1:
            return player_stats.player.full_name, str(value) + " points "


    def team_stats(self):
        return TeamStat.objects.get(game=self.game, team=self.team, mins__gt=0)


    def __str__(self):
        return '{team} ({away_team} at {home_team}, {date})'.format(team=self.team.name,
                                                                    away_team=self.game.away_team.code,
                                                                    home_team=self.game.home_team.code,
                                                                    date=self.game.date.strftime("%d.%m.%Y"))


    def save(self, *args, **kwargs):
        super(TeamStat, self).save(*args, **kwargs)

        stat = TeamStat.objects.filter(game=self.game).filter(team=self.team).aggregate(
            field_goals_made=Sum('field_goals_made'), three_field_goals_made=Sum('three_field_goals_made'),
            free_throws_made=Sum('free_throws_made')
        )

        self.field_goals_made = stat['field_goals_made']
        self.three_field_goals_made = stat['three_field_goals_made']
        self.free_throws_made = stat['free_throws_made']
        self.mins = self.mins
        self.points = self.free_throws_made + (self.field_goals_made - self.three_field_goals_made) * 2 + self.three_field_goals_made * 3

        if TeamStat.objects.filter(game=self.game) == 2:
            self.game.happened = True

            if (TeamStat.objects.get(game=self.game, team=self.game.home_team).points >
                    TeamStat.objects.get(game=self.game, team=self.game.away_team).points):
                self.game.winner = self.game.home_team
            else:
                self.game.winner = self.game.away_team

            self.game.save()

        super(TeamStat, self).save(*args, **kwargs)


    def team_players_stats(self):
        return PlayerStat.objects.game(self.game).team(self.team).order_by('-is_starter', '-mins')