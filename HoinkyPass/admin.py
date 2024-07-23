from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import HoinkyUser, Quest

class HoinkyUserAdmin(UserAdmin):
    # Fieldsets for editing an existing user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
         ('Additional info', {'fields': ('level', 'quests_achieved', 'qr_unique')}),
    )

    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'level', 'quests_achieved', 'qr_unique'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_quests')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def get_quests(self, obj):
        return ", ".join([quest.name for quest in obj.quests_achieved.all()])
    get_quests.short_description = 'Quests Achieved'

admin.site.register(HoinkyUser, HoinkyUserAdmin)
admin.site.register(Quest)