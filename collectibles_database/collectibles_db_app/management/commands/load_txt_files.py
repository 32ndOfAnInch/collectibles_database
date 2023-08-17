# load json fixtures works, but load txt doenst. Some problems with absolute/relative file paths that I currently don't know. 
# Maybe I will come back later to fix this.

from django.core.management.base import BaseCommand, CommandError
from collectibles_db_app.models import GradationSystem
import os
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **options):
        fixtures_path = 'collectibles_database/collectibles_db_app/fixtures'
        
        # Load fixtures
        call_command('loaddata', 'item_gradation')
        
        # Load text files, tried many variants, but all didnt work
        gradation_systems = GradationSystem.objects.all()
        for gradation_system in gradation_systems:
            if gradation_system.description.__contains__('.txt'):
                txt_file_path = fixtures_path + "/" + gradation_system.description
                normal_path = os.path.abspath(txt_file_path).replace('\\', '\')
                full_path = normal_path.replace('collectibles_database/collectibles_database/', '')
                #txt_file_path = os.path.join(fixtures_path, gradation_system.description)
                print("txt_file_path:", normal_path)  # Debugging line
                with open(r""+full_path+"", 'r') as txt_file:
                    gradation_system.description = txt_file.read()
                    gradation_system.save()

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
        