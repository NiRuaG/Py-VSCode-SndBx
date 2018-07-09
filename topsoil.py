import random
from collections import deque
from collections import namedtuple
from itertools import cycle
import colorama as colo

colo.init()#autoreset=True)

# class garden_obj():
#     def __init__(self, type=):

class game_Topsoil():
    Garden = namedtuple('Garden', 'plants soil')
    Harvest_Action = 'A'
    soil_cycle = {
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

        self._garden = game_Topsoil.Garden(plants=list(in_garden[0]), soil=list(in_garden[1]))

        #self._garden_areas = self._init_search_areas()
        self._timed_plants = []

        self._plant_queue = deque(in_cur_queue[:4])#, maxlen=4) doesn't seem necessary because we pop before adding - iow: it'll stay bounded to 4 anyway
        self._plant_queue.append(game_Topsoil.Harvest_Action)

        self._future_que = list(in_future_queue)
        self._score = 0
        

    # def _init_search_areas(self):
    #     ret = [None for _ in range(16)]
    #     area_id = 0
    #     for start_area_coord in range(16): 
    #         if ret[start_area_coord]: continue # if not None, the coordinate has an assigned area

    #         # start of a new component area 
    #         area_id += 1
            
    #         #search for contiguous area that matches the soil color
    #         match_soil = self._garden.soil[start_area_coord]
            
    #         dfs_stack = [start_area_coord]
    #         visited = set()
    #         while dfs_stack: 
    #             cur_coord = dfs_stack.pop()
    #             if ret[cur_coord] or cur_coord in visited: continue
    #             visited.add(cur_coord)
    #             if self._garden.soil[cur_coord] != match_soil: continue
                
    #             ret[cur_coord] = area_id
    #             dfs_stack.extend(game_Topsoil._coord_neighbors[cur_coord])
            
    #     return ret

    def pprint(self, extras=False, post=''):
        print(self._score)
        print(*self._plant_queue, sep='')
        for row in zip(*[iter(zip(self._garden.plants, self._garden.soil))]*4):
            for cell in row:
                print(game_Topsoil._bg_colors[cell[1]] + cell[0], end='')
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
        self._garden.plants[coord] = plant
        if plant == '3':
            self._timed_plants.append(coord)


    def _harvest_at(self, coord):
        ###TODO: check if coord is valid harvest (ie has plant)

        self._plant_queue.popleft()

        #find contigous area that matches the soil color & plant
        area = []
        match_soil = self._garden.soil[coord]
        match_plant = self._garden.plants[coord]

        dfs_stack = [coord]
        visited = set()
        while dfs_stack: 
            cur_coord = dfs_stack.pop()
            if cur_coord in visited: continue
            visited.add(cur_coord)
            if (   self._garden.soil[cur_coord]   != match_soil 
                or self._garden.plants[cur_coord] != match_plant): 
                continue
            
            area.append(cur_coord)
            dfs_stack.extend(game_Topsoil._coord_neighbors[cur_coord])

        #'remove' plants & cycle the soil under those plants
        next_soil = game_Topsoil.soil_cycle[match_soil]
        for coord in area:
            self._garden.plants[coord] = ' ' ### ? None ?
            self._garden.soil[coord] = next_soil

        # reduce timed TREES
        for coord in self._timed_plants: 
            # if timed down to 0, replace with TREE
            self._garden.plants[coord] = int(self._garden.plants[coord])-1

        # Score
        if (match_plant in ('|', '*', 'w')):
            self._score += ( len(area) * (len(area)+1) ) // 2
            #print(self._score)
        ### |, * = 1 + 2 + 3 + ..
    
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