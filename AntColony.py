#studentID: O11746951
#Thinh Phan
import csv
import datetime
from hash import *
from package import *
from truck import *
from collections import deque
from itertools import permutations
from tabulate import tabulate
from colorama import Fore, Style
import heapq
import random
import numpy as np

#returns distance between two weights. time complexity = O(1)
def heuristic(start, end):
    return abs(start - end)

#returns list of neighbor nodes. time complexity = O(1)
def get_neighbors(graph, node):
    return graph[node]

#lookup matching packageID in parsedPackages with passed in parameter ID. time complexity = O(N). space complexity = O(1)
def lookUp(package_id):
    for package in parsedPackages:
        if package.id == package_id:
            return package
    return None

#return edge weight between two addresses. time-space complexity = O(1)
def get_distance(truck_address_index, package_address_index):
    try:
        distance = distanceData[truck_address_index][package_address_index]
        if distance == '':
            distance = distanceData[package_address_index][truck_address_index]
        return float(distance)
    except IndexError:
        print(f"Index error: truck_address_index={truck_address_index}, package_address_index={package_address_index}")
        return float('inf') 


#time-complexity = o(n^3), space complexity = o(n)
# Parameters 
ALPHA = 1        
BETA = 2         
EVAPORATION = 0.5  
ANTS = 20        
ITERATIONS = 100  

#matrix
def initialize_pheromones(num_nodes):
    return np.ones((num_nodes, num_nodes))

# Update the pheromone matrix based on ant paths
def update_pheromones(pheromones, all_paths, all_distances):
    pheromones *= (1 - EVAPORATION)  # Evaporate pheromones
    for path, distance in zip(all_paths, all_distances):
        for i in range(len(path) - 1):
            pheromones[path[i]][path[i+1]] += 1.0 / distance  # Deposit pheromones
    return pheromones

# Calculate probability of choosing the next address based on pheromones and distance
def calculate_probabilities(current_address, unvisited, pheromones, distance_matrix):
    pheromone_values = np.array([pheromones[current_address][i] for i in unvisited])
    distance_values = np.array([distance_matrix[current_address][i] for i in unvisited])
    probabilities = (pheromone_values ** ALPHA) * ((1 / distance_values) ** BETA)
    return probabilities / probabilities.sum()

#run ACO for a single truck
def ant_colony_optimization(truck, distance_matrix):
    num_nodes = len(distance_matrix)
    pheromones = initialize_pheromones(num_nodes)

    best_path = None
    best_distance = float('inf')

    for iteration in range(ITERATIONS):
        all_paths = []
        all_distances = []

        for ant in range(ANTS):
            # Initialize an ant's path starting at the truck's current address
            current_address = truck.address
            unvisited = list(truck.packages)
            path = [current_address]
            total_distance = 0

            while unvisited:
                probabilities = calculate_probabilities(current_address, unvisited, pheromones, distance_matrix)
                next_package = random.choices(unvisited, probabilities)[0]
                distance_to_next = distance_matrix[current_address][next_package]
                total_distance += distance_to_next
                path.append(next_package)
                unvisited.remove(next_package)
                current_address = next_package
            # Return to hub
            total_distance += distance_matrix[current_address][addressDict["4001 South 700 East"]]
            path.append(addressDict["4001 South 700 East"])

            all_paths.append(path)
            all_distances.append(total_distance)

            if total_distance < best_distance:
                best_path = path
                best_distance = total_distance

        # Update pheromones after all ants have completed their paths
        pheromones = update_pheromones(pheromones, all_paths, all_distances)
    return best_path, best_distance


def deliver(truck):
    distance_matrix = np.array(distanceData, dtype=float) 
    best_path, total_distance = ant_colony_optimization(truck, distance_matrix)

    truck.miles += total_distance
    truck.time += datetime.timedelta(minutes=(total_distance / 0.3))

    print(f"Truck {truck.truckID} completed delivery with ACO in {total_distance:.2f} miles")

    # Mark packages as delivered based on the best path
    for package_id in best_path[1:-1]:  # Skip the first (hub) and last (hub return)
        package = lookUp(package_id)
        if package:
            package.time_delivered = truck.time
            package.truckID = truck.truckID

