from django.contrib import admin
from .models import Participant, Reservation

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1
    readonly_fields = ("reservation_date",)  
    autocomplete_fields = ('conference',) 
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "cin",
        "participant_category",  
        "created_at",
        "updated_at",
    )
    
    search_fields = ("username", "first_name", "last_name", "email", "cin")
    list_per_page = 10
    ordering = ("created_at",)
    readonly_fields = ("created_at", "updated_at")  

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'cin', 'participant_category') 
        }),
        ('Données de suivi', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [ReservationInline]  

    list_filter = (
        'participant_category',  
        'created_at',
    )
    list_editable = ('first_name', 'last_name')


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Reservation)
