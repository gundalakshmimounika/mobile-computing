#!/bin/bash
# Program 30 - run on Ubuntu/WSL inside your ns-3 folder (needs scratch/manet-aodv from Program 29)
echo "rate,tx,rx,pdr,delay_ms,thr_kbps,run" > results.csv
for rate in 64kbps 128kbps 256kbps 512kbps 1024kbps 2048kbps; do
  for run in 1 2 3 4 5; do
    line=$(./ns3 run "scratch/manet-aodv --rate=$rate" --command-template="%s --RngRun=$run" | tail -1)
    echo "$line,$run" >> results.csv
  done
done
