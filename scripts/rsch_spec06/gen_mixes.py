#!/usr/bin/python

# NOTE: Don't run twice in one day, it will overwrite both the mix file and backup file
import sys
from os import path
import random
import time

# NUM_MIXES = 32
NUM_MIXES = 128
spec_group_friendly = [462, 410, 433, 434, 437, 447, 459, 470, 481, 482]
spec_group_unfriendly = [400, 401, 403, 429, 445, 456, 458, 464, 471, 473, 483, 416, 435, 436, 444, 450, 453, 454, 465]

spec_group_all = [462, 410, 433, 434, 437, 447, 459, 470, 481, 482, 400, 401, 403, 429, 445, 456, 458, 464, 471, 473, 483, 416, 435, 436, 444, 450, 453, 454, 465]

mix_records_prefix = "/home/junjies/mixes-"
mix_records_suffix = ".txt"
# mix_groups = ["f4", "f1u3", "f2u2", "u4"]
# mix_groups = ["f7", "f3u4", "f5u2", "u7"]
mix_groups = ["a4"]

records = []

def shuffle(l):
  ll = l[:]
  random.shuffle(ll)
  return ll

def is_unique(index):
  for record in records:
    ordered_record = sorted(record)
    ordered_index = sorted(index)
    if ordered_index == ordered_record:
      print index, " and ", record, " matched, skip.."
      return False
  return True

def gen_unique_idx(num_friendly, num_unfriendly, num_all):
  while True:
    if num_all == -1:
      index_1 = shuffle(spec_group_friendly)[0:num_friendly]
      index_2 = shuffle(spec_group_unfriendly)[0:num_unfriendly]
      index = index_1 + index_2
    elif num_friendly == -1 and num_unfriendly == -1:
      index = shuffle(spec_group_all)[0:num_all]

    if is_unique(index):
      #print "Find a unique index: ", index
      return index

# Erase file content

num_friendly = -1
num_unfriendly = -1
num_all = -1
for group in mix_groups:
    if len(group) == 2:
        if group[0] == 'f':
            num_friendly = int(group[1])
            num_unfriendly = 0
            print "choose "+group[1]+" from friendly"
        elif group[0] == 'u':
            num_friendly = 0
            num_unfriendly = int(group[1])
            print "choose "+group[1]+" from unfriendly"
        elif group[0] == 'a':
            num_all = int(group[1])
            print "choose " +group[1]+ " randomly from all"
    elif len(group) == 4:
        num_friendly = int(group[1])
        num_unfriendly = int(group[3])
        print "get " + str(num_friendly) + " from friendly; " + str(num_unfriendly) + " from unfriendly"
    else:
        raise SystemExit

    f = open(mix_records_prefix+group+mix_records_suffix, 'w+')

    random.seed()

    for i in range(0, NUM_MIXES):
        idx = gen_unique_idx(num_friendly, num_unfriendly, num_all)
        print idx
        records.append(idx)

        f.write("-".join(map(str, idx)) + "\n")

