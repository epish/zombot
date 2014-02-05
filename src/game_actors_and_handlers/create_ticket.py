# coding=utf-8
import logging
from game_state.game_types import GameBuilding
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)

class CreateTicket(BaseActor):

  #функция создания проездного
  def create_ticket (self, _obj_id):
    create_ticket_event = {"type": "item",
                           "action": "craft",
                           "objId": _obj_id,
                           "itemId":"1"}
    self._get_events_sender().send_game_events([create_ticket_event])

  def perform_action(self):

    _loc = self._get_game_state().get_game_loc().get_location_id()
    if _loc == u'main':

      #получаем id фургона
      buildings = self._get_game_location().get_all_objects_by_type(GameBuilding.type)

      for building in list(buildings):
        building_item = self._get_item_reader().get(building.item)
        if building_item.name == u'Фургон': # или if building_item.id == 'B_VAN_ICE_CREAM'
          obj_id = building.id



      #есть ли на складе альбом и зеленая краска
          
      gr_paint = album =0
      st_items = self._get_game_state().get_state().storageItems

      for _item in list(st_items):
            if hasattr(_item,'item'):
               if _item.item == ('@CR_08'): gr_paint = _item.count
               if _item.item == ('@R_33'): album = _item.count



      #проверяем время окончания бафа /либо его отсутствие/ и создаем проездной
      l_buffs = self._get_game_state().get_state().buffs.list

      l_count = 0
      for l in l_buffs:
        if 'BUFF_TRAVEL_TICKET_TIME' in l.item:
          if l.expire.endDate > 0:
             l_count +=1
           
      if l_count == 0 and gr_paint >= 10 and album >= 1 : self.create_ticket (obj_id)
