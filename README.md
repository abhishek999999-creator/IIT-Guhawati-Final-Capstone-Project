# 🅿️ Smart Dynamic Parking Price Optimization System

**Using Real-Time Demand, Traffic, and Competitive Intelligence**


## 📖 Introduction

In densely populated cities, parking is a dynamic resource — fluctuating demand, traffic congestion, and rigid pricing models result in poor utilization, long queues, and driver frustration. Static pricing does not adapt to real-time conditions, leading to either underuse or overcrowding of parking lots.

This project proposes a **Smart Dynamic Parking Pricing System**, which uses real-time data streams (occupancy, traffic, queues, competition) to **dynamically calculate optimal prices**, simulate user behavior, and reroute drivers when lots are full — creating a fair, efficient, and intelligent parking environment.

---

## 🎯 Objectives

* Design **three adaptive pricing models**: baseline linear, demand-weighted, and geo-competitive.
* Simulate **real-time price adjustments** as demand changes over time.
* Implement **rerouting logic** to redirect vehicles from full lots to nearby alternatives.
* Provide a **Streamlit dashboard** to visualize price changes and simulate the system interactively.
* Enable smarter city-level parking distribution using data-centric logic.

---

## 🛠️ Tech Stack Used

* **Python**
* **Pathway** (Real-time data streaming)
* **Streamlit** (Web app framework)
* **Plotly** (Interactive visualizations)
* **Pandas** (Data manipulation)
* **NumPy** (Numerical computations)

---


## 📁 Dataset Overview

The dataset simulates parking sensor data and includes the following features:

* **Lot ID**: Unique identifier for each parking location.
* **Capacity**: Maximum number of vehicles that can be parked.
* **Occupancy**: Real-time count of currently parked vehicles.
* **Queue Length**: Vehicles waiting for a spot.
* **Vehicle Type**: Categorical feature (car, bike, van, etc.)
* **Traffic Conditions Nearby**: Encoded value representing congestion near the lot.
* **Special Day Flag**: Boolean for holidays/weekends.
* **Timestamp**: Combined date and time for streaming simulation.
* **Latitude & Longitude**: Coordinates used for geospatial distance calculations (Model 3).

This dataset serves as input for real-time dynamic pricing models and rerouting logic.

---

## 🧹 Data Preprocessing & Feature Engineering

Several steps were applied to prepare the data for dynamic modeling:

* **Datetime Indexing**: Combined `Date` and `Time` into a unified `Timestamp` for simulation streaming.
* **Occupancy Rate Calculation**: Normalized as `occupancy / capacity` for pricing logic.
* **Queue Normalization**: Scaled values for compatibility across lots.
* **Traffic & Special Day Encoding**: Converted categorical inputs to numerical weights.
* **Vehicle Demand Weighting**: Assigned demand stress factors to vehicle types.
* **Geospatial Distance Matrix**: Calculated between all lots using the Haversine formula for rerouting logic.

---

## 🧠 Pricing Models

The project implements three progressively intelligent models, each adding complexity and realism.

---

### 🔹 Model 1: Linear Pricing Based on Occupancy

**Principle**: Price is linearly adjusted based on how full the lot is.

* Price increases proportionally to occupancy rate.
* Simple and interpretable.
* Useful as a baseline.

**Formula**:
`price = base_price + α × (occupancy / capacity)`

**Limitations**:

* Ignores traffic, queue length, and other environmental factors.
* Cannot adapt to special days or vehicle types.

---

### 🔹 Model 2: Multi-Factor Demand-Based Pricing

**Principle**: Prices reflect a composite demand score calculated from multiple real-world factors.

**Demand Score Includes**:

* Occupancy Rate
* Normalized Queue Length
* Traffic Congestion Level
* Special Day Flag (higher base demand)
* Vehicle Type (larger vehicles = higher price impact)

**Formula**:
`price = base_price + α × demand_score`
(*Where demand\_score is a weighted sum of the above factors*)

**Strengths**:

* More adaptive and robust.
* Reflects real-world scenarios better than Model 1.

---

### 🔹 Model 3: Geo-Competitive Pricing with Rerouting

**Principle**: Lots adjust pricing based on surrounding lot conditions and reroute users if full.

**Key Features**:

* **Competitive Pricing**: If a nearby lot (within 1 km) has better availability and lower price, current lot may decrease its price.
* **Rerouting Logic**: When a lot is over 90% full, reroute to the nearest underutilized lot.
* **Proximity Analysis**: Geospatial calculations find nearest alternatives in real time.

**Outcome**:

