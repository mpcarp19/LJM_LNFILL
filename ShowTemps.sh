#!/bin/bash -l
echo Temp of A-side Detectors
./GetTemps.py T7-470010276.config
echo " "
echo Temp of B-side Detectors
./GetTemps.py T7-470010916.config
