# coding=utf-8
import logging
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)

#2013-11-07 03:03:35,344 Переходим на Остров Любви
#2013-11-07 03:03:35,472 Перешли на isle_03
#2013-11-07 03:03:36,045 Не осталось ресурсов для добычи
#2013-11-07 03:04:06,243 Переходим на Дремучий
#2013-11-07 03:04:06,316 Перешли на isle_wild
#2013-11-07 03:04:06,596 Не осталось ресурсов для добычи
#2013-11-07 03:04:36,739 Переходим на Мобильный остров
#2013-11-07 03:04:36,806 Перешли на isle_mobile
#2013-11-07 03:04:37,154 Не осталось ресурсов для добычи
#2013-11-07 03:05:07,326 Переходим на Остров Гигантов



class GameTravelBuff(BaseActor):
    
    def perform_action(self):
        is_there_travel_buff = False
        buff_list = self._get_game_state().get_state().buffs.list
        o_id = False
        for buff in buff_list:
            if buff.item == "@BUFF_TRAVEL_TICKET_TIME" or buff.item == "@BUFF_TRAVEL_TICKET_TIME2":
                time_exp = buff.expire.endDate
                is_there_travel_buff = True
            elif buff.item == "@BUFF_TRAVEL_TICKET_COUNT" or buff.item == "@BUFF_TRAVEL_TICKET_COUNT2":
                #time_exp = buff.expire.count
                time_exp = self._get_timer()._get_current_client_time() + 86400000
                is_there_travel_buff = True
        if is_there_travel_buff == False or self._get_timer().has_elapsed(time_exp):
            for item in self._get_game_state().get_state().gameObjects:
                if item.item == "@B_VAN_ICE_CREAM":
                    exchange = self._get_item_reader().get("B_VAN_ICE_CREAM").crafts
                    o_id = item.id
                elif  item.item == "@B_VAN_ICE_CREAM_CASH":
                    exchange = self._get_item_reader().get("@B_VAN_ICE_CREAM_CASH").crafts
                    o_id = item.id
            if o_id:
                craft = "1"
                exchange = self._get_item_reader().get("B_VAN_ICE_CREAM").crafts
                for one_item in exchange:
                    if one_item.id == craft:
                        sharp = one_item.materials[0].item
                        sharp_count = one_item.materials[0].count
                        books = one_item.materials[1].item
                        books_count = one_item.materials[1].count
                storage = self._get_game_state().get_state().storageItems
                for item in storage:
                    if item.item == sharp:
                        storage_sharp = item.count
                    elif item.item == books:
                        storage_books = item.count
                event = {"itemId":craft,"objId":o_id,"type":"item","action":"craft"}
                self._get_events_sender().send_game_events([event])
                logger.info(self._get_item_reader().get("@BUFF_TRAVEL_TICKET_TIME").name)
                buff_list.append(dict2obj({"item":"@BUFF_TRAVEL_TICKET_TIME", "expire": dict2obj({"type":"time", "time": str(int(self._get_timer()._get_current_client_time())+86400000*5)})}))
                self._get_game_state().remove_from_storage(sharp, sharp_count)
                self._get_game_state().remove_from_storage(books, books_count)
