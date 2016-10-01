# encoding=utf8

import random


def gen_pk():
    rand_num = random.random()
    return int(str(rand_num)[2:])
