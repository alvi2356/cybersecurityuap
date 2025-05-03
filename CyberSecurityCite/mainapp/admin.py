from django.contrib import admin
from .models import User, TeamMember, Event, Registration, Achievement, ContactForm, FormerPresident, EventRegistration

admin.site.register(User)
admin.site.register(TeamMember)
admin.site.register(FormerPresident)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Achievement)
admin.site.register(ContactForm)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'email', 'phone', 'event', 'registered_at')
    list_filter = ('event', 'has_experience', 'department', 'registered_at')
    search_fields = ('full_name', 'student_id', 'email', 'phone')
    readonly_fields = ('registered_at',)
    fieldsets = (
        ('Event Information', {
            'fields': ('event',)
        }),
        ('Student Information', {
            'fields': ('full_name', 'student_id', 'email', 'phone', 'department', 'semester')
        }),
        ('Additional Information', {
            'fields': ('has_experience', 'expectations', 'registered_at')
        }),
    )