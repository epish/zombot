# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameStone, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class PirateTreeCut(BaseActor):

    def get_object_type(self):
        return "chop"

    def perform_action(self):
        resources = self._get_game_location().get_all_objects_by_type(
                    self.get_object_type()
                )
        if resources:
            for resource in resources:
                tools = self._get_game_state().get_state().pirate
                tool_needed = resource.chopCount
                type_of_res = resource.item
                type_of_instrument = self._get_item_reader().get(type_of_res).chopInstrumentType
                for tool in tools.instruments:
                    if self._get_item_reader().get(tool.item).chopInstrumentType == type_of_instrument and tool.count >= tool_needed:
                        print tool.count, tool_needed
                        gain_event = {"type":"chop","objId":resource.id,"instruments":{self._get_item_reader().get(tool.item).id:tool_needed},"action":"chop"}
                        print gain_event
                        logger.info("Рубим с помощью " + str(type_of_instrument))
                        self._get_events_sender().send_game_events( [gain_event] )
                        tool.count -= tool_needed
                        break
        else:
            logger.info("Не осталось ресурсов для добычи")

    def __find_first_gain_not_started(self, resources):
        for resource in resources:
            if not resource.gainStarted:
                return resource

#{"type":"pirateCapture","objId":-5333,"action":"capture"} #пиратский клад

