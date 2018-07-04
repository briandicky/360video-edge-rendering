#!/bin/sh

# virginia
ping -c 1000 54.173.80.43 2>&1 | tee -a client_2_virginia_rtt.csv &

# california
ping -c 1000 18.144.29.198 2>&1 | tee -a client_2_california_rtt.csv &

# motreal
ping -c 1000 35.183.47.103 2>&1 | tee -a client_2_montreal_rtt.csv &

# frankfurt
ping -c 1000 18.185.126.92 2>&1 | tee -a client_2_frankfurt_rtt.csv &

# london
ping -c 1000 35.178.82.7 2>&1 | tee -a client_2_london_rtt.csv &

# Saopaulo
ping -c 1000 18.228.24.236 2>&1 | tee -a client_2_saopaulo_rtt.csv &
