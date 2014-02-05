# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
import collections
from game_state.game_event import dict2obj, obj2dict

logger = logging.getLogger(__name__)


class ChangeLocationBot(BaseActor):
    '''
    Changes location

    @param options: Available receive options:

    selected_location: location to change to
    '''

    def perform_action(self):
        self.__init_visit_queue()
        next_loc_id = self.__get_next_loc_id()
        self.__change_location(next_loc_id)

    def __init_visit_queue(self):
        if not hasattr(self, '_visit_queue'):
            self._visit_queue = collections.deque()
            for location in self._get_game_state().get_state().locationInfos:
                self._visit_queue.appendleft(location.locationId)

    def __change_location(self, location_id):
        logger.info(u'Переходим на ' + self.__get_location_name(location_id))
        change_location_event = {
          "user": None,
          "locationId" : location_id,
          "type":"gameState",
          "action":"gameState",
          "objId": None
        }
        self._get_events_sender().send_game_events([change_location_event])

    def __get_location_name(self, location_id):
        name = self._get_item_reader().get(location_id).name
        return name

    def __get_next_loc_id(self):
        current_loc_id = self._get_game_state().get_location_id()
        self._visit_queue.appendleft(current_loc_id)
        next_loc_id = self._visit_queue.pop()
        return next_loc_id


class GameStateEventHandler(object):
    def __init__(self, game_state):
        self.__game_state = game_state

    def handle(self, event_to_handle):
        logger.info(u'Перешли на ' + event_to_handle.location.id)
        self.__game_state.set_game_loc(event_to_handle)
