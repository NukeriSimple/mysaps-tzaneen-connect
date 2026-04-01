from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.utils import translation
from .models import Case, PoliceStation, IncidentCategory, Notification, CaseUpdate, Evidence
from .forms import CaseReportForm

def get_user_language(request):
    """Get user's preferred language"""
    if request.user.is_authenticated and request.user.preferred_language:
        return request.user.preferred_language
    return 'en'

@login_required
def dashboard(request):
    """User dashboard with bilingual support"""
    user = request.user
    language = get_user_language(request)
    
    # Set language for this request
    translation.activate(language)
    
    cases = Case.objects.filter(user=user).order_by('-created_at')
    
    stats = {
        'total': cases.count(),
        'pending': cases.filter(status='pending').count(),
        'in_progress': cases.filter(status='in_progress').count(),
        'resolved': cases.filter(status='resolved').count(),
    }
    
    # Get unread notifications
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]
    
    paginator = Paginator(cases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cases': page_obj,
        'stats': stats,
        'notifications': notifications,
        'large_font': user.large_font,
        'current_language': language,
    }
    
    return render(request, 'cases/dashboard.html', context)

@login_required
def report_case(request):
    """Report a new case with bilingual support"""
    user = request.user
    language = get_user_language(request)
    translation.activate(language)
    
    if request.method == 'POST':
        form = CaseReportForm(request.POST, user=user)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = user
            case.save()
            
            # Create initial case update
            update_text = 'Case reported successfully.'
            update_text_ts = 'Mhaka yi rhayiwile kahle.'
            
            CaseUpdate.objects.create(
                case=case,
                update_text=update_text,
                update_text_ts=update_text_ts,
                update_type='user_followup',
                created_by=user
            )
            
            # Create notification
            title_en = 'Case Reported'
            title_ts = 'Mhaka Yi Rhayiwile'
            message_en = f'Your case {case.case_number} has been reported successfully.'
            message_ts = f'Mhaka ya wena {case.case_number} yi rhayiwile kahle.'
            
            Notification.objects.create(
                user=user,
                case=case,
                title=title_en,
                title_ts=title_ts,
                message=message_en,
                message_ts=message_ts,
                notification_type='info'
            )
            
            messages.success(request, f'Case reported successfully! Case number: {case.case_number}')
            return redirect('cases:case_detail', case_id=case.id)
    else:
        form = CaseReportForm(user=user)
    
    categories = IncidentCategory.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'categories': categories,
        'large_font': user.large_font,
        'current_language': language,
    }
    
    return render(request, 'cases/report_case.html', context)

@login_required
def case_detail(request, case_id):
    """View case details with bilingual support"""
    user = request.user
    language = get_user_language(request)
    translation.activate(language)
    
    case = get_object_or_404(Case, id=case_id, user=user)
    updates = case.updates.all().order_by('-created_at')
    evidence = case.evidence.all()
    
    context = {
        'case': case,
        'updates': updates,
        'evidence': evidence,
        'large_font': user.large_font,
        'current_language': language,
    }
    
    return render(request, 'cases/case_detail.html', context)

@login_required
def voice_report(request):
    """Voice-based reporting view"""
    user = request.user
    language = get_user_language(request)
    translation.activate(language)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        location = request.POST.get('location')
        transcribed_text = request.POST.get('transcribed_text', '')
        
        if category_id and location:
            case = Case.objects.create(
                user=user,
                category_id=category_id,
                title='Voice Report',
                description=transcribed_text or 'Reported via voice input',
                location_description=location,
                contact_name=user.get_full_name() or user.username,
                contact_phone=user.phone_number,
                contact_email=user.email
            )
            
            messages.success(request, f'Voice report submitted! Case number: {case.case_number}')
            return redirect('cases:case_detail', case_id=case.id)
    
    categories = IncidentCategory.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'large_font': user.large_font,
        'current_language': language,
    }
    
    return render(request, 'cases/voice_report.html', context)

