import random
from collections import deque
from collections import namedtuple
import colorama as colo

colo.init()#autoreset=True)

# class garden_obj():
#     def __init__(self, type=):

class game_Topsoil():
    Garden = namedtuple('Garden', 'plants soil')
    Harvest_Action = 'A'

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

        self._garden = self.Garden(plants=list(in_garden[0]), soil=list(in_garden[1]))
        self._garden_areas = self._init_search_areas()

        self._plant_queue = deque(in_cur_queue[:4])#, maxlen=4) doesn't seem necessary because we pop before adding - iow: it'll stay bounded to 4 anyway
        self._future_que = list(in_future_queue)
        

    def _init_search_areas(self):
        ret = [None for _ in range(16)]
        visited = set()
        area_id = 0
        for seed_coord in range(16): 
            if ret[seed_coord] in visited: continue 

            # start of a new component area
            area_id += 1
            this_area = [seed_coord]
            
            #dfs search for the whole component that matches the soil
            match = self._garden.soil[seed_coord]
            stack = [seed_coord]
            while stack: 
                this_coord = stack.pop()
                if this_coord in visited: continue
                visited.add(this_coord)
                if self._garden.soil[this_coord] == match: this_area.append(this_coord)
                stack.extend(self._coord_neighbors[this_coord])
            
            for c in this_area: ret[c] = area_id
            
        return ret

    def pprint(self, extras=False, post=''):
        print(*self._plant_queue, sep='')
        for row in zip(*[iter(zip(self._garden.plants, self._garden.soil))]*4):
            for cell in row:
                print(self._bg_colors[cell[1]] + cell[0], end='')
            print() #newline
        #if extras: print extra info about areas
        print(colo.Back.WHITE + post, end='')

    def action_at(self, *action_coords): 
        for coord in action_coords:
            ###TODO: validate coordinate as possible plant or harvest location 
            queued_action = self._plant_queue[0]

            if (queued_action != self.Harvest_Action):
                self._plant_at(coord)
            else:
                self._harvest_at(coord)
                self._plant_queue.extend(self.next_plants_in_queue())
                self._plant_queue.append(self.Harvest_Action)

    def _plant_at(self, coord):
        self._garden.plants[coord] = self._plant_queue.popleft()

    def _harvest_at(self, coord):
        #find contigous area of plants at coord
        #remove plants & cycle the soil under those plants
        #score
        pass 
    
    def _top_soil_at(self, coord):
        return self._garden.soil[coord]
    
    def _no_moves(self):
        #return true/false
        pass

    def _cycle_soil(self):
        pass 
    
    def next_plants_in_queue(self):
        #TODO? handle problem for if future_que not a multiple of 3
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

    in_cur_queue="|w|"+game_Topsoil.Harvest_Action,
    in_future_queue="*w|")

g.pprint(post='\n')
g.action_at(6,12,3,3)
g.pprint()