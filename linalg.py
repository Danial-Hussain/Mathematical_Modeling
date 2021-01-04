import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import streamlit as st
import sympy as sp
import qeds
qeds.themes.mpl_style()


# --- Implementation of the Leontief Input-Output Open Linear System ---
# Applications to Economics

class Sector():

	def __init__(self, name, demand):
		"""
		Parameters:
		----------
		name: the name of the sector of the economy --> string
		demand: the consumer demand for this sector of the economy --> float
		"""
		self.name = name
		self.demand = demand

	def get_name(self):
		""" Get the name of the sector of the economy """
		return self.name

	def get_demand(self):
		""" Get the demand for the sector of the economy """
		return self.demand


class Leontieff():

	def __init__(self, producer, consumer, sectors):
		"""
		Parameters:
		----------
		producer: matrix representing production/consumption of economy --> numpy array
		consumer: matrix representing consumer demand for products --> numpy array
		sectors: sectors in the economy --> list of Sector
		"""
		self.economy = producer
		self.length = len(self.economy)
		self.demand = consumer
		self.sectors = [sector.get_name() for sector in sectors]

	def equilibrium_prod(self):
		""" Calculates the equilibrium levels of production for the economy"""
		I = np.identity(self.length)
		I_C = I - self.economy
		I_C_inv = np.linalg.inv(I_C)
		x_hat = np.dot(I_C_inv, self.demand)
		x_hat = [round(x, 2) for x in x_hat]
		return x_hat

	def plot_model(self):
		""" Plots the equilibrium production quantities """
		plt.bar(
			self.sectors, 
			self.equilibrium_prod(),
			color = '#353b48')
		plt.xlabel(
			"Sector of the Economy", 
			color = '#273c75'
		)
		plt.ylabel(
			"Quantity",
			color = '#273c75'
		)
		plt.title(
			"Equilibrium Production Levels for the Economy",
			color = '#273c75'
		)
		plt.show()


# --- Implementation of the Lotka-Volterra Dynamical System ---
# Applications to Biology

class Animal():

	def __init__(self, name, population, growth_rate, death_rate, color):
		"""
		Parameters:
		----------
		name: the name of the animal --> string
		population: the population size of the animal --> float
		growth_rate: the rate at which the animal's population grows --> float
		death_rate: the rate at which the animal's population declines --> float
		"""
		self.name = name
		self.color = color
		self.population = population
		self.growth_rate = growth_rate
		self.death_rate = death_rate

	def get_population(self):
		""" Returns the population of the animal"""
		return self.population

	def get_name(self):
		""" Returns the name of the animal """
		return self.name

	def get_color(self):
		""" Returns the color of the animal """
		return self.color

	def get_growth_rate(self):
		""" Returns the growth rate of the animal """
		return self.growth_rate

	def get_death_rate(self):
		""" Returns the death rate of the animal """
		return self.death_rate

	def __str__(self):
		""" When printing the animal """
		return f"{self.name} | Population: {self.population}"


class PredatorPreyModel():

	def __init__(self, Prey, Predator, T, step):
		"""
		Parameters:
		----------
		Prey: the prey in the model --> Animal
		Predator: the predator in the model --> Animal
		T: the duration of the simulation --> float
		step: the time steps in the simulation --> float
		"""
		self.x0 = np.array(
			[Prey.get_population(), Predator.get_population()]
		)
		self.parameters = {
			'Prey Growth Rate': Prey.get_growth_rate(),
			'Prey Death Rate' : Prey.get_death_rate(),
			'Predator Growth Rate': Predator.get_growth_rate(),
			'Predator Growth Rate': Predator.get_death_rate()
		}
		self.Predator = Predator
		self.Prey = Prey
		self.T = T
		self.step = step

	def get_params(self):
		""" Returns the parameters of the model """
		prey_growth = self.parameters['Prey Growth Rate']
		prey_death = self.parameters['Prey Death Rate']
		pred_growth = self.parameters['Predator Growth Rate']
		pred_death = self.parameters['Predator Growth Rate']
		return prey_growth, prey_death, pred_growth, pred_death

	def lotka_volterra(self):
		""" Lotka Volterra Equations: Euler method """
		n = int(self.T/self.step)
		time = np.zeros(n)
		prey = np.zeros(n)
		predator = np.zeros(n)
		prey[0] = self.x0[0]
		predator[0] = self.x0[0]
		prey_growth, prey_death, pred_growth, pred_death = self.get_params()
		for i in range(n-1):
			time[i+1] = time[i] + self.step
			predator[i+1] = predator[i] + self.step*predator[i] * (pred_growth * prey[i] - pred_death)
			prey[i+1] = prey[i] + self.step * prey[i] * (prey_growth - predator[i] * prey_death)
		return prey, predator, time

	def plot_simulation(self):
		""" Plot the simulation """
		prey, predator, time = self.lotka_volterra()
		fig1 = plt.figure()
		ax1 = fig1.add_subplot(111)
		ax2 = ax1.twinx()
		ax1.set_xlabel(
			'Time (Years)',
			fontsize=22
		)
		ax1.set_ylabel(
			ylabel = f"{self.Predator.get_name()} (Thousands).",
			fontsize=22,
			color = self.Predator.get_color(),
		)
		ax2.set_ylabel(
			ylabel = f"{self.Prey.get_name()} (Thousands).",
			fontsize=22,
			color = self.Prey.get_color()
		)
		ax1.plot(
			time,
			predator,
			label='Predator',
			linestyle='dashed',
			color = self.Predator.get_color()
		)
		ax2.plot(
			time,
			prey,
			label = 'Prey',
			color = self.Prey.get_color()
		)
		plt.title("Predator/Prey Population over Time")
		plt.show()


# Sector1 = Sector('Mining', 7)
# Sector2 = Sector('Lumber', 18)
# Sector3 = Sector('Energy', 26)
# sectors = [Sector1, Sector2, Sector3]
# demand = [sector.get_demand() for sector in sectors]


# model = Leontieff(
# 					np.array([
# 							[0.45, 0.35, 0.15],
# 							[0.15, 0.25, 0.05],
# 							[0.05, 0.05, 0.25]
# 						]),
# 					demand, 
# 					sectors
# 				)
# model.plot_model()

# Predator = Animal('Spotted Owl', 5, 1, 1, '#576574')
# Prey = Animal('Flying Squirrel', 3, 0.6666, 1.3333, '#ff9f43')
# model = PredatorPreyModel(Prey, Predator, 30, 0.0001)
# model.plot_simulation()