import math
import json
import time
import sys

sys.path.append('tools')
from celestial import *
from ship_id import *
from rpc import *


class Miner(Celestial):
    def __init__(self, miner):
        self.id = miner[0]
        self.owner = miner[1]
        self.pulling_price = miner[3]
        self.mining_area = miner[5]
        self.cooldown = miner[7]
        self.solar_system_id = miner[10]
        self.last_update = miner[2][3]
        super().__init__(miner[2])

    def update_position(self, ts = int(time.time())):
        cartesian = self.current_cartesian_position(ts)
        self.x = cartesian[0]
        self.y = cartesian[1]
        self.last_update = ts


def get_miner(miner_id, solar_system_id):
    miner = miner_manager_contract.functions.getMiner(miner_id, solar_system_id).call()
    result = Miner(miner)
    return result


def get_miner_position_at(miner_id, ts, sol):
    cartesian = miner_manager_contract.functions.minerPosition(miner_id, ts, sol).call()
    return cartesian


def compute_position_at(xyt, ts):
    distance = (xyt[0] ** 2 + xyt[1] ** 2) ** 0.5
    if xyt[0] == 0:
        angle = 0
        angle_2 = 0
    else:
        angle = math.atan2(xyt[1], xyt[0])
        angle_2 = angle + (ts - xyt[2]) * 3.0 / distance
    x_2 = distance * math.cos(angle_2)
    y_2 = distance * math.sin(angle_2)
    return (int(x_2), int(y_2), ts)



