import sys
import os
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StreamingPlatform.settings')

# Load Django settings
django.setup()
