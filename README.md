# Instalation

1) <DEV_FOLDER_PATH>/mkdir matific
2) <DEV_FOLDER_PATH>/cd matific
3) <DEV_FOLDER_PATH>/matific virtualenv -p python3
4) <DEV_FOLDER_PATH>/matific/mkdir src
5) <DEV_FOLDER_PATH>/cd src
6)  $<DEV_FOLDER_PATH>/matific/src/ to git clone https://github.com/rajivderas/blm.git
7)  $<DEV_FOLDER_PATH>/matific/src/blm/.\Scripts\activate
8) pip install -r requirements.txt
9) Update your settings.py in blm foldr to reflect the following:

# add the following entries to the .../blm/settings.py
...
INSTALLED_APPS = [
    ...
    'rest_framework',
    'players',
    'teams',
    'games',
]

...
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}

10) python manage.py makemigrations
11) python manage.py migrate
12) python manage.py init_blm_data
13) python manage.py createsuperuser(add the username and password you desire but please keep that in mind)
14) python manage.py runserver
15) goto any browser and type http://localhost:8000/admin then login using user account created in step 13.
16) now run any rest api service(exposed in the next section) in the browser by providing valid values to the request params.

# run any of the following rest services by poviding valid request params
note -by using admin login to the system you can view the sample data generated from init_blm_data.py command file and get valid values from their required to run following services.

Players:
http://localhost:8000/blm/api/players/player-stats/<int:player_id>
http://localhost:8000/blm/api/players/player-details/<int:player_id>

Teams:
http://localhost:8000/blm/api/teams/team-players/<int:team_id>
http://localhost:8000/blm/api/teams/team-details/<int:team_id>
http://localhost:8000/blm/api/teams/team-record/<int:team_id>/<str:place>
http://localhost:8000/blm/api/teams/best-team-players/<int:team_id>/<int:percentile>

Games:
http://localhost:8000/blm/api/games/team-stats/<int:game_id>
http://localhost:8000/blm/api/games/all-games
http://localhost:8000/blm/api/games/team-player-stats/<int:game_id>
http://localhost:8000/blm/api/games/top-game-points-scorer/<int:game_id>