#init packages list
parsedPackages = []

#init distance array
distanceData = []

#Init dictionary 
addressDict = {}

# open csv file then add all row to the initialized dictionary as key-val pairs.
# time complexity O(N), space complexity O(N) where n is the number of rows
def loadAddresses():
    with open('WGUPS_Addresses.csv', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            index = int(row[0])  # col1
            address = row[2]  # col2
            addressDict[address] = index 

loadAddresses()

# open CSV file and add every row from the file to the initialized data structure.
# time complexity O(N), space complexity O(N) where n is the number of rows
def load_package_data():
    try:
        with open('WGUPS_Package.csv', encoding='utf-8-sig') as csvfile: 
            package_reader = csv.reader(csvfile, delimiter=',')
            
            for row in package_reader:
                id = row[0].strip()
                address = row[1].strip()
                city = row[2].strip()
                state = row[3].strip()
                zip_code = row[4].strip()
                deliveryTime = row[5].strip()
                weight = row[6].strip()
                special_notes = row[7].strip()
              
                # get index of the address
                address_index = addressDict[address]
                new_package = Package(id, address_index, city, state, zip_code, deliveryTime, weight, special_notes)

                parsedPackages.append(new_package)

        return parsedPackages  
    except Exception as e:
        print(f"Error parsing packages: {e}")
        return []  

parsedPackages = load_package_data()

# open CSV file, parse every row in the file, append them to the array. time-space complexity O(N) where n is the number of rows
def read_distance_data():
    with open('distance_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            distanceData.append(row)

    return distanceData

distanceData = read_distance_data()


packageKey1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

#loop through every item in list then loop through parsedPackages, check if keys match. add to truck1packages list. time complexity = O(n)
truck1Packages = []
for a in packageKey1:
    package = lookUp(str(a))
    if package:
        truck1Packages.append(package.id)

#truck initialization packages/departure location/time , truckID
truck1 = Truck(truck1Packages, addressDict["4001 South 700 East"], 0,  datetime.timedelta(hours=8, minutes=0), 1)

#truck2
packageKey2 = [3, 6, 18, 22, 23, 25, 27, 28, 32, 33, 35, 36, 38]

#loop through every item in list then loop through parsedPackages, check if keys match. add to truck1packages list. time complexity = O(n), space complexity = O(N)
truck2Packages = []
for b in packageKey2:
    package = lookUp(str(b))
    if package:
        truck2Packages.append(package.id)

truck2 = Truck(truck2Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=9, minutes=10) , 2)

# truck3
packageKey3 = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 24, 26, 39]

#loop through every item in list then loop through parsedPackages, check if keys match. add to truck1packages list. time complexity = O(n^2), space complexity = O(N)
truck3Packages = []
for c in packageKey3:
    for Package in parsedPackages:
        if Package.id == str(c): #parse as str 
            truck3Packages.append(Package.id)

truck3 = Truck(truck3Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=10, minutes=0)  , 3)

#print each row in arr. time-space complexity: O(N)
#for a in distanceData:
#    print(a)

def run():
    deliver(truck1)
    deliver(truck2)
    deliver(truck3)

