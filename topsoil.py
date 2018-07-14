import random
from collections import deque
from collections import namedtuple
from itertools import cycle
import colorama as colo

colo.init()#autoreset=True)

def group_every(n, iterable):
    fill_sentinel = object()
    args = [iter(iterable)] * n
    for i in zip_longest(fillvalue=fill_sentinel, *args):
        yield i if i[-1] is not fill_sentinel else tuple(v for v in i if v is not fill_sentinel)



class game_Topsoil():
    class Garden_Plot():
        def __init__(self, plant, soil, timer=0, bird=False):
            self.plant = plant
            self.soil = soil
            self.timer = timer
            self.bird = bird

    Harvest_Action = 'V'
    Basic_Plants = ( '|', '*', 'w')
    Timed_Plants = {
        '@': 2, # flowers 
        'A': 3, # pine ['Ѧ','Δ','Ʌ','ѧ']
        'Y': 5, # oak 
        'f': 3  # mushroom 
    }
    _score_mult = {
        '|': 1,  # basic
        '*': 1,  # basic
        'w': 1,  # basic
        '@': 3,  # flowers 
        'A': 6,  # pine 
        'Y': 15, # oak 
        'f': 3   # mushroom
    }
    # flower[2], flower[1], flower[0], 
    # oak[5], oak[4], oak[3], oak[2], oak[1] ♠ Ψ ♀
    # mushroom[3], mr[2], mr[1], mr[0] ȶ ʈ
    # ɷ ʬ ω ᵩ † ⱷ
    
    _soil_cycle = {
        'y': 'g',
        'g': 'b',
        'b': 'y'
    }

    _bg_colors = {
        'y': colo.Back.LIGHTYELLOW_EX,
        'g': colo.Back.LIGHTGREEN_EX,
        'b': colo.Back.LIGHTBLUE_EX
    }
    _coord_neighbors = (
        (     1, 4), (   0, 2, 5), (    1, 3, 6), (    2,   7),
        (0,   5, 8), (1, 4, 6, 9), ( 3, 5, 7,10), ( 3, 6,  11),
        (4,   9,12), (5, 8,10,13), ( 7, 9,11,14), ( 7,10,  15),
        (8,  13   ), (9,12,14   ), (11,13,15   ), (11,14     )
    )

    def __init__(self, in_garden, in_cur_queue, in_future_queue=[]):
        print(colo.Fore.BLACK + colo.Back.WHITE, end='') # default bg/fg colors -- eventually put this to a seperate output class/method for printing game

        # ? TODO: starting garden has more complicated starting plots (with birds, with timers)
        self._garden = [game_Topsoil.Garden_Plot(plant=plant,soil=soil) for plant,soil in zip(in_garden[0],in_garden[1])]

        self._timed_plant_coords = []

        self._plant_queue = deque(in_cur_queue[:4])#, maxlen=4) doesn't seem necessary because we pop before adding - iow: it'll stay bounded to 4 anyway
        self._plant_queue.append(game_Topsoil.Harvest_Action)

        self._future_que = list(in_future_queue)
        self._score = 0

    def pprint(self, extras=False, post=''):
        print(self._score)
        print(*self._plant_queue, sep='')
        for row in group_every(4, self._garden):
            for plot in row: 
                print(game_Topsoil._bg_colors[plot.soil] + (plot.plant if not plot.timer else str(plot.timer)), end='') 
            print() #newline
        #if extras: print extra info about areas
        print(colo.Back.WHITE + post, end='')

    def action_at(self, *action_coords): 
        for coord in action_coords:
            ###TODO: validate coordinate as possible plant or harvest location 
            if (self._plant_queue[0] != game_Topsoil.Harvest_Action):
                self._plant_at(coord)
                if (self._plant_queue[0] == game_Topsoil.Harvest_Action):
                    self._plant_queue.extend(self.next_plants_in_queue())
            else:
                self._harvest_at(coord)
                self._plant_queue.append(game_Topsoil.Harvest_Action)

    def _plant_at(self, coord):
        plant = self._plant_queue.popleft()
        self._garden[coord].plant = plant
        if plant in game_Topsoil.Timed_Plants: 
             self._timed_plant_coords.append(coord) 
             self._garden[coord].timer = game_Topsoil.Timed_Plants[plant]


    def _harvest_at(self, coord):
        ###TODO: check if coord is valid harvest (ie has plant)

        self._plant_queue.popleft()

        #find contigous area that matches the soil color & plant
        harvest_area = []
        match_soil, match_plant = self._garden[coord].soil, self._garden[coord].plant

        dfs_stack = [coord]
        visited = set()
        while dfs_stack: 
            cur_coord = dfs_stack.pop()
            if cur_coord in visited: continue
            visited.add(cur_coord)
            if (self._garden[cur_coord].plant != match_plant 
             or self._garden[cur_coord].soil  != match_soil ): continue
            
            harvest_area.append(cur_coord)
            dfs_stack.extend(game_Topsoil._coord_neighbors[cur_coord])

        #'remove' plants & cycle the soil under those plants
        next_soil = game_Topsoil._soil_cycle[match_soil]
        for coord in harvest_area:
            self._garden[coord].plant = ' '
            self._garden[coord].soil = next_soil

        # reduce timers 
        for coord in self._timed_plant_coords: 
            self._garden[coord].timer -= 1
        self._timed_plant_coords[:] = [x for x in self._timed_plant_coords if not self._garden[x].timer == 0]

        # Score
        if (match_plant in game_Topsoil.Basic_Plants):
            self._score += ( len(area) * (len(area)+1) ) // 2   # = 1 + 2 + 3 + .. + up to length (size of plant area)
        #if (match_plant == '') #flower, pine, oak, mushroom

            
        ### |, * 
    
    # def _top_soil_at(self, coord):
    #     return self._garden.soil[coord]
    
    def _no_moves(self):
        #return true/false
        pass

    def next_plants_in_queue(self):
        ###TODO? handle problem for if future_que not a multiple of 3
        if not self._future_que:
            return list(input('What is the next set of plants in queue? '))
        else:
            ret = self._future_que[:3]
            self._future_que = self._future_que[3:]
            return ret


g = game_Topsoil(
    in_garden=(("  | "
                "   |"
                "w  *"
                " *| "),
               ("yygy"
                "yygy"
                "yggy"
                "ygyy")),

    in_cur_queue="|w|",

    in_future_queue=("*w|**|*ww*|*||www*||ww||||3")
    )

g.pprint(post='\n',extras=True)
g.action_at(
    6,12,3,3,
    15,4,3,14,
    9,14,7,11,
    10,1,5,5,
    12,1,8,13,
    4,5,12,2,
    8,13,11,11,
    3,7,9,7,
    4,3,7,12)
g.pprint()