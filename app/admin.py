from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(User)
admin.site.register(Feedback)
admin.site.register(Project)
admin.site.register(LikeProject)
admin.site.register(Community)
admin.site.register(Comment)
