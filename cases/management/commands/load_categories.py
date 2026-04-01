from django.core.management.base import BaseCommand
from cases.models import IncidentCategory

class Command(BaseCommand):
    help = 'Load initial incident categories with Xitsonga translations'
    
    def handle(self, *args, **options):
        categories = [
            {
                'name': 'theft',
                'name_ts': 'Vutsotsi',
                'icon': 'fas fa-money-bill-wave',
                'is_active': True
            },
            {
                'name': 'burglary',
                'name_ts': 'Ku ngheneriwa endlwini',
                'icon': 'fas fa-home',
                'is_active': True
            },
            {
                'name': 'assault',
                'name_ts': 'Ku vuriwa',
                'icon': 'fas fa-fist-raised',
                'is_active': True
            },
            {
                'name': 'robbery',
                'name_ts': 'Ku khomeriwa',
                'icon': 'fas fa-mask',
                'is_active': True
            },
            {
                'name': 'property_damage',
                'name_ts': 'Ku onhakala ka xifaniso',
                'icon': 'fas fa-hammer',
                'is_active': True
            },
            {
                'name': 'domestic_violence',
                'name_ts': 'Nghungu ya le kaya',
                'icon': 'fas fa-heart-broken',
                'is_active': True
            },
            {
                'name': 'service_delivery',
                'name_ts': 'Vukorhokeri',
                'icon': 'fas fa-handshake',
                'is_active': True
            },
            {
                'name': 'other',
                'name_ts': 'Swin\'wana',
                'icon': 'fas fa-question-circle',
                'is_active': True
            },
        ]
        
        for cat_data in categories:
            category, created = IncidentCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'name_ts': cat_data['name_ts'],
                    'icon': cat_data['icon'],
                    'is_active': cat_data['is_active']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.get_name_display()} (Xitsonga: {category.name_ts})'))
            else:
                # Update existing category
                category.name_ts = cat_data['name_ts']
                category.icon = cat_data['icon']
                category.save()
                self.stdout.write(f'Updated category: {category.get_name_display()}')
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded incident categories with Xitsonga translations'))
        