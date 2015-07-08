from django.contrib import admin
from main.models import State

class StateAdmin(admin.ModelAdmin):
	list_display = ('name', 'abbreviation', 'capital')
	search_fields = ('name',)

admin.site.register(State, StateAdmin)