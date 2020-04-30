#!/usr/bin/env python
from random import randint
import sys
import argparse
from math import cos


class DiceGroup:
	def __init__(self, die_spec, exploding = False):
		try:
			split_spec = die_spec.split('d')
			self.number = int(split_spec[0])
			self.sides = int(split_spec[1])
			assert self.sides > 0
		except AssertionError:
			print('Dice must all be Euclidian')
			sys.exit(1)
		except:
			print("Please check your die spec.")
			sys.exit(1)
		self.exploding = exploding


	def roll(self):
		rolls = []

		for x in range(self.number):
			roll = randint(1, self.sides)
			rolls.append(roll)
			while self.exploding and roll == self.sides:
				roll = randint(1, self.sides)
				rolls.append(roll)

		self.rolls = rolls


class DieRoll:
	def __init__(self, specs, bonus = None, exploding = None, agon = False):
		self.agon = agon
		self.dice = []
		for spec in specs:
			self.dice.append(DiceGroup(spec, exploding))
		for die in self.dice:
			die.roll()

		self.bonus = bonus

		if self.agon:
			self.working_dice = []
			self.dfours = []
			for die in self.dice:
				if die.sides == 4:
					self.dfours.extend(die.rolls)
				else:
					self.working_dice.extend(die.rolls)
			self.working_dice = sorted(self.working_dice)
			self.dfours = sorted(self.dfours)

			self.printable_working = ', '.join([str(x) for x in self.working_dice])
			if self.dfours:
				self.printable_dfours = ', '.join([str(x) for x in self.dfours])
			else:
				self.printable_dfours = 'Not used.'
		else:
			rolls = []
			for die in self.dice:
				rolls.extend(die.rolls)
			self.total = sum(rolls)

			self.formatted_rolls = ''
			if len(rolls) == 1:
				self.formatted_rolls = rolls[0]
			else:
				for i in range(len(rolls)):
					if i != 0:
						self.formatted_rolls = self.formatted_rolls + ', '
					if int(rolls[i]) == max(rolls):
						self.formatted_rolls = self.formatted_rolls + f'*{rolls[i]}*'
					else:
						self.formatted_rolls = self.formatted_rolls + str(rolls[i])

	def print_rolls(self):
		if self.agon:
			if self.bonus is None:
				print("WARNING: No bonus given. Setting strife to 5.")
				self.bonus = 5
			if self.dfours:
				print(f'\nWorking Dice: {self.printable_working} | Divine Favor: {self.printable_dfours} | Strife: {self.bonus}')
				print(f'  HERO: {self.working_dice[-1]} + {self.working_dice[-2]} + {self.dfours[-1]} = {sum(self.working_dice[-2:], self.dfours[-1])}')
			else:
				print(f'\nWorking Dice: {self.printable_working} | Divine Favor: {self.printable_dfours} | Strife: {self.bonus}')
				print(f'  HERO: {self.working_dice[-1]} + {self.working_dice[-2]} = {sum(self.working_dice[-2:])}')

			print(f'STRIFE: {self.working_dice[-1]} + {self.bonus} = {self.working_dice[-1] + self.bonus}\n')
		else:
			if self.bonus is None:
				self.bonus = 0
			print(f'{self.formatted_rolls}\n{self.total} + {self.bonus} = {self.total + self.bonus}')


def main():
	args = parser.parse_args()

	if args.complex:
		try:
			magnitude = DiceGroup(args.die_spec[0])
			angle = DiceGroup(args.die_spec[1])
			magnitude.roll()
			angle.roll()
			print(f'Your value: {sum(magnitude.rolls) * cos(sum(angle.rolls) / angle.sides)}')
		except:
			print('This is already dumb as hell, I\'m not adding any debugging.')
			sys.exit(2)
		finally:
			sys.exit(0)

	die_roll = DieRoll(args.die_spec, args.bonus, args.exploding, args.agon)
	die_roll.print_rolls()

parser = argparse.ArgumentParser(description = 'Roll arbitrary dice')
parser.add_argument('die_spec',
					help = 'Die specifications, as <n>d<s> (e.g., 1d6)',
					nargs = '+')
parser.add_argument('-b', '--bonus',
					help = 'Bonus to total roll. If rolling for Agon, this is the strife level.',
					type = int)
parser.add_argument('-e', '--exploding',
					help = 'Reroll and add dice which hit max value.',
					action = 'store_true')
parser.add_argument('-a', '--agon',
					help = 'Roll dice as required for the Agon system.',
					action = 'store_true')
parser.add_argument('-i', '--complex',
					help = 'A dumb idea. Roll two groups of dice, first the magnitude and the second the angle (radians, as fraction of sum / sides on dice). Return real component.',
					action = 'store_true')

if __name__ == '__main__':
	main()
