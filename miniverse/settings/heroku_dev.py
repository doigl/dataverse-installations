from __future__ import absolute_import
import os
from os.path import join#, normpath, isdir, isfile
import dj_database_url

from .base import *

# -----------------------------------
# DEBUG OFF
# -----------------------------------
DEBUG = False

METRICS_CACHE_VIEW = True
METRICS_CACHE_VIEW_TIME = 60 * 60 * 2   # 2 HOURS
METRICS_CACHE_API_TIME = 60 * 10 # 10 minutes

# -----------------------------------
# ADMINS and MANAGERS
# -----------------------------------

# Receive 500 errors
#
ADMINS = [ ('Raman', 'raman_prasad@harvard.edu'),
    ('Raman (g.harvard)', 'prasad@g.harvard.edu')]

# Receive 404 errors
#
MANAGERS = ADMINS

# -----------------------------------
# Mail settings
# -----------------------------------
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD =  os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']
EMAIL_USE_TLS = True


# -----------------------------------
# Site ID
# -----------------------------------
SITE_ID = 1

# -----------------------------------
# Set the secret key
# -----------------------------------
SECRET_KEY = os.environ['SECRET_KEY']

# -----------------------------------
# Cookie name
# -----------------------------------
SESSION_COOKIE_NAME = 'dv_metrics_dev'

# -----------------------------------
# INTERNAL_IPS for admin access
# -----------------------------------
INTERNAL_IPS = ['140.247', # Harvard
    '65.112',            # Harvard
    '10.252',            # Internal IP
    ]

# -----------------------------------
# Extra MIDDLEWARE_CLASSES
# -----------------------------------
MIDDLEWARE_CLASSES += [
    # Restrict by IP address
    #'dv_apps.admin_restrict.middleware.RestrictAdminMiddleware',
    # Email about broken 404s
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

# -----------------------------------
# ALLOWED_HOSTS
# -----------------------------------
ALLOWED_HOSTS = ['services-dataverse.herokuapp.com',
    '52.86.18.14',  # via Heroku quotaguard add-on
    '50.17.160.202', # via Heroku quotaguard add-on
    ]

# -----------------------------------
# Extra INSTALLED_APPS
# - Update to include Heroku specifc apps
# -----------------------------------
INSTALLED_APPS += [ 'storages', # For amazon S3
    ]


# -----------------------------------
# Database settings via Heroku url
#
#  We have two databases:
#   - Heroku db for django + "installations" app
#   - external Dataverse db for reading stats
#
# -----------------------------------
DATABASE_ROUTERS = ['miniverse.db_routers.db_dataverse_router.DataverseRouter', ]


# Set the default django database url - a Heroku Database
HEROKU_DB_CONFIG = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(HEROKU_DB_CONFIG)
DATABASES['default']['TEST'] = {'MIRROR': 'default'}


# Set the Dataverse url -- this is an external readonly db
DV_DEMO_DATABASE_URL = dj_database_url.parse(os.environ['DV_DEMO_DATABASE_URL'])
DATABASES['dataverse'] = {}
DATABASES['dataverse'].update(DV_DEMO_DATABASE_URL)

# Try some db routing via qtunnel.
# .qgtunnel file has actual host of 'demo.dataverse.org:5432'
DATABASES['dataverse']['HOST'] = '127.0.0.1'
DATABASES['dataverse']['PORT'] = '5432'



# User general urls -- but restrict for prod
ROOT_URLCONF = 'miniverse.urls_heroku_prod'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
#
STATIC_ROOT = join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
#
STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# --------------------------------
# Uploaded files (S3, Bucketeer)
# --------------------------------
# File Storage via S3 and Bucketeer
#   - https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
#   - https://devcenter.heroku.com/articles/bucketeer
#
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Credentials from Heroku, generated by Bucketeer
#
AWS_ACCESS_KEY_ID = os.environ['BUCKETEER_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['BUCKETEER_AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['BUCKETEER_BUCKET_NAME']

# Update media files url, etc
#
MEDIAFILES_LOCATION = 'media'
AWS_S3_CUSTOM_DOMAIN = 'bucketeer-38679028-08e1-4038-bf0e-bb761d97f8d7.s3.amazonaws.com'
MEDIA_URL = "%s/public/" % AWS_S3_CUSTOM_DOMAIN  # Will this work w/o full AWS_S3_CUSTOM_DOMAIN?
#DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
# --------------------------------


# --------------------------------
# Used to generate the swagger spec.
#   Hack: switch to using sites framework
# --------------------------------
SWAGGER_HOST = 'services-dataverse.herokuapp.com'
SWAGGER_SCHEME = 'https'
