''' Django notifications signal file '''
# -*- coding: utf-8 -*-
from django.dispatch import Signal

notify = Signal(providing_args=[  # pylint: disable=invalid-name
    'actor','recipient','nfrom',  'type','status','href','msg','verb', 'action_object', 'target', 'description',
    'timestamp', 'level'
])
