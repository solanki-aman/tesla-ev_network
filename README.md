# Tesla Supercharging Network

Tesla has been a very popular car in the Electric Cars market. With 20,000+ Superchargers globally, some people still hesitate to buy a Tesla because of the range anxiety. This paper focuses on developing a location optimization model to propose additional Supercharger locations aiming to lower potential buyer’s range anxiety. Additionally, a charging time simulation model emphasis on average charge time any Tesla would take to be fully charged at a nearest Supercharger Station. The Tesla Supercharger Network data is collected from Tesla’s official website using Beautiful Soup (Web Scraping). The visualization were created using Tableau. This paper only takes charging stations in Bay Area into consideration. 
   

<img width="1507" alt="Screenshot 2021-04-07 113537" src="https://user-images.githubusercontent.com/63038070/113917060-98897a80-9795-11eb-80d2-17c38346f29d.png">
<img width="121" alt="Screenshot 2021-04-07 113554" src="https://user-images.githubusercontent.com/63038070/113917058-97f0e400-9795-11eb-8073-96b447055ad2.png">
#### Tesla Supercharging Station in the Bay Area.
#### The size of the circle represents the number of chargers at the stations and the color represents the rate at which the specific Supercharger can charge a Tesla.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="677" alt="Picture1" src="https://user-images.githubusercontent.com/63038070/113916987-7ee83300-9795-11eb-95ad-35a273646edc.png">
<img width="752" alt="Picture2" src="https://user-images.githubusercontent.com/63038070/113916988-7f80c980-9795-11eb-82c2-3ef506aca161.png">
<img width="120" alt="Picture3" src="https://user-images.githubusercontent.com/63038070/113916989-80196000-9795-11eb-86c3-db517c925f71.png">
#### Tree map for Tesla Superchargers in Bay Area Counties.
#### The color represents the rate at which the specific Supercharger can charge a Tesla. The numbers in the box represent the number of station at the specific address.


## Location Optimization Model
The location optimization model proposes coordinates for a new Tesla Supercharger with minimum total distance from all other Superchargers in the Bay Area whereas the Charge Time Simulation model gives an estimate of minimum, maximum and average time it takes for a Tesla to be charged at any Supercharger Station. The idea behind the simulation model is to formulate a practical charging time estimate based on the station’s charge rate probability and car’s EPA estimated range probability. It simply translates to average time any Tesla would take to charge at any Supercharging Station. 
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
	di = √([(xs-xi]^2 + [(ys-yi)]^2 )
#### Objective: minimize distance between two stations: 
	min ∑ di
	
<img width="526" alt="m2" src="https://user-images.githubusercontent.com/63038070/113917569-3715db80-9796-11eb-8691-adda29d49ba5.png">
<img width="532" alt="m1" src="https://user-images.githubusercontent.com/63038070/113917573-37ae7200-9796-11eb-9b71-6d63e9fe6696.png">

	
## Charging Time Simulation Model

| Model Name	| Model Description	| Range (EPA est.) (miles)	| Battery Size (kWh)	| Vehicle Energy Efficiency (miles/kWh) |
| :---: 	| :---: 		| :---: 			| :---: 		| :---: 				|
| Model 3	| Standard Range Plus	| 263				| 75			| 3.506666667				| 
| Model Y	| Performance		| 303				| 80			| 3.7875				| 
| Model 3	| Performance		| 315				| 80			| 3.9375				| 
| Model Y	| Long Range		| 326				| 80			| 4.075					| 
| Model X	| Plaid			| 340				| 85			| 4					| 
| Model 3	| Long Range		| 353				| 85			| 4.152941176				| 
| Model X	| Long Range		| 360				| 85			| 4.235294118				| 
| Model S	| Plaid			| 390				| 90			| 4.333333333				| 
| Model S	| Long Range		| 412				| 90			| 4.577777778				| 
| Model S	| Plaid+		| 521				| 100			| 5.21					| 
#### Table 1.1 – Tesla Car Specifications
#### Source – Tesla.com, Wikipedia.com

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


| Range		| Cars	| Total Cars 	| Probability	| 
| :---: 	| :---:	| :---:		| :---:         | 
| 250-299	| 1	| 10		| 0.1		| 
| 300-349	| 4	| 10		| 0.4		| 
| 350-399	| 3	| 10		| 0.3		| 
| 400-449	| 1	| 10		| 0.1		| 
| 450+		| 1	| 10		| 0.1		| 
#### Table 1.2 – Range Probability of Tesla Car arriving at a Supercharger. 

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


| Charging Rate (kW)	| Stations	| Total Stations	| Probability| 
| :---: 		| :---: 	| :---: 		| :---:      | 
| 72			| 56		| 179			| 0.312849162| 
| 75			| 1		| 179			| 0.005586592| 
| 120			| 2		| 179			| 0.011173184| 
| 150			| 67		| 179			| 0.374301676| 
| 250			| 53		| 179			| 0.296089385| 
#### Table 1.3 – Charging Rate Probability of a Tesla Supercharger Station.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



