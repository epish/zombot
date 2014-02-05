# coding=utf-8
import logging
import time
from game_state.game_types import GameDiggerGrave, GameDiggerGraveWithBrains
from game_actors_and_handlers.workers import ResourcePicker


logger = logging.getLogger(__name__)

class BagsPicker(ResourcePicker):
    '''
    {u'gainTime': u'1513587', u'started': True, u'gainDone': 452L, u'item': u'@SC_FISHER_GRAVE_BRAINER', u'materials': 0L, u'y': 24L, u'x': 33L, u'type': u'diggerGraveWithBrains', u'id': 2126L}
    or
    {u'started': True, u'gainDone': 452L, u'item': u'@SC_FISHER_GRAVE_BRAINER', u'materials': 3L, u'y': 24L, u'x': 33L, u'type': u'diggerGraveWithBrains', u'id': 2126L}
    '''

    def get_worker_types(self):
        return [GameDiggerGrave.type, GameDiggerGraveWithBrains.type]
    
    def perform_action(self):

#        event = {"gift":{"item":"@CAKE_RABBIT","user":"4538650","count":100,"msg":""},"id":25,"type":"gift","action":"sendGift"}

#        event = {"id":19,"gift":{"item":"@CAKE_RABBIT","user":"7642260","count":1,"msg":""},"type":"gift","action":"sendGift"}
#        for _ in range (100):
#            time.sleep(5)
#            self._get_events_sender().send_game_events([event])

        graves = self._get_game_location().get_all_objects_by_types(
                            self.get_worker_types())
        for grave in graves:
            if grave.materials:
                logger.info("Собираем мешки " + str(grave.materials) + ' шт.')
            for _ in range(grave.materials):
                self._pick_material(grave, None)
                grave.materials -= 1


class TimeGainEventHandler(object):
    '''
    {"type":"timeGain","action":"start","objId":23196,"gainDone":452,"gainTime":"1867126"}
    '''

    def __init__(self, item_reader, game_location,
                  timer):
        self.__item_reader = item_reader
        self.__game_location = game_location
        self.__timer = timer

    def _get_timer(self):
        return self.__timer

    def handle(self, event_to_handle):
        gameObject = self.__game_location.get_object_by_id(
            event_to_handle.objId
        )
        worker = self.__item_reader.get(gameObject.item).name
        if hasattr(gameObject, 'gainTime') and gameObject.gainTime and self._get_timer().has_elapsed(gameObject.gainTime):
                logger.info(worker + u' принёс')
                gameObject.materials += 1
                gameObject.gainTime = None
        if event_to_handle.action == 'start':
            gameObject.started = True
            gameObject.gainTime = event_to_handle.gainTime
            logger.info(worker + u' принесёт через ' + str((int(gameObject.gainTime) - self._get_timer()._get_current_client_time())/1000/60) + u' мин.')
        else:
            gameObject.started = False
