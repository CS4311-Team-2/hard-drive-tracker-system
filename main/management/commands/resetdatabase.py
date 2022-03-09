from subprocess import call
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

BaseCommand

MIGRATIONS = os.path.relpath(os.path.join(os.getcwd(), 'main', 'migrations'))

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        
        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")
        else:
            print("The file does not exist")

        for filename in os.listdir(MIGRATIONS):
            f = os.path.join(MIGRATIONS, filename)

            if os.path.isfile(f) and not f == os.path.join(MIGRATIONS, '__init__.py'):
                os.remove(f)

        call_command('makemigrations')
        call_command('migrate')
        print('')
        call_command('updatemodels')

        