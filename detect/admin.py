from django.contrib import admin
from .models import Player, Card, Paper

class CardInLine(admin.TabularInline):
	model = Card
	extra = 0

class PaperInLine(admin.TabularInline):
	model = Paper
	extra = 0

class PlayerAdmin(admin.ModelAdmin):
	inlines = [CardInLine,PaperInLine]
	search_fields = ['nickname']
	list_display = ('nickname', 'join_time', 'profile_photo')


admin.site.register(Player, PlayerAdmin)
