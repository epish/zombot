# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class FriendDigger(BaseActor):

    def perform_action(self):
        go_to_friend = {"action":"gameState","locationId":"main","user":"200961723","type":"gameState"}#{"id":8,"action":"gameState","objId":null,"locationId":"main","user":"200961723","type":"gameState"}
        self._get_events_sender().send_game_events([go_to_friend])
        logger.info(u"Иду к другу")
 #       dig = {"x":63,"action":"remoteDig","y":57,"type":"item","objId":159}
#        dig = {"x":72,"action":"remoteDig","y":92,"id":18,"type":"item","objId":41979} # 116164569
        dig = {"objId":7203,"x":69,"action":"remoteDig","y":67,"type":"item"}
        dig_count = 299
        for _ in range(dig_count):
            self._get_events_sender().send_game_events([dig])
            logger.info(u"Копаю клад")
        friend_ret ={"action":"gameState","locationId":"un_09","type":"gameState"} #{"id":14,"action":"gameState","objId":null,"locationId":"main","user":null,"type":"gameState"}
        self._get_events_sender().send_game_events([friend_ret])
        logger.info(u"Возвращаюсь на домашний")
