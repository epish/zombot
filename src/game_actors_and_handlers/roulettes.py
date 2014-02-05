# coding=utf-8
import logging
import sys
from game_state.game_types import GameBuilding, GamePlayGame
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class RouletteRoller(BaseActor):

    def perform_action(self):
        buildings = self._get_game_location().get_all_objects_by_type(
                        GameBuilding.type)
        for building in list(buildings):
            building_item = self._get_item_reader().get(building.item)
            for game in building_item.games:
                game_id = game.id
                play_cost = None
                if hasattr(game, 'playCost'):
                    play_cost = game.playCost
                next_play = None
                next_play_times = building.nextPlayTimes.__dict__
                if game_id in next_play_times and not game_id == "B_TAVERNA_ROULETTE_1":
                    next_play = int(next_play_times[game_id])
                if (
                        next_play and
                        self._get_timer().has_elapsed(next_play) and
                        play_cost is None
                ):
                    logger.info(
                        u"Крутим рулетку в '" +
                        building_item.name + "' " +
                        str(building.id) +
                        u" по координатам (" +
                        str(building.x) + u", " + str(building.y) + u")")
                    roll = GamePlayGame(building.id, game_id)
                    self._get_events_sender().send_game_events([roll])
                    
class CherryRouletteRoller(BaseActor):

    def perform_action(self):
        cherrys = 0
        fruit = '@S_52' # cherry
        #fruit = '@S_51' #яблоко
        all_items = self._get_game_state().get_state().storageItems
        for one_item in all_items:
            if one_item.item == fruit:
                cherrys = one_item.count
        buildings = self._get_game_location().get_all_objects_by_type(
                        GameBuilding.type)
        for building in list(buildings):
            building_item = self._get_item_reader().get(building.item)
            for game in building_item.games:
                game_id = game.id
                play_cost = None
                if hasattr(game, 'playCost'):
                    play_cost = game.playCost.item
                next_play = None
                next_play_times = building.nextPlayTimes.__dict__
                if game_id in next_play_times:
                    next_play = int(next_play_times[game_id])
                if (
                        next_play and
                        self._get_timer().has_elapsed(next_play) and
                        play_cost == fruit
                ):
                    for _ in range(cherrys/5):
                        logger.info(
                            u"Крутим рулетку в '" +
                            building_item.name + "' " +
                            str(building.id) +
                            u" по координатам (" +
                            str(building.x) + u", " + str(building.y) + u")")
                        roll = GamePlayGame(building.id, game_id)
                        self._get_events_sender().send_game_events([roll])
                    cherrys = 0


class GameResultHandler(object):
    def __init__(self, item_reader, game_location):
        self.__item_reader = item_reader
        self.__game_location = game_location

    def handle(self, event_to_handle):
        nextPlayDate = event_to_handle.nextPlayDate
        extraId = event_to_handle.extraId
        obj_id = event_to_handle.objId
        gameObject = self.__game_location.get_object_by_id(obj_id)
        if gameObject is None:
            logger.critical("OMG! No such object")
        gameObject.nextPlayTimes.__setattr__(extraId, nextPlayDate)
        building = self.__item_reader.get(gameObject.item)
        for game in building.games:
            if game.id == extraId:
                game_prize = None
                if hasattr(event_to_handle.result, 'pos'):
                    prize_pos = event_to_handle.result.pos
                    game_prize = game.prizes[prize_pos]
                elif hasattr(event_to_handle.result, 'won'):
                    prize_pos = event_to_handle.result.won
                    if prize_pos is not None:
                        game_prize = game.combinations[prize_pos].prize
                if game_prize:
                    prize_item = game_prize.item
                    prize = self.__item_reader.get(prize_item)
                    count = game_prize.count
                    logger.info(u'Вы выиграли ' + prize.name +
                                u'(' + str(count) + u' шт.)')
                else:
                    logger.info('Вы ничего не выиграли.')
