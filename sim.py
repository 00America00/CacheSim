#project for Comp Arch
#run with: python3 sim.py -f file.trc -s 512 -b 16 -a 2 -r RR -p 1GB
import math
import os
import sys
import argparse
import random

trace = []

parser = argparse.ArgumentParser()           
parser.add_argument("-f", "--traceFile", dest = "traceFile") #needs to accept 1 to 3 files
parser.add_argument("-s", "--cacheSize", dest = "cacheSize")
parser.add_argument("-b", "--blockSize", dest = "blockSize")
parser.add_argument("-a", "--associativity", dest = "associativity")
parser.add_argument("-r", "--replace", dest = "replace") #replacement policy
parser.add_argument("-p", "--physicalMem", dest = "physicalMem")
args = parser.parse_args()

dataBus = 32 #addressspace
# valid
# if int(args.associativity == (1 or 2 or 4 or 8 or 16 )):
    # print("")
# else:
    # sys.exit("Associativity Invalid: 1KB - 8KB")

if ((int(args.cacheSize) >= 1) and (int(args.cacheSize) <= 8000)):
    print("")
else:
    sys.exit("Cache Size Invalid: 1KB - 8KB")

#milestone #1
print("Cache Simulator CS 3853 Fall 2023 - Group #09 \n")

print("Cache Simulator - CS 3853 - Instructor Version: 2.02 \n")

print("Trace File: "+args.traceFile+"\n") #fix

print("***** Cache Input Parameters *****")
print("Cache Size:\t\t"+args.cacheSize+" KB")
print("Block Size:\t\t"+args.blockSize+" bytes")
print("Associativity:\t\t"+args.associativity)
print("Replacement Policy:\t"+args.replace+"\n")
#print("Physical Memory:\t"+args.physicalMem+"\n")

print ("***** Cache Calculated Values *****")
rows = ((int(args.cacheSize))*1024)/((int(args.associativity))*(int(args.blockSize)))
index = math.log(rows,2)
offset = math.log(int(args.blockSize),2)
tag = dataBus - (index+offset)
totalBlocks = (int(args.cacheSize)*1024)/(int(args.blockSize)) #does floating point
price_per_block = 0.09
print("Total # Blocks:\t\t\t",'%.0f'%(totalBlocks))
print("Tag Size:\t\t\t", '%.0f'%(tag)+" bits")
print("Index Size:\t\t\t",'%.0f'%(index)+" bits")
print("Total # Rows:\t\t\t",'%.0f'%(rows))
overhead = (math.pow(2,tag)+math.pow(2,index)+math.pow(2,offset))-(int(args.blockSize)) 
print("Overhead Size:\t\t\t",'%.0f'%(overhead)+" bytes")
impMem = overhead+(int(args.cacheSize)*1024)
impKB = (overhead+(int(args.cacheSize)*1024))/1024
print("Implementation Memory Size:\t",'%.0f'%(impKB),"KB","("+'%.0f'%(impMem)+" bytes)")
cost = impKB * price_per_block
print("Cost:\t\t\t\t","$"+'%.2f'%(cost)+" @ ($0.09 / KB)\n")

#print 20 lines of the trace file
#file = open(args.traceFile,"r")
#for i in range(20):
#    string = file.readline()
#    print("0x"+string[10:18]+":"+string[4:8]+"\n")
#    string = file.readline()
#    string = file.readline()
#file.close()

def traceThing():
    
    file = open(args.traceFile,"r")
    string = file.readline()
    while string:
        trace.append(string[10:18])
        string = file.readline()
        string = file.readline()
        string = file.readline()
    file.close()

def extract_tag_and_index(address):
    tagbit = address >> int(index)
    indexbit = address & ((1 << int(index)) - 1)
    return tagbit, indexbit
    
if(args.replace == "RR"):
    args.replace = "Round Robin"
    trace()
    cache = [None]*int(totalBlocks)
    
elif(args.replace == "RND"):
    args.replace = "Random"
    traceThing()
    cache = [None]*int(totalBlocks)
    repeatBlocks = set()
    memory_addresses = [int(addr, 16) for addr in trace]

    cache_hits = 0
    cache_misses = 0
    compulsory_misses = 0
    conflict_misses = 0

    for address in memory_addresses:
        tagbit, indexbit = extract_tag_and_index(address)
        
        if cache[indexbit] == tagbit:
            cache_hits += 1
        else:
            cache_misses += 1
        
            if indexbit not in repeatBlocks:
                compulsory_misses += 1
                repeatBlocks.add(indexbit)
            else:
                conflict_misses += 1

                cache[indexbit] = tag

    total_cache_accesses = len(memory_addresses)
    
else:
    sys.exit("Replacement Invalid: RR or RND")

#milestone #2
print ("***** Cache Calculated Values *****\n")
print("Total Cache Accesses: ",total_cache_accesses)
print("Cache Hits: ",cache_hits)
print("Cache Misses:: ",cache_misses)
print("--- Compulsory Misses: ", compulsory_misses)
print("--- Confict Misses: ",conflict_misses,"\n")
print ("***** ***** CACHE HIT & MISS RATE: ***** *****\n")
hit_rate = (cache_hits*100)/total_cache_accesses
print("Hit Rate:",hit_rate,"%")
miss_rate = 1 - hit_rate
print("Miss Rate: ",miss_rate)
print("CPI:","\n\n")

unusedKB = ((totalBlocks - compulsory_misses) * (int(args.blockSize)+overhead)) / int(args.cacheSize)
waste = unusedKB * price_per_block
print("Unused Cache Space: ","$",'%.2f'%(waste))
print("Unused Cache Blocks: ")


