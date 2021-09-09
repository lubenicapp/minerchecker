import math
import json
import time
import sys

from comet_manager import get_all_classic_comets_in_sol
from miner_manager import *
sys.path.append('tools')
from ship_id import *

hour = 3600
time_range = 1 * hour
time_range_by_sol = {0: 1, 1: 1, 2: 1, 3: 0.20}
tolerance = 0.35
orbit_time_range = 120

def celestial_distance(a, b):
    sqx = (float(a[0]) - float(b[0])) ** 2
    sqy = (float (a[1]) - float(b[1])) ** 2
    return math.sqrt(sqx + sqy)

def xyt_for_all_comets(sol):
    list_comet = get_all_classic_comets_in_sol(sol)
    all_xyt_for_all_cmt = []
    min = time.time() + orbit_time_range * 5
    for i in range(len(list_comet)):
        all_xyt_for_all_cmt.append(get_xyt_when_comet_is_in_range(list_comet[i], sol))
    for i in range(len(list_comet)):
        entry = all_xyt_for_all_cmt[i][0][2]
        if entry < min:
            result = i
            min = entry
    return all_xyt_for_all_cmt[result]


def get_xyt_when_comet_is_in_range(comet, sol):
    now = time.time()
    min = math.inf
    new_tr = int(time_range * time_range_by_sol[sol])
    for i in range(new_tr):
        comet_position = comet.current_cartesian_position(now + i)
        comet_distance = celestial_distance(comet_position, [0, 0])
        if comet_distance < min:
            min = comet_distance
            min_i = now + i
    all_xyt = []
    for i in range(orbit_time_range):
        ts = now - orbit_time_range / 2 + i
        comet_position = comet.current_cartesian_position(ts)
        all_xyt.append([comet_position[0], comet_position[1], int(ts)])
    return all_xyt


def get_collision_miner_comet_timestamp(miner, comet, sol):
    min = math.inf
    min_i = 0
    start = int(time.time())
    miner_pos = get_miner_position_at(miner.id, start + min_i, sol)
    miner_distance = math.sqrt(miner_pos[0] ** 2 + miner_pos[1] ** 2)
    for i in range(time_range):
        comet_position = comet.current_cartesian_position(start + i)
        comet_distance = celestial_distance(comet_position, [0, 0])
        if comet_distance < min:
            min = comet_distance
            min_i = i
        if math.fabs(comet_distance - miner_distance) < miner.mining_area - tolerance:
            miner_position = get_miner_position_at(miner.id, start + i, sol)
            if celestial_distance(comet_position, miner_position) < miner.mining_area:
                return 1, i
    print (min, min_i, get_miner_position_at(miner.id, start + min_i, sol))
    return 0, i


def check_collisions_miner_sol(miner, sol):
        list_comet = get_all_classic_comets_in_sol(sol)
        result = -1
        for i in range(len(list_comet)):
            result = get_collision_miner_comet_timestamp(miner, list_comet[i], sol)
            if result[0] == 1:
             break
        if result[0] == 1:
            return "collision in {} seconds".format(result[1])
        else:
            return "no collision in the next {} seconds".format(int(time_range * time_range_by_sol[sol]))


def check_for_ship_in_sol(ship_name, ship_nb, solar_system):
    try:
        miner_id = getId(ship_name, ship_nb)
        miner = (get_miner(miner_id, solar_system - 1))
        str = check_collisions_miner_sol(miner, solar_system - 1)
        return ship_name + " : " + str
    except:
        return "something went wrong"
