from django.test import TestCase

# Create your tests here.
from tk_docker import settings
print(settings.STATICFILES_DIRS[0]+'')