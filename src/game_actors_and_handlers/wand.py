# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameStone, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class MagicWand(BaseActor):

    def get_object_type(self):
        return GameWoodTree.type

    def perform_action(self):
        resources = self._get_game_location().get_all_objects_by_type(
                    self.get_object_type()
                )
        while(resources):
            # make sure gain is not started yet
            resource = self.__find_first_gain_not_started(resources)
            if not resource:
                logger.info("Все ресурсы уже добываются")
            else:
                for _ in range(resource.materialCount):
                    gain_event = {"action":"magic","type":"item","objId":resource.id}
                    self._get_events_sender().send_game_events( [gain_event] )
                    resource.gainStarted = True
        else:
            logger.info("Не осталось ресурсов для добычи")

    def __find_first_gain_not_started(self, resources):
        for resource in resources:
            if not resource.gainStarted:
                return resource

