from subprocess import call
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

BaseCommand

MAIN_MIGRATIONS = os.path.relpath(os.path.join(os.getcwd(), 'main', 'migrations'))
USER_MIGRATIONS = os.path.relpath(os.path.join(os.getcwd(), 'users', 'migrations'))

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        
        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")
        else:
            print("The file does not exist")

        for filename in os.listdir(MAIN_MIGRATIONS):
            f = os.path.join(MAIN_MIGRATIONS, filename)

            if os.path.isfile(f) and not f == os.path.join(MAIN_MIGRATIONS, '__init__.py'):
                os.remove(f)

        for filename in os.listdir(USER_MIGRATIONS):
            f = os.path.join(USER_MIGRATIONS, filename)

            if os.path.isfile(f) and not f == os.path.join(USER_MIGRATIONS, '__init__.py'):
                os.remove(f)

        call_command('makemigrations')
        call_command('migrate')
        print('')
        call_command('updatemodels')

        