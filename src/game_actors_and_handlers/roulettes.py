# coding=utf-8
import logging
from game_state.game_types import GameBuilding, GamePlayGame, DailyBonus
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import obj2dict

logger = logging.getLogger(__name__)

                    
class FrutRouletteRoller(BaseActor):

    def perform_action(self):
        # '@R_56' Компот
        # '@R_57' Вишнёвый джем
        # '@R_58' Лимонный микс
        # '@R_59' Мармелад
        # '@S_51' Apple
        ftut_ids = {'@S_51'}
		
        for fr in ftut_ids:
            frut_count=self._get_game_state().count_in_storage(fr)
            if frut_count==0: break
            buildings = self._get_game_location().get_all_objects_by_type(
                            GameBuilding.type)
            for building in list(buildings):
                building_item = self._get_item_reader().get(building.item)
                for game in building_item.games:
                    game_id = game.id
                    play_cost = None
                    if hasattr(game, 'playCost'):
                        play_cost = game.playCost.item
                    #{"type":"roulette","id":"B_SLOT_APPLE_ROULETTE2","level":1,"delayTime":0,"title":"Бонус-Рулетка","hint":"Крути рулетку за 1 Компот, чтобы испытать удачу.","playCost":{"count":1,"image":"storage/recipe_56.png","item":"@R_56"},"prizes":[{"count":1,"item":"@EGG_01"},{"count":5,"item":"@RED_SPEEDUPER"},{"count":1,"item":"@EGG_02"},{"count":10,"item":"@RED_TREE_FERTILIZER"},{"count":5,"item":"@RED_SPEEDUPER"},{"count":1,"item":"@EGG_04"},{"count":10,"item":"@RED_TREE_FERTILIZER"}]}
                    next_play = None
                    next_play_times = building.nextPlayTimes.__dict__
                    if game_id in next_play_times:
                        next_play = int(next_play_times[game_id])
                    if (
                            next_play and
                            self._get_timer().has_elapsed(next_play) and
                            play_cost == fr
                    ):
                        countR=0
                        for i in range(frut_count):
                            roll = GamePlayGame(building.id, game_id)
                            self._get_events_sender().send_game_events([roll])
                            countR+=1
                            self._get_game_state().remove_from_storage(fr,1)
                        logger.info(u"Крутим рулетку %d раз в '%s' %d по координатам (%d,%d)"%(countR,building_item.name,building.id,building.x,building.y))
                        #logger.info(u"Крутим рулетку "+str(countR)+" раз в '"+building_item.name + "' " +str(building.id)+u" по координатам (" +str(building.x) + u", " + str(building.y) + u")")

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

                # Ежедневный бонус
                dailyBonus = self._get_game_state().get_state().dailyBonus
                if int(dailyBonus.playFrom) and self._get_timer().has_elapsed(dailyBonus.playFrom):
                    daily = DailyBonus()
                    self._get_events_sender().send_game_events([daily])
                    logger.info(u"Крутим рулетку: Ежедневный бонус")
                #конец ежедневной рулетке
                    
                # Крутить рулетку в адмирал за глазной суп
                item_count=self._get_game_state().count_in_storage('@R_60')
                if building_item.id == 'B_SOLDIER' and game_id == 'B_SOLDIER_ROULETTE' and item_count>=1:
                    self._get_game_state().remove_from_storage('@R_60',1)
                    play_cost = None
                # Конец адмирала
                
                # Крутить рулетку в аисте за 25 малины
                item_count=self._get_game_state().count_in_storage('@S_57')
                if building_item.id == 'B_TREE_STORK' and game_id == 'B_TREE_STORK_ROULETTE' and item_count>=25:
                    self._get_game_state().remove_from_storage('@S_57',25)
                    play_cost = None
                # Конец аиста
                # Крутить рулетку в казино если фишек = 0
                item_count=self._get_game_state().count_in_storage("@O_CHIPS")
                if (building_item.name==u'Казино'):
                    if (item_count==0) and (not next_play):
                        play_cost = None
                    else: 
                        play_cost = 'Nul'
                # Конец казино
                # Зомби фортуна за 5 фишек
                if (building_item.name==u'Зомби-фортуна') and (game_id == 'B_SLOT_B_ROULETTE1') and item_count>=5:
                    self._get_game_state().remove_from_storage('@O_CHIPS',5)
                    play_cost = None
                    next_play = False
                # Конец зомби фортуны
                
                #print building_item.name
                #print next_play_times
                #print next_play
                #print get_next_play
                #print play_cost
                #print (play_cost is None)
                #print ((not next_play) and (game.level == building.level))
                #print ((next_play and self._get_timer().has_elapsed(next_play)) or ((not next_play) and (game.level == building.level)))
                #raw_input()
                    
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


class GameResultHandler(object):
    def __init__(self, item_reader, game_location,game_state):
        self.__item_reader = item_reader
        self.__game_location = game_location
        self.__game_state_ = game_state

    def handle(self, event_to_handle):
        nextPlayDate = event_to_handle.nextPlayDate
        extraId = event_to_handle.extraId
        obj_id = event_to_handle.objId
        gameObject = self.__game_location.get_object_by_id(obj_id)
        if gameObject is None:
            logger.critical("OMG! No such object")
            return
        else:
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
                        #print 'Rollets'
                        #print prize_item
                        self.__game_state_.add_from_storage(prize_item,count)
                        logger.info(u'Вы выиграли ' + prize.name +
                                    u'(' + str(count) + u' шт.)')
                    else:
                        logger.info('Вы ничего не выиграли.')


class GameDaylyBonusResultHandler(object):
    def __init__ (self, item_reader, game_state):
        self.__item_reader = item_reader
        self.__game_state_ = game_state
        
    def handle(self, event_to_handle):
        dailyBonus = self.__game_state_.get_state().dailyBonus
        if hasattr(event_to_handle.result, 'pos'):
            prize_pos = event_to_handle.result.pos
            print u('result')
        else:
            prize_pos = event_to_handle.pos
            print u('No result')
            
        game_prize = dailyBonus.prizes[prize_pos]
        prize = self.__item_reader.get(game_prize.item)
        count = game_prize.count
        
        self.__game_state_.add_from_storage(prize_item,count)
        logger.info(u'Вы выиграли ' + prize.name +
                    u'(' + str(count) + u' шт.)')
