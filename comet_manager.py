import json
import time
import sys

sys.path.append('tools')
from celestial import *
from rpc import *


class Comet(Celestial):
    def __init__(self, raw_comet):
        super().__init__(raw_comet[1])


def get_all_classic_comets_in_sol(sol, type='both'):
    list_comet = comet_manager_contract.functions.cometsFrom(sol).call()
    comet_data = []
    if type == 'classic' or type == 'both':
        list_comet_normal = list_comet[0]
    if type == 'both' or type == 'rover':
        list_comet_normal.extend(list_comet[1])
    for i in range(len(list_comet_normal)):
        comet_data.append(Comet(list_comet_normal[i]))
    return comet_data
