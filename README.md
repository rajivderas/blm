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
13) python manage.py runserver
