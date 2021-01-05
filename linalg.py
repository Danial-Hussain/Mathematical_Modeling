import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import streamlit as st
import pandas as pd
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


class Leontief():

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
		fig1 = plt.figure()
		ax1 = fig1.add_subplot(111)
		ax1.bar(
			self.sectors, 
			self.equilibrium_prod(),
			color = '#353b48')
		ax1.set_xlabel(
			"Sector of the Economy", 
			color = '#273c75'
		)
		ax1.set_ylabel(
			"Production (Billions of $)",
			color = '#273c75'
		)
		ax1.set_title(
			"Equilibrium Production Levels for the Economy",
			color = '#273c75'
		)
		return fig1


# --- Implementation of the Lotka-Volterra Dynamical System ---
# Applications to Ecology

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
			'Predator Death Rate': Predator.get_death_rate()
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
		pred_death = self.parameters['Predator Death Rate']
		return prey_growth, prey_death, pred_growth, pred_death

	def lotka_volterra(self):
		""" Lotka Volterra Equations: Euler method Integration """
		n = int(self.T/self.step)
		time = np.zeros(n)
		prey = np.zeros(n)
		predator = np.zeros(n)
		time[0] = 0.0
		prey[0] = self.x0[0]
		predator[0] = self.x0[1]
		prey_growth, prey_death, pred_growth, pred_death = self.get_params()
		for i in range(n-1):
			time[i+1] = time[i] + self.step
			predator[i+1] = predator[i] + self.step * predator[i] * (pred_growth * prey[i] - pred_death)
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
			fontsize=15
		)
		ax1.set_ylabel(
			ylabel = f"{self.Predator.get_name()} (Population Density)",
			fontsize=15,
			color = self.Predator.get_color(),
		)
		ax2.set_ylabel(
			ylabel = f"{self.Prey.get_name()} (Population Density)",
			fontsize=15,
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
		return fig1


# --- Page Configuration/Layout --- 
st.set_page_config(
	page_title='Implementation of Mathematical Models',
    layout="wide"
)
introduction = st.beta_container()
leontief = st.beta_container()
lotka = st.beta_container()

# --- Container for introductory styling ---
with introduction:

	null1, app_title, null2 = st.beta_columns(3)
	null3, by_title, null4  = st.beta_columns(3)

	app_title.markdown(
		"<h1 style='text-align: center; color: #273c75;'>Mathematical Modeling Streamlit Application</h1>",
		unsafe_allow_html=True
	)
	
	by_title.markdown(
		"<p style='text-align: center; color: #718093;'>Created by Ali Danial Hussain</p>",
		unsafe_allow_html=True
	)

# --- Container for Leontief ---
with leontief:

	st.header("Leontief Input-Output Open Linear System")

	leontief_expander = st.beta_expander(
		"Learn more about the Leontief Input-Output Model"
	)

	st.markdown(
		"""
		In this example there is an economy with three sectors: \
		Mining, Lumber and Energy. Each sector consumes a certain \
		percentage of the production it produces and gives a certain \
		percentage of its production to another sector.\
		Additionally, there is an external demand from\
		the consumer. Change the parameters to see how the equilibrium\
		production levels are effected.
		""")

	table, distributions, chart = st.beta_columns(3)

	econ = table.radio(
			"Choose a economy:",
			('Economy A', 'Economy B', 'Economy C')
		)

	distributions.markdown("### Change the Parameters:")

	demand_external = {}

	for i, val in enumerate(['Mining', 'Lumber', 'Energy']):
		demand_external[f'demand{i}'] =  distributions.slider(
									f"Consumer Demand for {val}",
									min_value = 1,
									max_value = 100,
									value = 10,
									step = 1
								)

	if econ == 'Economy A':
		producer = np.array([
								[0.45, 0.35, 0.15],
								[0.15, 0.25, 0.05],
								[0.05, 0.05, 0.25]
							]) 
	elif econ == 'Economy B':
		producer = np.array([
								[0.40, 0.30, 0.10],
								[0.05, 0.05, 0.65],
								[0.05, 0.20, 0.05]
							]) 
	elif econ == 'Economy C':
		producer = np.array([
								[0.10, 0.10, 0.02],
								[0.60, 0.65, 0.95],
								[0.15, 0.10, 0.02]
							]) 


	df = pd.DataFrame(producer)

	df.columns = pd.MultiIndex.from_product([
		['Distribution of Output By'],['Mining', 'Lumber', 'Energy']
	])

	df = df.rename(
		index = {0: 'Purchased by Mining', 1: 'Purchased by Lumber', 2: 'Purchased by Energy'}
	)

	table.markdown("""### Matrix Representing the Economy""")
	table.write(df)

	chart.markdown("""### Economy Distributions""")
	Sector1 = Sector('Mining', demand_external['demand0'])
	Sector2 = Sector('Lumber', demand_external['demand1'])
	Sector3 = Sector('Energy', demand_external['demand2'])
	sectors = [Sector1, Sector2, Sector3]
	demand = [sector.get_demand() for sector in sectors]

	model = Leontief(
						producer,
						demand, 
						sectors
					)
	chart.write(model.plot_model())


# --- Container for Lotka-Volterra ---
with lotka:

	st.header("Lotka-Volterra Dynamical System")
	lotka_volterra_expander = st.beta_expander(
		"Learn more about the Lotka-Volterra Predator-Prey Model"
	)

	st.markdown(
		"""
		In this example there are two species of animals: \
		Spotted Owls (Predator) and Flying Squirrels (Prey). \
		Both of these species interact in an ecological system. \
		Adjust the parameters below to observe the population dynamics\
		of this ecosystem.
		""")

	param, sliders, chart = st.beta_columns(3)

	sliders.markdown("### Change the Parameters:")
	predator_pop_density = sliders.slider(
			"Predator Population Density",
			min_value = 1,
			max_value = 10,
			value = 5,
			step = 1
		)
	prey_pop_density = sliders.slider(
			"Prey Population Density",
			min_value = 1,
			max_value = 10,
			value = 3,
			step = 1
		)	
	prey_growth_rate = sliders.slider(
			"Growth Rate of Prey Population",
			min_value = 0.1,
			max_value = 5.0,
			value = 2.5,
			step = 0.1
		)
	predation_rate = sliders.slider(
			"Predation Rate",
			min_value = 0.1,
			max_value = 5.0,
			value = 1.3333,
			step = 0.1
		)
	predator_growth_rate = sliders.slider(
			"Reproduction Rate of Predators per Prey Consumed",
			min_value = 0.1,
			max_value = 5.0,
			value = 1.0,
			step = 0.1
		)
	predator_death_rate= sliders.slider(
			"Predator Mortality Rate",
			min_value = 0.1,
			max_value = 5.0,
			value = 1.0,
			step = 0.1
		)
	time= sliders.slider(
			"Time duration",
			min_value = 1,
			max_value = 50,
			value = 30,
			step = 1
		)

	def visualization():
		Predator = Animal(
						'Spotted Owl', 
						predator_pop_density, 
						predator_growth_rate, 
						predator_death_rate, 
						'#576574'
					)
		Prey = Animal(
				'Flying Squirrel', 
				prey_pop_density, 
				prey_growth_rate, 
				predation_rate, 
				'#ff9f43'
			)
		model = PredatorPreyModel(Prey, Predator, time, 0.0001)
		return model.plot_simulation()

	def parameters():
		return str(
			f"""
			### Current Parameters:
			- Growth Rate of Prey Population: {prey_growth_rate}
			- Population Density of Prey: {prey_pop_density}
			- Predation Rate: {predation_rate}
			- Population Density of Predator: {predator_pop_density}
			- Reproduction Rate of Predators per Prey Consumed: {predator_growth_rate}
			- Predator Mortality Rate: {predator_death_rate}
			"""
		)

	param.write(parameters())
	chart.markdown("### Population Dynamics")
	chart.write(visualization())


# --- Expander for Leontieff ---
with leontief_expander:

	st.markdown(
		"""
		### Leontief Input-Output Open Linear System
		The input-output model represents a quantitative economic model that highlights how each sector \
		of the economy is dependent on the other. The model assumes that the total production of the economy\
		 is equal to the total internal demand (i.e demand from each sector of the economy on each other sector)\
		  and the external demand (i.e the demand by the consumers of the product). There are two types of input-output models:

		1. Closed Model: No external demand is present and therefore the total production is equal to the total internal demand
		- Mathematical Representation: ![](https://latex.codecogs.com/gif.latex?X%20%3D%20AX%20%5CLeftrightarrow%20%28I-A%29X%20%3D%200)
		2. Open Model: Sectors of the economy not only satisfy their own need but also an external need.
		- Mathematical Representation: ![](https://latex.codecogs.com/gif.latex?X%3DAX&plus;D%20%5CLeftrightarrow%20%28I-A%29X%3DD%20%5CLeftrightarrow%20X%3D%28I-A%29-D)

		![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5C%5CA%3A%5Cmathrm%7BEconomy%7D%20%5C%5CD%3A%20%5Cmathrm%7BDemand%7D%20%5C%5CI%3A%20%5Cmathrm%7BIdentity%7D)

		Since closed models are quite rare in the real world, I chose to implement the open model for this project.\
		 Leontief's model has been used by a plethora of different institutions and companies ranging from the United\
		  Nations, General Electric and local governments for a range of applications such as calculating GDP, predicting\
		   demand for products/services, and public investments. 
		""")

# --- Expander for Lotka Volterra ---
with lotka_volterra_expander:

	st.markdown(
		"""
		### Lotka-Volterra (Predator-Prey Model) Dynamical System
		The Lotka-Volterra model is a set of differential equations that model the \
		interaction behind a predator and prey species in an ecological system. \
		The equations describe how the populations of the two species evolve offer \
		time depending on the predation rate and the reproduction rate of each species. \
		The model makes various assumptions:
		1. Supplies are abundant for the prey
		2. The population changes relative to its size.
		3. Environmental changes aren't present
		4. The predators can eat endlessly

		The change in the prey's population over time can be represented by the following equation: \
		![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Cfrac%7Bdx%7D%7Bdt%7D%20%3D%20%5Calpha%20x%20-%20%5Cbeta%20xy)

		This equation effectively demonstrates that the prey's population is dependent on its own \
		reproduction rate as well as the rate at which it is preyed upon (predation rate).

		The change in the predator's population over time can be represented by the following equation:\
		 ![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Cfrac%7Bdy%7D%7Bdt%7D%20%3D%20%5Cdelta%20xy%20-%20%5Cgamma%20y)

		This equation effectively delineates that the predator's population is dependent on the rate at\
		 which it grows due to consumption of the prey minus its intrinsic death rate.

		![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5C%5C%5Calpha%3A%20%5Ctextrm%7BGrowth%20Rate%20of%20Prey%20Population%7D%20%5C%5Cx%3A%20%5Ctextrm%7BDensity%20of%20the%20Prey%7D%20%5C%5C%5Cbeta%3A%20%5Ctextrm%7BPredation%20Rate%7D%20%5C%5Cy%3A%20%5Ctextrm%7BDensity%20of%20the%20Predator%7D%20%5C%5C%5Cdelta%3A%20%5Ctextrm%7BReproduction%20Rate%20of%20Predators%20per%20Prey%20Consumed%7D%20%5C%5C%5Cgamma%3A%20%5Ctextrm%7BPredator%20Mortality%20Rate%7D)

		Overall the solutions for the Lotka-Volterra equation highlight that neither species ever goes extinct due to the fact \
		that as the population of animal 1 drops close to zero, animal 2's population skyrockets which then leads to an increase\
		 in the population of animal 1, thus preventing it from going to zero. Ex: Consider a system with two species: spotted owls\
		  (predator) and flying squirrels (prey). If the population of spotted owls drops close to zero, the prey will survive more\
		   often which would thus increase their population. This increase in the population of the flying squirrels, would result\
		    in more food for the spotted owls and thus cause an increase in the population of spotted owls.
		""")