* Optimizes usage across the network, not just individual lots.
* Prevents overcrowding and improves city-wide traffic flow.

---

## ⏱️ Real-Time Simulation

To mimic a real-time environment, the system streams parking records one-by-one in timestamp order. Each record updates:

* Current lot status (occupancy, queue, traffic).
* Recalculates pricing using the chosen model.
* Triggers rerouting if the lot is full.
* Streams price updates into a timeline, allowing visualization.

This dynamic simulation creates a **temporal dimension** to pricing, offering insight into how prices change during peak vs off-peak hours.

---

## 📊 Interactive Dashboard (Streamlit)

An intuitive **Streamlit-based web app** was developed to simulate and visualize the system.

### 🧩 App Features:

* Upload CSV data for simulation.
* Choose pricing model and parameters (`alpha`, `beta`, etc.).
* Visualize pricing over time using interactive plots (Plotly).
* Track rerouted vehicles and compare nearby lot prices.
* Explore how different lots behave under changing demand.

![image](https://github.com/user-attachments/assets/7807b698-339e-44d7-adff-76f64081d7d2)


### 🎯 Purpose:

Allows urban planners, stakeholders, or students to **experiment interactively** and understand system behavior without deep code involvement.

---

## 📌 Key Results & Insights

* **Model 2** yields smoother, more reasonable pricing by factoring multiple variables.
* **Model 3** is the most realistic, showing how rerouting eases pressure on congested lots.
* **Dynamic pricing helps flatten the demand curve**, encouraging use of underutilized lots.
* **Queue-based pricing** prevents excessive waiting time and spreads traffic more evenly.

---

### 🏗️ Architecture Diagram Description

```
+------------------+         +----------------------+        +---------------------+
|                  |         |                      |        |                     |
|  Real-Time Data   | ----->  |  Data Preprocessing  | -----> |  Pricing Models      |
|  Sources:        |         |  & Feature Engineering|        |  (Model 1, 2, 3)    |
|  - Parking Sensors|         |                      |        |                     |
|  - Traffic APIs  |         +----------------------+        +---------------------+
|  - Queue Status  |                                              |
+------------------+                                              |
                                                                   v
                                                          +---------------------+
                                                          |  Rerouting Logic &   |
                                                          |  Geo-Competitive     |
                                                          |  Pricing Module      |
                                                          +---------------------+
                                                                   |
                                                                   v
                                                          +---------------------+
                                                          | Streamlit Dashboard  |
                                                          | (Visualization &     |
                                                          | Simulation UI)       |
                                                          +---------------------+
                                                                   |
                                                                   v
                                                          +---------------------+
                                                          | User Interaction &   |
                                                          | Parameter Tuning     |
                                                          +---------------------+
```

---

### Explanation:

1. **Real-Time Data Sources:** Data streams from parking sensors, traffic conditions, and queue lengths feed into the system continuously.
2. **Data Preprocessing & Feature Engineering:** Raw data is cleaned, normalized, timestamped, and enriched (e.g., distance matrices) for the pricing models.
3. **Pricing Models:** Three models (linear, demand-based, geo-competitive) compute dynamic prices based on the preprocessed data.
4. **Rerouting Logic:** Geo-competitive pricing adjusts prices and reroutes vehicles to less congested lots.
5. **Streamlit Dashboard:** Offers a user interface for visualizing price changes, simulating demand, and interacting with the system.
6. **User Interaction:** Stakeholders adjust parameters and observe system behavior live.

---


## 🔮 Future Work

* Integrate **live traffic APIs** (e.g., Google Maps) for real-time congestion updates.
* Build a **driver-facing mobile app** that displays optimal nearby parking with live prices.
* Add **reinforcement learning** to self-tune model weights based on revenue vs fairness.
* Use **map-based visualization** for geographic monitoring of all lots.
* Deploy the app publicly using **Streamlit Cloud or AWS Lambda**.

---

## 🛠️ Dependencies

Install the necessary Python packages with:

```bash
pip install pandas numpy streamlit bokeh plotly pathway
```

---

## 🚀 Live App Access

You can access the live application [Live App](https://parkingappproject.streamlit.app/).

---


## 🌟 Acknowledgements

This project was developed as part of Summer Analytics Course 2025 Academic Work at **Indian Institute of Technology (IIT) Guwahati**.

Special thanks to:

* **Pathway** – for real-time data streaming tools.
* **Streamlit** – for rapid dashboard development.
* **OpenStreetMap** – for geospatial context.
* **Plotly & Bokeh** – for powerful interactive plotting.
