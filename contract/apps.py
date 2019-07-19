from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class ContractConfig(AppConfig):
    name = 'contract'
    verbose_name = '业务订单管理'

    def ready(self):
        autodiscover_modules('signals.py')

