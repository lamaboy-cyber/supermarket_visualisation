from classes import get_transition_probs
from functions import simulate_supermarket, plot

import pandas as pd
import argparse

num_customers = 300
duration = 480

parser = argparse.ArgumentParser(description = "Simulate customer behaviour in a supermarket")
parser.add_argument('-n', '--num_customers', type = int, metavar = '', default = 300, help = 'number of customers')
parser.add_argument('-d', '--duration', type = int, metavar = '', default = 480, help = 'duration of simulation (minutes)')
args = parser.parse_args()


df = simulate_supermarket(args.num_customers, args.duration)
plot(df)
