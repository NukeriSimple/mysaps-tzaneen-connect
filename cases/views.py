from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from .models import Case, PoliceStation, IncidentCategory, Notification, CaseUpdate
from .forms import CaseReportForm

@login_required
def dashboard(request):
    """User dashboard"""
    cases = Case.objects.filter(user=request.user).order_by('-created_at')
    
    stats = {
        'total': cases.count(),
        'pending': cases.filter(status='pending').count(),
        'in_progress': cases.filter(status='in_progress').count(),
        'resolved': cases.filter(status='resolved').count(),
    }
    
    # Get unread notifications
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    
    paginator = Paginator(cases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cases': page_obj,
        'stats': stats,
        'notifications': notifications,
        'large_font': request.user.large_font,
    }
    
    return render(request, 'cases/dashboard.html', context)

@login_required
def report_case(request):
    """Report a new case"""
    if request.method == 'POST':
        form = CaseReportForm(request.POST, user=request.user)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            case.save()
            
            # Create initial case update
            CaseUpdate.objects.create(
                case=case,
                update_text=_('Case reported successfully.'),
                update_type='user_followup',
                created_by=request.user
            )
            
            # Create a notification
            Notification.objects.create(
                user=request.user,
                case=case,
                title=_('Case Reported'),
                message=f'Your case {case.case_number} has been reported successfully.',
                notification_type='info'
            )
            
            messages.success(request, _(f'Case reported successfully! Case number: {case.case_number}'))
            return redirect('cases:case_detail', case_id=case.id)
    else:
        form = CaseReportForm(user=request.user)
    
    categories = IncidentCategory.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'categories': categories,
        'large_font': request.user.large_font,
    }
    
    return render(request, 'cases/report_case.html', context)

@login_required
def voice_report(request):
    """Voice-based reporting view"""
    if request.method == 'POST':
        # Handle voice report submission
        category_id = request.POST.get('category')
        location = request.POST.get('location')
        transcribed_text = request.POST.get('transcribed_text', '')
        
        if category_id and location:
            # Create case from voice input
            case = Case.objects.create(
                user=request.user,
                category_id=category_id,
                title=_('Voice Report'),
                description=transcribed_text or _('Reported via voice input'),
                location_description=location,
                contact_name=request.user.get_full_name() or request.user.username,
                contact_phone=request.user.phone_number,
                contact_email=request.user.email
            )
            
            # Create case update
            CaseUpdate.objects.create(
                case=case,
                update_text=_('Voice report submitted.'),
                update_type='user_followup',
                created_by=request.user
            )
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                case=case,
                title=_('Voice Report Submitted'),
                message=f'Your voice report has been submitted. Case number: {case.case_number}',
                notification_type='info'
            )
            
            messages.success(request, _(f'Voice report submitted! Case number: {case.case_number}'))
            return redirect('cases:case_detail', case_id=case.id)
    
    # Get categories for the form
    categories = IncidentCategory.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'large_font': request.user.large_font,
    }
    
    return render(request, 'cases/voice_report.html', context)

@login_required
def case_detail(request, case_id):
    """View case details"""
    case = get_object_or_404(Case, id=case_id, user=request.user)
    
    # Get case updates
    updates = case.updates.all().order_by('-created_at')
    
    # Get evidence
    evidence = case.evidence.all()
    
    context = {
        'case': case,
        'updates': updates,
        'evidence': evidence,
        'large_font': request.user.large_font,
    }
    
    return render(request, 'cases/case_detail.html', context)

@login_required
def station_finder(request):
    """Find police stations"""
    stations = PoliceStation.objects.all()
    
    # Get user location from session or default to Tzaneen center
    user_lat = request.GET.get('lat')
    user_lng = request.GET.get('lng')
    
    if user_lat and user_lng:
        for station in stations:
            # Calculate rough distance (simplified)
            lat_diff = float(station.location_lat) - float(user_lat)
            lng_diff = float(station.location_lng) - float(user_lng)
            station.distance = round(((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111, 1)
        
        stations = sorted(stations, key=lambda x: getattr(x, 'distance', 999))
    
    context = {
        'stations': stations,
        'large_font': request.user.large_font,
    }
    
    return render(request, 'cases/station_finder.html', context)

@login_required
def notifications_view(request):
    """View all notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark as read
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return redirect('cases:notifications')
    
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'notifications': page_obj,
        'large_font': request.user.large_font,
    }
    
    return render(request, 'cases/notifications.html', context)

@login_required
def safety_tips(request):
    """Display safety tips"""
    safety_tips_data = [
        {
            'title': _('Home Security'),
            'title_ts': _('Xixala xa le kaya'),
            'content': _('Always lock doors and windows. Install burglar bars and security gates. Keep your property well-lit at night.'),
            'icon': 'fas fa-home',
            'tips': [
                'Install security gates on all external doors',
                'Use motion-sensor lights around your property',
                'Keep windows locked, especially at night',
                'Consider installing a home alarm system',
                'Join your local neighborhood watch'
            ]
        },
        {
            'title': _('Business Safety'),
            'title_ts': _('Xixala xa bizinisi'),
            'content': _('Install CCTV cameras. Keep minimal cash on premises. Have emergency contact numbers ready.'),
            'icon': 'fas fa-store',
            'tips': [
                'Install visible CCTV cameras',
                'Keep cash in a secure safe',
                'Train staff on emergency procedures',
                'Display emergency numbers prominently',
                'Conduct regular security audits'
            ]
        },
        {
            'title': _('Personal Safety'),
            'title_ts': _('Xixala xa wena hi wena'),
            'content': _('Avoid walking alone at night. Keep valuables hidden. Be aware of your surroundings.'),
            'icon': 'fas fa-user-shield',
            'tips': [
                'Avoid walking alone late at night',
                'Keep your phone charged and accessible',
                'Share your location with family when traveling',
                'Trust your instincts - if something feels wrong, leave',
                'Keep valuables out of sight in your car'
            ]
        },
        {
            'title': _('Emergency Preparedness'),
            'title_ts': _('Lulamisele leyi xiyimo xa xitulu'),
            'content': _('Keep emergency numbers saved. Know your nearest police station. Have a family emergency plan.'),
            'icon': 'fas fa-ambulance',
            'tips': [
                'Save emergency numbers: 10111 (Police), 10177 (Ambulance)',
                'Know the location of your nearest police station',
                'Create a family emergency communication plan',
                'Keep a first aid kit at home and in your car',
                'Practice emergency drills with your family'
            ]
        },
        {
            'title': _('Cyber Safety'),
            'title_ts': _('Xixala xa Internet'),
            'content': _('Protect your personal information online. Use strong passwords. Be careful of scams.'),
            'icon': 'fas fa-laptop',
            'tips': [
                'Use strong, unique passwords for different accounts',
                'Never share your banking PIN or OTP',
                'Be wary of phishing emails and suspicious links',
                'Keep your software and apps updated',
                'Monitor your bank statements regularly'
            ]
        }
    ]
    
    context = {
        'safety_tips': safety_tips_data,
        'large_font': request.user.large_font,
        'preferred_language': request.user.preferred_language,
    }
    
    return render(request, 'cases/safety_tips.html', context)