# coding=utf-8
import logging
from game_state.game_types import GamePickPickup, GamePickItem, GamePickup
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)


class Pickuper(BaseActor):

    def perform_action(self):
        pickups = self._get_game_location().get_pickups()
        self.pick_pickups(pickups)

    def pick_pickups(self, pickups):
        if pickups:
            logger.info(u'Подбираем дроп...')
        for pickup in pickups:
            pick_event = GamePickPickup([pickup])
            self._get_events_sender().send_game_events([pick_event])
            self._get_game_location().remove_pickup(pickup)


class BoxPickuper(BaseActor):

    def getOpeningPriceMsg(self, boxItem):
        openingPrice = boxItem.openingPrice[0]
        count = openingPrice.count
        item_name = self._get_item_reader().get(openingPrice.item).name
        price_msg = u'%d %s' % (count, item_name)
        return price_msg

    def perform_action(self):
        boxes = self._get_game_location().get_all_objects_by_type(
                                                    GamePickup.type)
        for box in boxes:
            name = self._get_item_reader().get_name(box)
            boxItem = self._get_item_reader().get(box.item)
            if hasattr(boxItem, 'openingPrice'):
                logger.info(u'Открыть %s можно за %s' %
                            (name, self.getOpeningPriceMsg(boxItem)))
            else:
                logger.info(u'Вскрываем %s' % name)
                pick_event = GamePickItem(objId=box.id)
                self._get_events_sender().send_game_events([pick_event])
                self._get_game_location().remove_object_by_id(box.id)


class AddPickupHandler(object):
    def __init__(self, game_location):
        self.__game_loc = game_location

    def handle(self, event_to_handle):
        for pickup in event_to_handle.pickups:
            item_type_msg = {
                'coins':
                    lambda pickup: u'денег',
                'xp':
                    lambda pickup: u'опыта',
                'collection':
                    lambda pickup: u'предмет(а) коллекции %s' % pickup.id,
                'storageItem':
                    lambda pickup: u'предмет(а) %s' % pickup.id,
                'shovel':
                    lambda pickup: u'лопат(ы)',
                'scrapItem':
                    lambda pickup: u'шт. металлолома'
            }.get(pickup.type, lambda pickup: pickup.type)(pickup)
            logger.info(u'Подбираем %d %s по координатам (%d,%d)' %
                        (pickup.count, item_type_msg, pickup.x, pickup.y))
        self.__game_loc.add_pickups(event_to_handle.pickups)
