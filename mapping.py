import math
import json
import time
import sys

from miner_manager import compute_position_at, Miner, get_miner_position_at, get_miner
from comet_manager import get_all_classic_comets_in_sol
from collision_check import time_range_by_sol
from mapping import *
sys.path.append('tools')
from celestial import *
from rpc import *
from ship_id import getId, id_to_str


hour = 3600
time_range = 1 * hour
ONE_OUT_OF_ = 1


def comet_positions_in_the_next_time_range(sol):
    type = 'classic'
    if sol == 3:
        type = 'rover'
    list_comets = get_all_classic_comets_in_sol(sol, type)
    all_comet_positions = []
    start = int(time.time())
    new_tr = int(time_range * time_range_by_sol[sol])
    for comet in range(len(list_comets)):
        for i in range(new_tr):
            pos = list_comets[comet].current_cartesian_position(start + i)
            p = [pos[0], pos[1], start + i]
            all_comet_positions.append(p)
    return all_comet_positions


def where_to_be_to_hit_comet_in_future(sol):
    miner_ideal_positions = {}
    now = int(time.time())
    all_comet_positions = comet_positions_in_the_next_time_range(sol)
    for i in range(0, len(all_comet_positions), 4):
        pos = compute_position_at(all_comet_positions[i], now)
        miner_ideal_positions[i] = pos
    return miner_ideal_positions


def owner_ship(name, id, sol):
     now = int(time.time())
     miner = get_miner(getId(name, id), sol)
     miner_position  = miner.current_cartesian_position(now)
     result = {'ship':[miner_position[0], miner_position[1], now], 'radius':miner.mining_area}
     return json.dumps(result)


def mappy(sol):
    now = int(time.time())
    miner_ideal_positions = where_to_be_to_hit_comet_in_future(sol)
    return (json.dumps(miner_ideal_positions))


def get_all_miners_in_sol(sol):
    miner_count = miner_manager_contract.functions.countMinerIn(sol).call()
    all_miners = miner_manager_contract.functions.minersPaginated(0, miner_count, sol).call()
    result = []
    now = int(time.time())
    for i in range(0, len(all_miners), ONE_OUT_OF_):
        miner = Miner(all_miners[i])
        miner.update_position(now)
        result.append(miner)
    return (result)

def get_all_miners_in_sol_as_xyt(sol):
    xyts = []
    all_miners = get_all_miners_in_sol(sol)
    now = int(time.time())
    for i in range(len(all_miners)):
        miner = all_miners[i]
        xyts.append([miner.x, miner.y, miner.last_update])
    return json.dumps(xyts)

if __name__ == "__main__":
    result = (get_all_miners_in_sol(100))
    print (len(result), " ships :")
    result.sort(key=lambda x: x.id)
    for miner in result:
        print (id_to_str(miner.id), miner.owner)
    pass
