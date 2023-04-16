from dataclasses import asdict
from typing import List, Optional, Dict

from .dtos import MenuDTO
from ..models import Menu


class GetMenuContextUseCase:
    def __init__(self, menu_slug: Optional[str]):
        self._menu_slug = menu_slug

    def execute(self) -> dict:
        menus_map = self._get_menus_map()

        chosen_menu: MenuDTO = [
            menu for menu in menus_map.values() if self._menu_slug and menu.slug == self._menu_slug
        ][0]

        parents: List[MenuDTO] = self._get_parents(chosen_menu, menus_map, [])[::-1]
        children: List[MenuDTO] = chosen_menu.children

        return {
            'parents': [asdict(parent) for parent in parents],
            'children': [asdict(ch) for ch in children],
            'chosen_menu': asdict(chosen_menu),
        }

    @staticmethod
    def _get_menus_map() -> Dict[int, MenuDTO]:
        menus = list(MenuDTO(**menu) for menu in Menu.objects.all().values('id', 'title', 'slug', 'parent_id'))

        menus_map: Dict[int, MenuDTO] = {
            menu.id: menu for menu in menus
        }

        for menu in menus_map.values():
            if not menu.parent_id:
                continue
            menus_map[menu.parent_id].children.append(menu)

        return menus_map

    def _get_parents(self, menu: MenuDTO, menus_map: Dict[int, MenuDTO], result: list) -> List[MenuDTO]:
        if menu.parent_id is not None:
            parent: MenuDTO = menus_map[menu.parent_id]
            result.append(parent)
            return self._get_parents(menu=parent, menus_map=menus_map, result=result)
        return result
