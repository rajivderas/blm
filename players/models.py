from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.conf import settings
from django.utils.functional import cached_property
from collections import OrderedDict

from games.models import PlayerStat


class Role(models.Model):
    ADMIN = 'A'
    PLAYER = 'P'
    COACH = 'C'

    ROLE_TYPES = [(ADMIN, 'Admin'),(PLAYER, 'Player'),(COACH, 'Coach')]

    type = models.CharField(
        max_length=2,
        choices=ROLE_TYPES,
        default=PLAYER,
        verbose_name='Role Type'
    )

    class Meta:
        ordering = ['type']

    def __str__(self):
        return str(self.type)

    def get_id(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('players:role_page', args=[str(self.id)])


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        try:
            return '{first_name} {last_name} ({type})'.format(first_name=self.user.first_name,
                                                          last_name=self.user.last_name,
                                                          type=self.role.type)
        except Role.DoesNotExist:
            return self.user.first_name

    def get_absolute_url(self):
        return reverse('players:user_role_page', args=[str(self.id)])


class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_player',
                             on_delete=models.CASCADE)
    team = models.ForeignKey('teams.Team', related_name='player',
                             verbose_name='Team', on_delete=models.CASCADE)
    jersey_number = models.PositiveSmallIntegerField(
        verbose_name='Jersey Number',
        blank=False,
        null=False,
        default=0
    )
    height = models.DecimalField(max_digits=10000,
                                 decimal_places=2,
                                 blank=True,
                                 null=False,
                                 default='0',
                                 verbose_name='Height (cm)')

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        unique_together = ('team', 'jersey_number')

    def get_absolute_url(self):
        return reverse('players:player_page',
                       args=[str(self.user.first_name) + '_' + str(self.user.last_name)])

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.user.first_name,
                                                 last_name=self.user.last_name)

    @cached_property
    def full_name(self):
        return '{first_name} {last_name}'.format(first_name=self.user.first_name,
                                                 last_name=self.user.last_name)

    @cached_property
    def number_of_games(self):
        return PlayerStat.objects.filter(player=self).filter(mins__gt=0).count()

    @cached_property
    def average_score(self):
        return PlayerStat.objects.filter(player=self).aggregate(Avg('points'))

    @cached_property
    def points_scored_as_percentage(self):
        player_stat = PlayerStat.objects.filter(mins__gt=0).get(id=self.user.id)
        points_percentage_dict = {}

        try:
            points_percentage_dict['field_goals_perc'] = float('{0:.3f}'.format(player_stat.field_goals_made / player_stat.field_goals_attempted))
            points_percentage_dict['three_field_goals_perc'] = float('{0:.3f}'.format(player_stat.three_field_goals_made / player_stat.three_field_goals_attempted))
            points_percentage_dict['free_throws_perc'] = float('{0:.3f}'.format(player_stat.free_throws_made / player_stat.free_throws_attempted))

        except ZeroDivisionError:
            raise ValueError("Division by Zero !")

        return points_percentage_dict


    def game_stats(self):
        return PlayerStat.objects.filter(mins__gt=0).filter(id=self.user.id).first()

