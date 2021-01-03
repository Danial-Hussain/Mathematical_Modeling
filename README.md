# LinearAlgebra
In this project, I sought to implement classic mathematical models, with applications to biology and economics, that I learned from computational linear algebra. The two models are as follows:
1. Leontief Input-Output Open Linear System
2. Lotka-Volterra Competition Dynamical System
### Leontief Input-Output Open Linear System
The input-output model represents a quantitative economic model that highlights how each sector of the economy is dependent on the other. The model assumes that the total production of the economy is equal to the total internal demand (i.e demand from each sector of the economy on each other sector) and the external demand (i.e the demand by the consumers of the product). There are two types of input-output models:
1. Closed Model: No external demand is present and therefore the total production is equal to the total internal demand
- Mathematical Representation: ![](https://latex.codecogs.com/gif.latex?X%20%3D%20AX%20%5CLeftrightarrow%20%28I-A%29X%20%3D%200)
2. Open Model: Sectors of the economy not only satisfy their own need but also an external need.
- Mathematical Representation: ![](https://latex.codecogs.com/gif.latex?X%3DAX&plus;D%20%5CLeftrightarrow%20%28I-A%29X%3DD%20%5CLeftrightarrow%20X%3D%28I-A%29-D)

![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5C%5CA%3A%5Cmathrm%7BEconomy%7D%20%5C%5CD%3A%20%5Cmathrm%7BDemand%7D%20%5C%5CI%3A%20%5Cmathrm%7BIdentity%7D)

Since closed models are quite rare in the real world, I chose to implement the open model for this project. Leontief's model has been used by a plethora of different institutions and companies ranging from the United Nations, General Electric and local governments for a range of applications such as calculating GDP, predicting demand for products/services, and public investments.
### Lotka-Volterra Competition Dynamical System
The Lotka-Volterra model is a set of differential equations that model the interaction behind a predator and prey species in an ecological system. The equations describe how the populations of the two species evolve offer time depending on the predation rate and the reproduction rate of each species. The model makes various assumptions:
1. Supplies are abundant fore the prey
2. The population changes relative to its size.
3. Environmental changes aren't present
4. The predators can eat endlessly

The change in the prey's population over time can be represented by the following equation: ![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Cfrac%7Bdx%7D%7Bdt%7D%20%3D%20%5Calpha%20x%20-%20%5Cbeta%20xy)

This equation effectively demonstrates that the prey's population is dependent on its own reproduction rate as well as the rate at which it is preyed upon (predation rate).

The change in the predator's population over time can be represented by the following equation: ![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Cfrac%7Bdy%7D%7Bdt%7D%20%3D%20%5Cdelta%20xy%20-%20%5Cgamma%20y)

This equation effectively delineates that the predator's population is dependent on the rate at which it grows due to consumption of the prey minus its intrinsic death rate.
