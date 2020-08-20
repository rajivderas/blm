from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404

import math
from faker import Faker

from games.models import Game, TeamStat, PlayerStat
from players.models import Role, UserRole, Player
from teams.models import Team, Coach


class Command(BaseCommand):


    def roles(self, fake):
        ADMIN = 'A'
        PLAYER = 'P'
        COACH = 'C'

        ROLE_TYPES = [ADMIN, PLAYER, COACH]
        for item in range(len(ROLE_TYPES)):
            try:
                role = Role(type=ROLE_TYPES[item])
            except ObjectDoesNotExist:
                raise CommandError('Role Model Does not exists')
            role.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted data for Role "%s"' % role.type))


    def users(self, fake):
        for i in range(177):
            username = fake.user_name()
            password = 'matific'
            try:
                user = User.objects.create_user(username=username, password=password, email=fake.safe_email(),
                                                first_name=fake.first_name(), last_name=fake.last_name())
            except ObjectDoesNotExist:
                raise CommandError('User Model Does not exits')
            user.save()
            self.stdout.write(self.style.SUCCESS('User Created : "%s"' % user.username))


    def user_roles(self, fake):
        users = User.objects.filter(is_superuser=False)

        admin = get_object_or_404(Role, type='A')
        coach = get_object_or_404(Role, type='C')
        player = get_object_or_404(Role, type='P')

        for user in users[:160]:
            try:
                p = UserRole(user_id=user.id, role_id=player.id, is_logged_in=True)
            except ObjectDoesNotExist:
                raise CommandError('Issue in adding user role mapping')
            p.save()
            self.stdout.write(self.style.SUCCESS('User Role Mapped : { %s : %s }' % (user.username, player.type)))

        for user in users[160:176]:
            print(user)
            try:
                u = UserRole(user_id=user.id, role_id=coach.id, is_logged_in=True)
            except coach.DoesNotExists:
                raise CommandError('Issue in adding user role mapping')
            u.save()
            self.stdout.write(self.style.SUCCESS('User Role Mapped : { %s : %s }' % (user.username, coach.type)))

        for user in users[176:]:
            try:
                u = UserRole(user_id=user.id, role_id=admin.id, is_logged_in=True)
            except ObjectDoesNotExist:
                raise CommandError('Issue in adding user role mapping')
            u.save()
            self.stdout.write(self.style.SUCCESS('Super Admin Mapped : { %s : %s }' % (user.username, admin.type)))


    def coaches(self, fake):
        role = get_object_or_404(Role, type='C')
        user_role = UserRole.objects.filter(role_id=role.id)

        for i in range(len(user_role)):
            try:
                coach = Coach(user_id=user_role[i].user.id)
            except ObjectDoesNotExist:
                raise CommandError('Issue with adding user as Coach')
            coach.save()
            self.stdout.write(self.style.SUCCESS('Coach Created  : %s ' % user_role[i].user.id))


    def teams(self, fake):
       role = get_object_or_404(Role, type='C')
       user_role = UserRole.objects.filter(role_id=role.id)

       counter = 0
       for item in range(16):
            try:
                coach = get_object_or_404(Coach,user=user_role[counter].user.id)
                print(coach)
                team = Team(name=fake.slug(), code=fake.lexify(text='????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                            coach=coach)
            except ObjectDoesNotExist:
                raise CommandError('Team Model Does not exists')
            team.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully inserted Team : "%s" , Code : "%s"' % (team.name, team.code)))
            counter += 1


    def players(self, fake):
        teams = Team.objects.all()
        player = Role.objects.filter(type='P').first()
        users = UserRole.objects.filter(role_id=player.id)

        total = 0
        for team in teams:
            counter = 0
            while counter < 10:
                try:
                    player = Player(user_id=users[total].user.id,team_id=team.id,
                                    jersey_number=counter+1,
                                    height=fake.random_int(min=100, max=255, step=1))
                except ObjectDoesNotExist:
                    raise Warning('Issue with adding user as Player')
                player.save()
                self.stdout.write(self.style.SUCCESS('Player Created  : %s %s' %
                                                     (users[total].user.first_name,
                                                      users[total].user.username)))
                total += 1
                counter += 1


    def qf_game(self, fake):
        teams = Team.objects.all()
        self.create_game(fake, teams, 'QF')


    def sf_game(self, fake):
        teams = Game.objects.filter(round_number='QF')
        self.create_game(fake, teams, 'SF')


    def fi_game(self, fake):
        teams = Game.objects.filter(round_number='SF')
        self.create_game(fake, teams, 'FI')


    def winner(self, fake):
        teams = Game.objects.filter(round_number='FI')
        self.create_game(fake, teams, 'WI')


    def create_game(self, fake, teams, round_number):
        home_teams = teams[1::2]
        away_teams = teams[0::2]
        for i in range(len(home_teams)):
            home_score = fake.random_int(min=0, max=186, step=1)
            away_score = fake.random_int(min=0, max=186, step=1)

            winning_team = home_teams[i] if home_score > away_score else away_teams[i]

            home = home_teams[i] if round_number == 'QF' else home_teams[i].game_winning_team
            away = away_teams[i] if round_number == 'QF' else away_teams[i].game_winning_team
            winner = winning_team if round_number == 'QF' else winning_team.game_winning_team

            try:
                game = Game(home_team=home, away_team=away, game_played=True,
                            game_winning_team=winner, round_number=round_number,
                            home_team_score=home_score, away_team_score=away_score,
                            date=fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None))
            except ObjectDoesNotExist:
                raise CommandError('games populated')
            game.save()
            self.stdout.write(self.style.SUCCESS('%s Game %s Vs %s =>  winner : %s '
                                                 % (round_number, home.id, away.id, winner.id)))


    def team_stats(self, fake):
        teams = Team.objects.all()

        for team in teams:
            games = Game.objects.filter(Q(home_team=team.id) | Q(away_team=team.id)).filter(game_played=True)

            for game in games:
                team_id = game.home_team_id if game.home_team_id == team.id else game.away_team_id
                game_score = game.home_team_score if game.home_team_id == team.id else game.away_team_score
                mins = fake.random_int(min=1, max=48, step=1)
                equal_points = int(math.ceil(game_score / 3))

                team_stat = TeamStat(team_id=team_id, game_id=game.id,
                                          field_goals_made=equal_points,
                                          three_field_goals_made=equal_points,
                                          free_throws_made=equal_points,
                                          mins=mins
                                          )

                team_stat.save()
                self.stdout.write(self.style.SUCCESS('Stat saved for Game # %s ' % game.id))


    def player_stats(self, fake):
        team_stats = TeamStat.objects.all()

        for team_stat in team_stats:
            players = Player.objects.filter(team_id=team_stat.team_id).order_by('jersey_number')
            equal_points = int(math.ceil((team_stat.points / len(players)) / 3))

            for i in range(len(players)):
                field_goals_made = equal_points
                field_goals_attempted = fake.random_int(min=0, max=30, step=1)
                three_field_goals_made = equal_points
                three_field_goals_attempted = fake.random_int(min=0, max=30, step=1)
                free_throws_made = equal_points
                free_throws_attempted = fake.random_int(min=0, max=30, step=1)
                mins = fake.random_int(min=1, max=48, step=1)

                player_stat = PlayerStat(player_id=players[i].id, game_id=team_stat.game_id,
                                         is_starter=True,field_goals_made=field_goals_made,
                                         field_goals_attempted=field_goals_attempted,
                                         three_field_goals_made=three_field_goals_made,
                                         three_field_goals_attempted=three_field_goals_attempted,
                                         free_throws_made=free_throws_made,
                                         free_throws_attempted=free_throws_attempted,
                                         mins=mins)
                player_stat.save()
                self.stdout.write(
                    self.style.SUCCESS('Stat saved for Player # %s ' % (players[i].id)))


    def handle(self, *args, **options):
        fake = Faker()

        self.roles(fake)
        self.users(fake)
        self.user_roles(fake)

        self.coaches(fake)
        self.teams(fake)
        self.players(fake)

        self.qf_game(fake)
        self.sf_game(fake)
        self.fi_game(fake)
        self.winner(fake)

        self.team_stats(fake)
        self.player_stats(fake)