# coding=utf-8
import logging
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)


class GameBuffHarvest(BaseActor):
    
    def perform_action(self):
        is_there_harvest_buff = False
        buff_list = self._get_game_state().get_state().buffs.list
        for buff in buff_list:
            if buff.item == "@BUFF_FIX_HARVEST_1":
                time_exp = buff.expire.endDate
                is_there_harvest_buff = True
        if is_there_harvest_buff == False or self._get_timer().has_elapsed(time_exp):
            if self._get_game_state().has_in_storage("@BS_BUFF_FIX_HARVEST_1", 1):
                event = {"x":20,"type":"item","y":7,"action":"useStorageItem","itemId":"BS_BUFF_FIX_HARVEST_1"}
                self._get_events_sender().send_game_events([event])
                logger.info(u"Применяю супер-урожай на 24 часа")
                buff_list.append(dict2obj({"item":"@BUFF_FIX_HARVEST_1", "expire": dict2obj({"type":"time", "endDate": str(int(self._get_timer()._get_current_client_time())+86400000)})}))
                self._get_game_state().remove_from_storage("@BS_BUFF_FIX_HARVEST_1", 1)


