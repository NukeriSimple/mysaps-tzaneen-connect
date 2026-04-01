# MySAPS Tzaneen Connect

A comprehensive crime reporting and case tracking system designed specifically for the Tzaneen community in Limpopo, South Africa, with full bilingual support (English and Xitsonga).

## 🌟 Features

### Core Functionality
- **Case Reporting**: Report incidents with detailed descriptions, location, and evidence
- **Voice Reporting**: Speech-to-text functionality in English and Xitsonga
- **Case Tracking**: Real-time status updates with color-coded indicators
- **Dashboard View**: All active cases visible at a glance with statistics
- **Bilingual Support**: Full interface in English and Xitsonga

### User Features
- **Simplified Registration**: Register with just a phone number
- **Notifications**: Receive updates via SMS, WhatsApp, or in-app notifications
- **Police Station Finder**: Locate nearby police stations with GPS
- **Safety Tips Library**: Crime prevention information in both languages
- **Evidence Upload**: Attach photos and documents to cases

### Accessibility
- **Large Font Mode**: Enhanced readability for elderly users
- **Voice Input**: Alternative input method for users with limited literacy
- **Landmark-Based Location**: Describe locations without GPS
- **Color-Coded Status**: Easy visual status indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Load stations: `python manage.py load_stations`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

## 🌍 Language Support

- **English**: Default interface
- **Xitsonga**: Full translation for Tsonga speakers

## 📞 Emergency Contacts

- **Police Emergency**: 10111
- **Crime Stop**: 08600 10111
- **Ambulance**: 10177
- **Tzaneen Police**: 015 306 2111

---

**Developed for the Tzaneen Community | Interactive Systems Design Assessment**