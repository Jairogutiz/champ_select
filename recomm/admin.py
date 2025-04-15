from django.contrib import admin
from .models import ChampionInteraction, Champion

@admin.register(ChampionInteraction)
class ChampionInteractionAdmin(admin.ModelAdmin):
    list_display = ('champion1', 'champion1_role', 'champion2', 'champion2_role', 'interaction_type', 'win_rate', 'delta_wr', 'sample_size')
    list_filter = ('champion1_role', 'champion2_role', 'interaction_type')
    search_fields = ('champion1', 'champion2')

@admin.register(Champion)
class ChampionAdmin(admin.ModelAdmin):
    list_display = ('champion_id', 'name')
    search_fields = ('name',)