#interface
def interface():
    print('WGUPS Delivery Service')
    print('**********************')
    total_miles = round(truck1.miles + truck2.miles + truck3.miles, 2)
    print(f"Route completed in: {total_miles} miles")
    print(f"Truck 1 miles: {truck1.miles}")
    print(f"Truck 2 miles: {truck2.miles}")
    print(f"Truck 3 miles: {truck3.miles}")
    print('**********************')

    while True:
        print("\nEnter a command (1-3):")
        print("1. Display specific package")
        print("2. Display all package status")
        print("3. Exit")
        selectedNum = int(input())

        if selectedNum == 1:
            packageId = input('Enter a Package ID (1-40): ')
            timeStamp = input('Enter a time in HH:MM format: ')
            (h, m) = timeStamp.split(':')
            timeStamp = datetime.timedelta(hours=int(h), minutes=int(m))

            # returnPackage = hashTable.search(packageId)
            #   print(type(returnPackage))
            #   print(returnPackage.id)

            #if package obj in list matches the input, we return the package object. O(1)
            tempStorage = lookUp(packageId)
            
            #based on package's truck ID, assign a time when the truck leaves hub and based on timestamp user enters and based on condition, return a msg value. O(1)

            mg = ''
            truckDepartureTime = {
                1: datetime.timedelta(hours=8, minutes=0),
                2: datetime.timedelta(hours=9, minutes=10),
                3: datetime.timedelta(hours=10, minutes=0)
            }
            
            if tempStorage.truckID == 1:
                initTime = truckDepartureTime[1]
            elif tempStorage.truckID == 2:
                initTime = truckDepartureTime[2]
            elif tempStorage.truckID == 3:
                initTime = truckDepartureTime[3]
            
            print('Delivery time', tempStorage.time_delivered)
            print('Departure time', initTime)

            if timeStamp <= initTime:
                mg = "at hub"
            elif initTime < timeStamp < tempStorage.time_delivered:
                mg =  "en route"
            elif timeStamp >= tempStorage.time_delivered:
                mg =  "delivered"


            print(f"\nTimestamp: {timeStamp} \nPackageID: {tempStorage.id} \nLeft the hub at: {initTime} \nStatus: {mg} \nDeliver at: {tempStorage.time_delivered} \nDeliver to: {tempStorage.address} \nSpecial Notes: {tempStorage.notes} \nTruck Number: {tempStorage.truckID}")

        elif selectedNum == 2:
            timeStamp = input('Enter a time in HH:MM format: ')
            (h, m) = timeStamp.split(':')
            timeStamp = datetime.timedelta(hours=int(h), minutes=int(m))

            print(f"Status of packages at {timeStamp}:")
            table_data = []

            #fetch all packages stored from the parsedPackage list and insert them  into p4kages list. time complexity =  O(N), space complexity = O(N) 
            p4ckages = []

            for Package in parsedPackages:
                p4ckages.append(Package)

            status = ""

            #every package obj in list based on its truck ID, we assign truck departure time and based on condition we assign a msg
            for Package in p4ckages:
                msg = ''
                truckDepartureTime = {
                1: datetime.timedelta(hours=8, minutes=0),
                2: datetime.timedelta(hours=9, minutes=5),
                3: datetime.timedelta(hours=10, minutes=0)
                }
    
                address = next(key for key, value in addressDict.items() if value == Package.address)

                if Package.truckID == 1:
                    initTime = truckDepartureTime[1]
                elif Package.truckID == 2:
                    initTime = truckDepartureTime[2]
                elif Package.truckID == 3:
                    initTime = truckDepartureTime[3]
                    
                if timeStamp <= initTime:
                    status = "at hub"
                elif initTime < timeStamp < Package.time_delivered:
                    status = "en route"
                elif timeStamp >= Package.time_delivered:
                    status =  "delivered"
                    
                table_data.append([Package.id, address, status, Package.time_delivered, Package.truckID])
            print(tabulate(table_data, headers=[f"{Fore.BLUE}Package ID{Style.RESET_ALL}", "Address", f"{Fore.LIGHTGREEN_EX}Status{Style.RESET_ALL}", "Deliver by", f"{Fore.CYAN}Truck ID{Style.RESET_ALL}"], tablefmt="pretty"))

        elif selectedNum == 3:
            print("Exiting program...")
            break

        else:
            print("Invalid command, please try again.")

#main executes what is called within scope
if __name__ == "__main__":
    run()
    interface()


    
