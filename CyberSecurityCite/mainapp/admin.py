from django.contrib import admin
from .models import User, TeamMember, Event, Registration, Achievement, ContactForm

admin.site.register(User)
admin.site.register(TeamMember)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Achievement)
admin.site.register(ContactForm)