import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
import qeds
qeds.themes.mpl_style()


# --- Implementation of Consumer Theory ---

class Item():

	def __init__(self, name, color, price):
		"""
		Parameters:
		----------
		name: the name of the item --> string
		color: the color of the item (hex code) --> string
		price: the price of the item --> float
		"""
		self.name = name
		self.color = color
		self.price = price

	def get_name(self):
		""" Get the name of the item """
		return self.name

	def get_color(self):
		""" Get the color of the item """
		return self.color

	def get_price(self):
		""" Get the price of the item """
		return self.price


class Consumer():

	def __init__(self, Item1, Item2, budget):
		"""
		Parameters:
		----------
		Item1: The first item the consumer purchases --> Item
		Item2: The second item the consumer purchases --> Item
		budget: The consumer's budget --> float
		"""
		self.Item1 = Item1
		self.Item2 = Item2
		self.budget = budget

	def plot_indifference(self, ax, alpha = 1/3):
		""" Plots the indifference Curve """
		ubar = np.arange(1, 11, 2)
		I1 = np.linspace(1, self.budget, 100).reshape((100, 1))
		I2 = ubar**(1/(1-alpha)) * I1**(-alpha/(1-alpha))
		ax.plot(
			I1, 
			I2,
			color = '#576574'
		)
		ax.legend(['Indifference'])

	def plot_budget(self, ax):
		""" Plots the Budget Constraint Curve """
		I1 = np.array([0.0, self.budget/self.Item2.get_price()])
		I2 = (self.budget-I1) / self.Item1.get_price()
		ax.plot(
			I1,
			I2,
			color = "#222f3e"
		)
		ax.set_xlabel(
			xlabel = f"{self.Item1.get_name()}",
			color = self.Item1.get_color()
		)
		ax.set_ylabel(
			ylabel = f"{self.Item2.get_name()}",
			color = self.Item2.get_color()
		)
		ax.fill_between(
			I1,
			0,
			I2,
			alpha = 0.2,
			color = "#222f3e"
		)
		plt.title(
			f"Budget Constraint & Indifference Curve \n{self.Item1.get_name()}s and {self.Item2.get_name()}s"
		)
		ax.tick_params(
			axis="x",
			colors = self.Item1.get_color()
		)
		ax.tick_params(
			axis="y",
			colors = self.Item2.get_color()
		)

	def plot_both(self):
		""" Plots both indifference curve and budget constraint curve """
		fig, ax = plt.subplots()
		self.plot_indifference(ax)
		self.plot_budget(ax)
		plt.show()


# Item1 = Item("Apple", "#ee5253", 2)
# Item2 = Item("Bannana", "#fad390", 1)
# bud = Consumer(Item1, Item2, 20.0)
# bud.plot_both()


# --- Implementation of Fractional Reserve Banking ---

class Reserve():

	def __init__(self, init_deposit, number_of_banks, reserve_ratio):
		"""
		Parameters:
		----------
		init_deposit: The first deposit amount in the first bank --> float
		number_of_banks: The total number of banks in the economy --> float
		reserve_ratio: The reserve ratio --> float
		"""
		self.d0 = init_deposit
		self.i = number_of_banks
		self.r = reserve_ratio

	def sum_of_deposits(self):
		""" Calculates the sum of all deposits in banking system """
		deposits = []
		for i in range(0, self.i+1):
			curr = (1-self.r)**i*self.d0
			if i != 0:
				deposits.append(deposits[-1] + curr)
			else:
				deposits.append(curr)
		plt.plot(
			range(0,self.i+1),
			deposits
		)
		plt.xlabel("Number of Banks")
		plt.ylabel("Total Deposits")
		plt.title("Fractional Reserve Banking")
		plt.show()

	def multiplier(self):
		""" Returns the money multiplier """
		print(f"The money multiplier is: {1/self.r}")


# system = Reserve(500, 400, 0.05)
# system.sum_of_deposits()