from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jj4*7%31-8t-m3hib6*a#_m_4^y%odc)bknovi-sf-18$b^u0@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notes.apps.NotesConfig',
    'ckeditor',
    'ckeditor_uploader',
]


# CK-EDITOR configurations
CKEDITOR_CONFIGS = {

    'simple':{
      'skin': 'moono-lisa',
      'toolbar': 'Custom',
      'toolbar_Custom': [
          ['Bold'],
          ['NumberedList', 'BulletedList'],
      ],

      'width': 690
    
    },

    'moderate':{
      'skin': 'moono-lisa',
      'toolbar': 'Custom',
      'toolbar_Custom': [
          ['Bold', 'Italic'],
          ['Table', 'HorizontalRule'],
          ['TextColor', 'BGColor'],
          ['NumberedList', 'BulletedList'],
          ['Indent', 'Outdent'],
          ['Maximize'],
      ],
      'width': 690,
      'height': 490
    },


    'default': {
        'skin': 'moono-lisa',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
            ['JustifyLeft', 'HorizontalRule' ,'JustifyCenter','JustifyRight','JustifyBlock'],
            ['NumberedList','BulletedList'],
            ['Indent','Outdent'],
            ['Maximize'],
        ],
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                'codesnippet',
                'uploadimage',
                'uploadwidget',
                'autoembed',
                'clipboard',
                'uicolor',
                'stylesheetparser',
                'tabletools',
                'templates',
                'exportpdf'
            ]
        ),
        'codeSnippet_theme': 'monokai_sublime',
        'height': 390,
        'width': 690,
    },

    'my_ckeditor': {
        'toolbar': 'Basic',
    }
}

CKEDITOR_RESTRICT_BY_USER = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'notebook.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notes.context_processors.get_all_notes_type',
                'notes.context_processors.get_url_name',
            ],
        },
    },
]

AUTH_USER_MODEL = 'accounts.UserAccount'

WSGI_APPLICATION = 'notebook.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_builtin')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'

CKEDITOR_UPLOAD_PATH = 'uploads/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