@login_required
def station_finder(request):
    """Find police stations with bilingual support"""
    user = request.user
    language = get_user_language(request)
    translation.activate(language)
    
    stations = PoliceStation.objects.all()
    
    user_lat = request.GET.get('lat')
    user_lng = request.GET.get('lng')
    
    if user_lat and user_lng:
        for station in stations:
            lat_diff = float(station.location_lat) - float(user_lat)
            lng_diff = float(station.location_lng) - float(user_lng)
            station.distance = round(((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111, 1)
        stations = sorted(stations, key=lambda x: getattr(x, 'distance', 999))
    
    context = {
        'stations': stations,
        'large_font': user.large_font,
        'current_language': language,
    }
    
    return render(request, 'cases/station_finder.html', context)

@login_required
def notifications_view(request):
    """View all notifications"""
    user = request.user
    language = get_user_language(request)
    translation.activate(language)
    
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = get_object_or_404(Notification, id=notification_id, user=user)
            notification.is_read = True
            notification.save()
            return redirect('cases:notifications')
    
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'notifications': page_obj,
        'large_font': user.large_font,
        'current_language': language,
    }
    
    return render(request, 'cases/notifications.html', context)

@login_required
def safety_tips(request):
    """Display safety tips with bilingual support"""
    user = request.user
    language = get_user_language(request)
    translation.activate(language)
    
    safety_tips_data = [
        {
            'title': {'en': 'Home Security', 'ts': 'Xixala xa le kaya'},
            'content': {
                'en': 'Always lock doors and windows. Install burglar bars and security gates. Keep your property well-lit at night.',
                'ts': 'Tsarha swinyawana ni swifasitero. Veka switsarhi na magidi ya vusekurity. Pfuxa leswi nga ekaya vusiku.'
            },
            'icon': 'fas fa-home',
            'tips': {
                'en': [
                    'Install security gates on all external doors',
                    'Use motion-sensor lights around your property',
                    'Keep windows locked, especially at night',
                    'Consider installing a home alarm system',
                    'Join your local neighborhood watch'
                ],
                'ts': [
                    'Veka magidi ya vusekurity etinyaweni hinkwato',
                    'Tirhisa switshuri leswi tshurikaka loko ku ri na nyimpfu',
                    'Tsarha swifasitero, ngopfu-ngopfu vusiku',
                    'Cinca ku veka alarm ya le kaya',
                    'Tlangana ni vaaki va wena ku langutela vusekurity'
                ]
            }
        },
        {
            'title': {'en': 'Business Safety', 'ts': 'Xixala xa bizinisi'},
            'content': {
                'en': 'Install CCTV cameras. Keep minimal cash on premises. Have emergency contact numbers ready.',
                'ts': 'Veka tikhamera ta CCTV. U nga tshami ni mali yo tala eka bizinisi. Va na tinomoro ta xitulu.'
            },
            'icon': 'fas fa-store',
            'tips': {
                'en': [
                    'Install visible CCTV cameras',
                    'Keep cash in a secure safe',
                    'Train staff on emergency procedures',
                    'Display emergency numbers prominently',
                    'Conduct regular security audits'
                ],
                'ts': [
                    'Veka tikhamera ta CCTV leswi vonakaka',
                    'Tshika mali eka safe yo tiyiseka',
                    'Dyondzisa vatirhi hi ndlela yo tirha eka xitulu',
                    'Beka tinomoro ta xitulu laha swi vonakaka',
                    'Endza vukamberi bya vusekurity nkarhi na nkarhi'
                ]
            }
        },
        {
            'title': {'en': 'Personal Safety', 'ts': 'Xixala xa wena hi wena'},
            'content': {
                'en': 'Avoid walking alone at night. Keep valuables hidden. Be aware of your surroundings.',
                'ts': 'Tshika ku famba u ri ntsena vusiku. Pfumala swilo swa nkoka. Tivisisa leswi nga ku n_helo.'
            },
            'icon': 'fas fa-user-shield',
            'tips': {
                'en': [
                    'Avoid walking alone late at night',
                    'Keep your phone charged and accessible',
                    'Share your location with family when traveling',
                    'Trust your instincts - if something feels wrong, leave',
                    'Keep valuables out of sight in your car'
                ],
                'ts': [
                    'Tshika ku famba u ri ntsena vusiku',
                    'Tiyisa leswaku xihambana xa wena xi na mbuyelo',
                    'Byela vandla lwa wena laha u nga kona loko u ri endleleni',
                    'Tshemba mbilu ya wena - loko u twa swi nga ri kahle, famba',
                    'U nga tshami swilo swa nkoka swi vonaka eka movha wa wena'
                ]
            }
        }
    ]
    
    # Get tips in user's language
    for tip in safety_tips_data:
        tip['title_display'] = tip['title'].get(language, tip['title']['en'])
        tip['content_display'] = tip['content'].get(language, tip['content']['en'])
        tip['tips_display'] = tip['tips'].get(language, tip['tips']['en'])
    
    context = {
        'safety_tips': safety_tips_data,
        'large_font': user.large_font,
        'current_language': language,
    }
    
    return render(request, 'cases/safety_tips.html', context)