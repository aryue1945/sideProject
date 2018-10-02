#!/usr/bin/env python3

import argparse
import os
import re
from collections import defaultdict
import statistics 
"""
read all the txt report produeced by CPU2006 runspec, and generate report to compare

"""
BLOCKS = 'blocks.dat'
OUTFILE = 'runtimeStat.txt'
BENCHMARK = re.compile(r'(\d{3}\.\w+)')
BASERATE = re.compile(r'(\d+\.\d) [S|\*]')
GEOMEAN = re.compile(r'Est. SPECfp\(R\)_rate_base2006  *(\d+\.\d)')

def getDatafromEachTxt(wholetxt):
  name = re.findall(BENCHMARK, wholetxt)
  rate = re.findall(BASERATE, wholetxt)
  record = zip(name, rate)
  d = defaultdict(list)
  for k, v in record:
    d[k].append(float(v))
  return d, list(d.keys())

def variation(L):
  return (max(L) - min(L))/min(L)*100

def main(args):    
  inputdir = os.path.abspath(args.input_path)
  outputdir = os.path.abspath(args.output_path)

  benchmark = []
  allResults = dict()
  geoMean = dict()

  onlyfiles = [f for f in os.listdir(inputdir) if os.path.isfile(os.path.join(inputdir, f))]
  print(onlyfiles)

  for x in onlyfiles:
    txtfile = open(os.path.join(inputdir, x))
    upperHalf=""
    lowerPart=""
    passFirstHalf = False
    for line in txtfile:
      if not passFirstHalf:
        upperHalf += line
      if passFirstHalf:
        lowerPart += line
      if line == '==============================================================================\n':
        passFirstHalf = True
      if 'Est. SPECfp_rate2006' in line:
        break
    allResults[x.split('.')[0]], n = getDatafromEachTxt(upperHalf)
    geoMean[x.split('.')[0]] = re.findall(GEOMEAN, lowerPart)
    if (len(benchmark) == 0):
      benchmark = n
    if (set(benchmark) != set(n)):
      print("Data not match")
      exit(-1)
  print(geoMean)
  f = open(os.path.join(outputdir,OUTFILE), 'w')
  # report first line - test name
  f.write("\t")
  testname = allResults.keys()
  for x in testname:
    f.write(x + "\t\t")
  f.write("\n")

  # report second line
  f.write("\t")
  for x in testname:
    f.write("median(baseRate)\tvariation%\t")
  f.write("\n")

  # benchmark data
  for b in benchmark:
    f.write(b+"\t")
    for x in testname:
      f.write(str(statistics.median(allResults[x][b]))+"\t")
      f.write(str(round(variation(allResults[x][b]),2))+"\t")
    f.write("\n")
  
  #geoMean
  f.write("\t")
  for x in testname:
    f.write(geoMean[x][0]+"\t\t")
  f.write("\n")

  
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=
  """read blocks.dat file from each sub directory in the input path and
  produce heuristic cost report in the output path""")
  parser.add_argument('input_path', help='input directory')
  parser.add_argument('output_path', help='output directory')

  args = parser.parse_args()
  main(args)