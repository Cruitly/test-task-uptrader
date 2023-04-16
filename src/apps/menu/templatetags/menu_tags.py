from typing import Optional

from django import template

from .use_cases import GetMenuContextUseCase

register = template.Library()


@register.inclusion_tag('menu/menu_template.html')
def draw_menu(menu_slug: Optional[str]) -> dict:
    return GetMenuContextUseCase(menu_slug=menu_slug).execute()
