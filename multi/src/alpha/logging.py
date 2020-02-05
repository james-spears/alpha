"""Define LOGGING dictionary."""
import os
from django.utils.log import DEFAULT_LOGGING

# Use defaults as the basis for our logging setup
LOGGING = DEFAULT_LOGGING

# We need some formatters. These ones are from the docs.
LOGGING['formatters'] = {
    'verbose': {
        'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
    },
    'simple': {
        'format': '%(levelname)s %(message)s'
    },
}

# A log file handler that rotates periodically
LOGGING['handlers'].update({
    'console': {
        'level': 'INFO',
        'filters': ['require_debug_true'],
        'class': 'logging.StreamHandler',
    },
    'django.server': {
        'level': 'ERROR',
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
    },
    'mail_admins': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'django.utils.log.AdminEmailHandler'
    }
})

# The default 'django' logger is a catch-all that does nothing. We replace it with
# a rotating file handler.
LOGGING['loggers'].update({
    'django': {
        'handlers': ['console', 'mail_admins'],
        'propagate': True,
        'level': 'INFO',
    },
    'django.server': {
        'handlers': ['django.server'],
        'level': 'INFO',
        'propagate': False,
    },
})
