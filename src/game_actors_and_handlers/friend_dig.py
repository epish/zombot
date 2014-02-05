# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class FriendDigger(BaseActor):

    def perform_action(self):

        friends = self._get_options()
        friends = ['[BOT]friend1','[BOT]friend2'] + friends
        logger.info(u"friends %s"%str(friends))
        
        #logger.info(u"gameState %s"%str(self._get_game_state().shovel))
        self._get_game_state().shovel = 0
        logger.info(u"Иду к другу")
        event_go_to_friend = {"action":"gameState","locationId":"main","user":"227218389","type":"gameState"}
        self._get_events_sender().send_game_events([event_go_to_friend])
        
 #       dig = {"x":63,"action":"remoteDig","y":57,"type":"item","objId":159}
#        dig = {"x":72,"action":"remoteDig","y":92,"id":18,"type":"item","objId":41979} # 116164569
        event_dig = {"objId":7203,"x":69,"action":"remoteDig","y":67,"type":"item"}
        dig_count = 3
        for _ in range(dig_count):
            #self._get_events_sender().send_game_events([event_dig])
            logger.info(u"Копаю клад")
        
        logger.info(u"Возвращаюсь на домашний")
        event_return_home ={"action":"gameState","locationId":"main","type":"gameState"} #{"id":14,"action":"gameState","objId":null,"locationId":"main","user":null,"type":"gameState"}
        self._get_events_sender().send_game_events([event_return_home])
        
