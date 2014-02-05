# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_types import GameApplyGiftEvent, GameGift
logger = logging.getLogger(__name__)

class TricksReceiverBot(BaseActor):
    def perform_action(self):
        # Тыквы
        towers = self._get_game_location().\
                    get_all_objects_by_type('halloweenTower')
        count = 0
        for tower in towers:
            for user in tower.users:
                count += self._get_item_reader().get(user.itemId).count
                apply_tower_event = {"type":"item",
				                    "action":"trick",
				                    "objId":tower.id,
				                    "itemId":user.itemId,
				                    "extraId":user.id}
                self._get_events_sender().send_game_events([apply_tower_event])
            tower.users = []
        if count > 0:
            logger.info(u"Собрали %d хелоуинских плюшек" % count)
