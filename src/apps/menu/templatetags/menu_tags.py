from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict

from django import template

from apps.menu.models import Menu

register = template.Library()


@dataclass
class MenuDTO:
    id: int
    title: str
    slug: str
    parent_id: Optional[int]
    children: List['MenuDTO'] = field(default_factory=list)


def _get_parents(menu: MenuDTO, menus_map: Dict[int, MenuDTO], result: list) -> List[MenuDTO]:
    if menu.parent_id is not None:
        parent: MenuDTO = menus_map[menu.parent_id]
        result.append(parent)
        return _get_parents(parent, menus_map, result)
    return result


@register.inclusion_tag('menu/menu_template.html')
def draw_menu(menu_slug: Optional[str]) -> dict:
    menus = list(MenuDTO(**menu) for menu in Menu.objects.all().values('id', 'title', 'slug', 'parent_id'))
    menus_map: Dict[int, MenuDTO] = {
        menu.id: menu for menu in menus
    }
    for menu in menus_map.values():
        if not menu.parent_id:
            continue
        menus_map[menu.parent_id].children.append(menu)

    chosen_menu: MenuDTO = [menu for menu in menus_map.values() if menu_slug and menu.slug == menu_slug][0]

    parents: List[MenuDTO] = _get_parents(chosen_menu, menus_map, [])[::-1]
    children: List[MenuDTO] = chosen_menu.children

    return {
        'parents': [asdict(parent) for parent in parents],
        'children': [asdict(ch) for ch in children],
            'selected_menu': asdict(chosen_menu)
    }
