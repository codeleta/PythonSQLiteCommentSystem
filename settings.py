LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s][%(processName)s][%(threadName)s][%(filename)s:%(lineno)s]'
                      ' %(name)s: %(message)s '
        }
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },

    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

HOST = 'localhost'
PORT = 8000