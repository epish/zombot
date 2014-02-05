# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
import sys
logger = logging.getLogger(__name__)

class DigBot(BaseActor):
   
  def perform_action(self):
    
    i=0
    freeslots=[]
    
    for burySlot in self._get_game_state().get_state().burySlots:
      try:
        print str(i) + " " + burySlot.user
      except:
        print str(i) + " " + 'Free'
        freeslots.append(i)
      i+=1
    
    friends=["202086245","227218389","213708199","232900765","160640012", "230333671", "227641221"]
    
    
    i=0
    for slot in freeslots:
      print (u'Закапываем: ' + friends[slot]).encode('cp866')
      cook_event = {"action":"bury","type":"bury","user":friends[slot],"slot":slot}
      self._get_events_sender().send_game_events([cook_event])
      i+=1
      

    
