from django import template
from recomm.models import Champion

register = template.Library()

@register.filter(name='champion_icon_url')
def champion_icon_url(champion_name):
    """Convert champion name to icon URL"""
    try:
        if not champion_name:
            return ''
        champion = Champion.objects.get(name=champion_name)
        return f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champion.champion_id}.png"
    except Champion.DoesNotExist:
        return ''

@register.filter(name='role_icon_url')
def role_icon_url(role):
    """Convert role name to icon URL"""
    role_map = {
        'top': 'position-top',
        'jungle': 'position-jungle',
        'middle': 'position-middle',
        'bottom': 'position-bottom',
        'support': 'position-utility'
    }
    
    base_role = role_map.get(role.lower(), 'position-utility')
    return f"https://raw.communitydragon.org/pbe/plugins/rcp-fe-lol-static-assets/global/default/svg/{base_role}.svg"

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)