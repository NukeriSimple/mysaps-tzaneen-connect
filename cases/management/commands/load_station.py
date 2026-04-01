from django.core.management.base import BaseCommand
from cases.models import PoliceStation

class Command(BaseCommand):
    help = 'Load initial police stations for Tzaneen area with Xitsonga translations'
    
    def handle(self, *args, **options):
        stations = [
            {
                'name': 'Tzaneen Police Station',
                'name_ts': 'Xitlhangi xa Maphorisa eTzaneen',
                'address': '2 Danie Joubert Street, Tzaneen CBD, 0850',
                'address_ts': '2 Danie Joubert Street, Tzaneen CBD, 0850',
                'phone': '015 306 2111',
                'emergency_phone': '10111',
                'location_lat': -23.8311,
                'location_lng': 30.1639,
                'operating_hours': '24 hours',
                'operating_hours_ts': '24 tiawara',
            },
            {
                'name': 'Nkowankowa Police Station',
                'name_ts': 'Xitlhangi xa Maphorisa eNkowankowa',
                'address': 'Nkowankowa Main Road, Tzaneen, 0850',
                'address_ts': 'Nkowankowa Main Road, Tzaneen, 0850',
                'phone': '015 355 1000',
                'emergency_phone': '10111',
                'location_lat': -23.8912,
                'location_lng': 30.2905,
                'operating_hours': '24 hours',
                'operating_hours_ts': '24 tiawara',
            },
            {
                'name': 'Dan Village Satellite Police Station',
                'name_ts': 'Xitlhangi xa Maphorisa eDan Village',
                'address': 'Dan Village, Tzaneen, 0850',
                'address_ts': 'Dan Village, Tzaneen, 0850',
                'phone': '015 306 2111',
                'emergency_phone': '10111',
                'location_lat': -23.7642,
                'location_lng': 30.1489,
                'operating_hours': '08:00 - 16:00',
                'operating_hours_ts': '08:00 - 16:00',
            },
        ]
        
        for station_data in stations:
            station, created = PoliceStation.objects.get_or_create(
                name=station_data['name'],
                defaults=station_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created station: {station.name} (Xitsonga: {station.name_ts})'))
            else:
                self.stdout.write(f'Station already exists: {station.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded police stations with Xitsonga translations'))