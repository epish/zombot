# coding=utf-8
import logging
from game_state.game_types import GamePlant, GameFruitTree, GameSlag,\
    GameDigItem, GamePickItem, GameBuyItem
from game_state.item_reader import LogicalItemReader
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class HarvesterBot(BaseActor):

    def perform_action(self):
        plants = self._get_game_location().get_all_objects_by_type(
            GamePlant.type)
        trees = self._get_game_location().get_all_objects_by_type(
            GameFruitTree.type)
        harvestItems = plants + trees
        pick_events = []
        for harvestItem in list(harvestItems):
            pick_event = self._pick_harvest(harvestItem)
            if pick_event:
                pick_events.append(pick_event)
        if pick_events:
            self._get_events_sender().send_game_events(pick_events)

        slags = self._get_game_location().get_all_objects_by_type(
            GameSlag.type)
        dig_events = []
        for slag in list(slags):
            item = self._get_item_reader().get(slag.item)
            logger.info(u"Копаем '" + item.name + "' " + str(slag.id) +
                        u" по координатам (" +
                        str(slag.x) + ", " + str(slag.y) + u")")
            dig_event = GameDigItem(slag.id)
            dig_events.append(dig_event)
            # convert slag to ground
            slag.type = 'base'
            slag.item = '@GROUND'
        if dig_events:
            self._get_events_sender().send_game_events(dig_events)

    def _pick_harvest(self, harvestItem):
        if self._get_timer().has_elapsed(harvestItem.jobFinishTime):
            item = self._get_item_reader().get(harvestItem.item)
            logger.info(u"Собираем '" + item.name + "' " +
                        str(harvestItem.id) +
                        u" по координатам (" +
                        str(harvestItem.x) + u", " + str(harvestItem.y) + u")")
            pick_event = GamePickItem(objId=harvestItem.id)
            if harvestItem.type == GamePlant.type:
                # convert plant to slag
                harvestItem.type = GameSlag.type
                harvestItem.item = GameSlag(0L, 0L, 0L).item
            elif harvestItem.type == GameFruitTree.type:
                harvestItem.fruitingCount -= 1
                if harvestItem.fruitingCount == 0:
                    # remove fruit tree
                    self._get_game_location().remove_object_by_id(
                                                                harvestItem.id)
                    # harvestItem.type = GamePickItem.type
                    # TODO convert to pickup box
                    # convert tree to pick item
            return pick_event


class SeederBot(BaseActor):

    def perform_action(self):
        buy_events = []
        grounds = self._get_game_location().get_all_objects_by_type('ground')
        for ground in list(grounds):
            item = self._get_item_reader().get(ground.item)
            seed_item = self._get_options()
            if not self._is_seed_available(seed_item):
                logger.info(u'Это растение здесь сажать запрещено')
                return
            logger.info(u"Сеем '" + seed_item.name +
                        u"' на '" + item.name + u"' " +
                        str(ground.id) +
                        u" по координатам (" +
                        str(ground.x) + u", " + str(ground.y) + u")")
            buy_event = GameBuyItem(unicode(seed_item.id),
                                    ground.id,
                                    ground.y, ground.x)
            buy_events.append(buy_event)
            ground.type = u'plant'
            ground.item = unicode(seed_item.id)
        if buy_events:
            self._get_events_sender().send_game_events(buy_events)

    def _is_seed_available(self, seed_item):
        seed_reader = GameSeedReader(self._get_item_reader())
        game_state = self._get_game_state()
        return seed_reader.is_item_available(seed_item, game_state)
    

class GameSeedReader(LogicalItemReader):

    def _get_item_type(self):
        return 'seed'

    def _get_all_item_ids(self):
        return self._item_reader.get('shop').seed


class PlantEventHandler(object):
    def __init__(self, game_location):
        self.__game_location = game_location

    def handle(self, event_to_handle):
        gameObject = self.__game_location.get_object_by_id(
            event_to_handle.objId
        )
        if gameObject is None:
            logger.critical("OMG! No such object")
        gameObject.fertilized = True
        logger.info(u'Растение посажено')
        gameObject.jobFinishTime = event_to_handle.jobFinishTime
        gameObject.jobStartTime = event_to_handle.jobStartTime
