from django.contrib import admin
from .models import Conference
from users .models import *
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
# Register your models here.
class ReservationInLine(admin.TabularInline):   #StackedInline
    model=Reservation
    extra=1
    readonly_fields=('reservation_date',)
    
class ParticipantFilter(admin.SimpleListFilter):
    title="participant filter"
    parameter_name="participant"
    def lookups(self,request,model_admin):
        return(
            ('0',('no participant')),
            ('more',('more participants'))
            
        )
    def queryset(self,request,queryset):
        if self.value()=='0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        if self.value()=='more':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        return queryset
    


class ConferenceDateFilter(admin.SimpleListFilter):
    title = ('conference date')
    parameter_name = 'conference_date'

    def lookups(self, request, model_admin):
        return (
            ('past', ('Past Conferences')),
            ('today', ('Today Conferences')),
            ('upcoming', ('Upcoming Conferences')),
        )

    def queryset(self, request, queryset):
        today = now().date() 

        if self.value() == 'past':
            return queryset.filter(end_date__lt=today)

        if self.value() == 'today':
            return queryset.filter(start_date__lte=today, end_date__gte=today)

        if self.value() == 'upcoming':
            return queryset.filter(start_date__gt=today)

        return queryset
    
class ConferenceAdmin(admin.ModelAdmin):
    list_display=('title','location','start_date','end_date','price')
    search_fields=('title',)
    list_per_page=1
    ordering=('start_date','price')
    fieldsets = (
        ('Description', {
            "fields": ('title','description','category','location'
                
            ),
           
        }),
        ('Horaire' ,{
             "fields": ('start_date','end_date','created_at','updated_at'
                
            ),
        }
         ),
         ('Documents' ,{
             "fields": ('program',
                
            ),
        }
         )
    )
    readonly_fields=('created_at','updated_at')
    inlines=[ReservationInLine]
    autocomplete_fields=('category',)
    list_filter=('title',ParticipantFilter,ConferenceDateFilter)
    
    
admin.site.register(Conference,ConferenceAdmin)