#!/usr/bin/env python3
from sys import argv
import sqlite3
from datetime import datetime
from MarkovChain import MarkovChain
from config import COMMENT_FILE, MARKOV_DB, MIN_LEN, LOG_FILE

mc = MarkovChain(MARKOV_DB)

def makeDatabase():
    with open(COMMENT_FILE, 'r') as f:
        mc.generateDatabase(f.read())
        mc.dumpdb()

def printComments(qty):
    for i in range(0, qty):
        x = mc.generateString()
        while len(x) < MIN_LEN:
            x = mc.generateString()
        print(str(i) + " - " + x[:140])

def singleComment():
    comment = mc.generateString()
    while len(comment) < MIN_LEN:
        comment = mc.generateString()
    return comment

def singleCommentSeed(seed):
    up_seed = str(seed).upper()
    comment = mc.generateStringWithSeed(up_seed)
    while len(comment) < MIN_LEN:
        comment = mc.generateStringWithSeed(up_seed)
    return comment

def logError(message):
    now = datetime.now().strftime('%y-%m-%d %H:%M:%S')
    output = now + ": " +str(message)
    with open(LOG_FILE,'a') as f:
        f.write(output)


def usage():
    print("Usage:\t" + argv[0] + " comment [N# of comments]"\
        "\n\t"+argv[0]+" makedatabase" )

if __name__ == "__main__":
    qty = 10
    if 'makedatabase' in argv:
        makeDatabase()
    elif 'comment' in argv:
        try:
            qty = int(argv[2])
        except:
            pass
        printComments(qty)
    else:
        usage()