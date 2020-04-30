#!/usr/bin/env python
from random import randint
import sys
import argparse
from statistics import mean, median

def interpret_spec(input):
	first_string = input.replace('+', 'd')
	if 'd' in first_string:
		spec = first_string.split('d')
		number = spec[0]
		try:
			sides = spec[1]
			bonus = int(spec[2])
		except:
			sides = spec[1]
			bonus = None
			return(int(number), int(sides), bonus)
	else:
		print("Please check your die spec. Exiting.")
		sys.exit(1)


def roll(number, sides, exploding):
	rolls = []

	for x in range(number):
		roll = randint(1, sides)
		rolls.append(roll)
		while exploding and roll == sides:
			roll = randint(1, sides)
			rolls.append(roll)

	return rolls

def print_rolls(rolls):
	print_rolls = ''
	for i in range(len(rolls)):
		if i != 0:
			print_rolls = print_rolls + ', '
		if int(rolls[i]) == max(rolls):
			print_rolls = print_rolls + f'*{rolls[i]}*'
		else:
			print_rolls = print_rolls + str(rolls[i])
	total = sum(rolls)
	return (print_rolls, total)

def main():
	args = parser.parse_args()
	if args.pick_high:
		keep = 'high'
	elif args.pick_low:
		keep = 'low'
	else:
		keep = None

	if args.agon:
		pass
	else:
		specs = []
		for spec in args.die_spec:
			specs.append(interpret_spec(spec))

		rolls = []
		for spec in specs:
			results = roll(spec[0], spec[1], spec[2], args.exploding, keep = keep)
			print(print_rolls(results[0]))
			print(f'Total: {results[1]}')

parser = argparse.ArgumentParser(description = 'Roll arbitrary dice')
parser.add_argument('die_spec', help = 'Die specifications, as <n>d<s> where n is number and s is sides', nargs = '+')
parser.add_argument('-e', '--exploding', help = 'Reroll and add dice which hit max value.', action = 'store_true')
parser.add_argument('--agon', help = 'Roll dice as required for the Agon system.', action = 'store_true')

picks = parser.add_mutually_exclusive_group(required = False)
picks.add_argument('--pick-high', help = 'Take highest value, not total', action = 'store_true')
picks.add_argument('--pick-low', help = 'Take lowest value, not total', action = 'store_true')

if __name__ == '__main__':
	main()
