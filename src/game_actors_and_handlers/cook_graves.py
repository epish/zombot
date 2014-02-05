# coding=utf-8
import logging
from game_state.game_types import GameCookGrave, GameCookGraveWithBrains
from game_state.item_reader import LogicalItemReader
from game_actors_and_handlers.workers import ResourcePicker, TargetSelecter

logger = logging.getLogger(__name__)


class BrewPicker(ResourcePicker):

    def get_worker_types(self):
        return [GameCookGrave.type, GameCookGraveWithBrains.type]

class CookerBot(TargetSelecter):
    MAX_PENDING_RECIPES = 3

    def get_worker_types(self):
        return [GameCookGrave.type, GameCookGraveWithBrains.type]

    def is_busy(self, worker):
        return self._get_player_brains().is_using_brains(worker) and\
               (self.has_current_recipe(worker)\
               and len(worker.pendingRecipes) == CookerBot.MAX_PENDING_RECIPES - 1)

    def start_job(self, free_worker):
        logger.info(u"Отправляем поваров на работу")
        if not hasattr(free_worker, "isUp") or not free_worker.isUp:
            start_item_event = {"objId": free_worker.id, "action":"start", "type":"item"}
            self._get_events_sender().send_game_events([start_item_event])
            free_worker.isUp = True
            if free_worker.pendingRecipes:
                free_worker.currentRecipe = free_worker.pendingRecipes.pop()
        empty_buckets = CookerBot.MAX_PENDING_RECIPES - len(free_worker.pendingRecipes)
        if self.has_current_recipe(free_worker):
            empty_buckets -= 1
        cook_item = self._get_options()
        for _ in range(empty_buckets):
            if self.has_enough_ingredients(cook_item.ingridients):
                self.fill_basket(free_worker, cook_item)
                self.remove_ingredients(cook_item.ingridients)
            else:
                logger.info(u"Недостаточно ингредиентов для рецепта '%s'"
                            % cook_item.name)

    def has_enough_ingredients(self, ingredients):
        for ingredient in ingredients:
            if not self._get_game_state().has_in_storage(ingredient.item,
                                                        ingredient.count):
                return False
        return True

    def remove_ingredients(self, ingredients):
        for ingredient in ingredients:
            self._get_game_state().remove_from_storage(ingredient.item,
                                                       ingredient.count)

    def fill_basket(self, free_worker, cook_item):
        logger.info(u"Добавляем в корзину %s" % cook_item.name)
        cook_item_event = {"type": "item", "objId": free_worker.id,
                           "action": "cook", "itemId": cook_item.id}
        self._get_events_sender().send_game_events([cook_item_event])
        if not self.has_current_recipe(free_worker):
            free_worker.currentRecipe = cook_item.id
        else:
            free_worker.pendingRecipes.append(cook_item.id)

    def has_current_recipe(self, free_worker):
        return hasattr(free_worker, "currentRecipe") and free_worker.currentRecipe


class RecipeReader(LogicalItemReader):
    def __init__(self, game_item_reader):
        self._item_reader = game_item_reader

    def _get_item_type(self):
        return 'recipe'

    def _get_all_item_ids(self):
        return self._item_reader.get('recipes').items


# TODO cooker event: set isUp to False, currentRecipe to the next pending recipe
