from xadmin.plugins.auth import PermissionModelMultipleChoiceField
from notifications.models import Notification
from common.basemodel import Baseadminmodel
from users.resources import Userresource
from .models import *
import  xadmin
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from django.utils.translation import ugettext as _
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper

class Conpanymodel(Baseadminmodel):
    list_display = ['name']
    search_fields = ['name']
    hidden_menu = True
    only_admin_show = True
xadmin.site.register(Company,Conpanymodel)


