#!/usr/bin/env python3

import argparse
import os
import re
"""
read blocks.dat file from each sub directory in the input path and
produce heuristic cost report in the output path

"""
BLOCKS = 'blocks.dat'
BENCHMARK = re.compile(r'(\w+):\n')
HEURISTIC_COST = re.compile(r'Heuristic cost: (\d+)\n')

def getBenchMarkDict(wholetxt):
  name = re.findall(BENCHMARK, wholetxt)
  cost = re.findall(HEURISTIC_COST, wholetxt)
  dictionary = dict(zip(name, cost))
  return dictionary, name

def getTestName(inputdir):
  algorithms=[]
  for o in os.listdir(inputdir):
    if (os.path.isdir(os.path.join(inputdir, o))):
      txtPath = os.path.join(os.path.join(inputdir, o), BLOCKS)
      if os.path.isfile(txtPath):
        algorithms.append(o)
  return algorithms

def getResults(inputdir):
  benchmarks = []
  algorithms = getTestName(inputdir)
  allResults = dict()
  for x in algorithms:
      txtPath = os.path.join(os.path.join(inputdir, x), BLOCKS)
      txtfile = open(txtPath)
      wholetxt=""
      for line in txtfile:
        wholetxt += line
      allResults[x], n = getBenchMarkDict(wholetxt)
      if len(benchmarks) == 0:
        benchmarks = n
      if (set(benchmarks) != set(n)):
        print("Data not match")
        exit(-1)
  return allResults, algorithms, benchmarks

def main(args): 
    
  inputdir = os.path.abspath(args.input_path)
  outputdir = os.path.abspath(args.output_path)
  OUTFILE = args.reportfilename

  allResults, algorithms, benchmarks = getResults(inputdir)

  # generate report
  if not os.path.exists(outputdir):
      os.makedirs(outputdir)

  f = open(os.path.join(outputdir,OUTFILE), 'w')
  f.write("\t")
  for x in algorithms:
    f.write(x + "\t")
  f.write("\n")
  for b in benchmarks:
    f.write(b+"\t")
    for x in algorithms:
      f.write(allResults[x][b]+"\t")
    f.write("\n")

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=
  """read blocks.dat file from each sub directory in the input path and
  produce heuristic cost report in the output path""")
  parser.add_argument('input_path', help='input directory')
  parser.add_argument('output_path', help='output directory')
  parser.add_argument('reportfilename', help='output directory')

  args = parser.parse_args()

  main(args)

