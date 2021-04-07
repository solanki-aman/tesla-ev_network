# Tesla Supercharging Network

Tesla has been a very popular car in the Electric Cars market. With 20,000+ Superchargers globally, some people still hesitate to buy a Tesla because of the range anxiety. This paper focuses on developing a location optimization model to propose additional Supercharger locations aiming to lower potential buyer’s range anxiety. Additionally, a charging time simulation model emphasis on average charge time any Tesla would take to be fully charged at a nearest Supercharger Station. The Tesla Supercharger Network data is collected from Tesla’s official website using Beautiful Soup (Web Scraping). The visualization were created using Tableau. This paper only takes charging stations in Bay Area into consideration. 

The location optimization model proposes coordinates for a new Tesla Supercharger with minimum total distance from all other Superchargers in the Bay Area whereas the Charge Time Simulation model gives an estimate of minimum, maximum and average time it takes for a Tesla to be charged at any Supercharger Station. The idea behind the simulation model is to formulate a practical charging time estimate based on the station’s charge rate probability and car’s EPA estimated range probability. It simply translates to average time any Tesla would take to charge at any Supercharging Station.    


## Location Optimization Model
### Model Formulation:
#### Inputs:
	i – Supercharger Station, i = 1, …,45
	xi , yi  = Coordinates of  Supercharger Station
	xi  = Longitude of  Supercharger Station (x-coordinates)
	yi = Latitude of Supercharger Station (Absolute value) (y-coordinates)
#### Decision variables:
	xs ,ys = Coordinates of New Supercharger Station
#### Calculated value:
	di = Distance between New Supercharger Station and Existing Supercharger Station:
	d_i=√(〖(x_s-x_i)〗^2+〖(y_s-y_i)〗^2 )
#### Objective: minimize distance between two stations: 
	∑ di

