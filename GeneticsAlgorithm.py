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
import random
import heapq

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

#parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
GENERATIONS = 100

#calculate total distance of route, starting w/ truck at hub and package addresses
def calculate_fitness(route, truck):
    total_distance = 0
    currentAddress = truck.address
    for package_id in route:
        package = lookUp(package_id)
        if package:
            total_distance += get_distance(currentAddress, package.address)
            currentAddress = package.address
    total_distance += get_distance(currentAddress, addressDict["4001 South 700 East"])
    return total_distance

#shuffle vertexes then append to the arr[]
def copulate(truck_packages):
    population = []
    for i in range(POPULATION_SIZE):
        route = truck_packages.copy()
        random.shuffle(route)  
        population.append(route)
    return population

# combine parts of two routes
def inheritance(parent1, parent2):
    size = len(parent1)
    #create empty route
    child = [None] * size
    #select two points and sort them t
    start, end = sorted([random.randint(0, size - 1) for i in range(2)])
    child[start:end] = parent1[start:end]
    p2_pointer = 0
    #if the child route is empty. add value from 2nd parent
    for i in range(size):
        if child[i] is None:
            while parent2[p2_pointer] in child:
                p2_pointer += 1
            child[i] = parent2[p2_pointer]

    return child

#randomize the route , select two vertices(packages) within the route and swap them
def mutation(route):
    if random.random() < MUTATION_RATE:
        idx1, idx2 = random.sample(range(len(route)), 2)
        route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

#sort by fitness score, keep 50% of the routes from population
def selection(population, truck):
    population_sorted = sorted(population, key=lambda route: calculate_fitness(route, truck))
    return population_sorted[:POPULATION_SIZE // 2]  


def route(truck):
    population = copulate(truck.packages)
    for generation in range(GENERATIONS):
        #select route
        selected_population = selection(population, truck)
        next_population = []
        for i in range(POPULATION_SIZE):
            parent1, parent2 = random.sample(selected_population, 2)
            #inherit
            child = inheritance(parent1, parent2)
            #mutation
            child = mutation(child)
            next_population.append(child)
        population = next_population
    bestRoute = min(population, key=lambda route: calculate_fitness(route, truck))
    return bestRoute

#assign route, truck address, fetch packages and edge weights, and increment miles/time
def init(truck):
    bestRoute = route(truck)
    
    currentAddress = truck.address
    for package_id in bestRoute:
        #fetch package
        package = lookUp(package_id)
        if package:
            distance = get_distance(currentAddress, package.address)
            if package.id == '9' and truck.time > datetime.timedelta(hours=10, minutes=20):
                package.address = addressDict["410 S State St"]
            #increment edge weight / time = distance / 18 * (1 / 60)
            truck.miles += distance
            truck.time += datetime.timedelta(minutes=(distance / (0.3)))
            print(f"Truck {truck.truckID} delivered package {package.id} at {truck.time}")
            currentAddress = package.address
            package.time_delivered = truck.time
            package.truckID = truck.truckID
    #return to hub
    hub = addressDict["4001 South 700 East"]
    distance_to_hub = get_distance(currentAddress, hub)
    truck.miles += distance_to_hub
    truck.time += datetime.timedelta(minutes=(distance_to_hub / (0.3)))
    truck.miles = float(f"{truck.miles:.1f}")

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
    init(truck1)
    init(truck2)
    init(truck3)

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

            if timeStamp <= initTime:
                mg = "at hub"
            elif initTime < timeStamp < tempStorage.time_delivered:
                mg =  "en route"
            elif timeStamp >= tempStorage.time_delivered:
                mg =  "delivered"

            headers = ["Package ID", "Left the Hub At", "Status", "Deliver At", "Deliver To", "Special Notes", "Truck Number"]
            package_data = []

            package_data.append([
                tempStorage.id,
                initTime,
                mg,
                tempStorage.time_delivered,
                tempStorage.address,
                tempStorage.notes,
                tempStorage.truckID
            ])
            print(tabulate(package_data, headers=headers, tablefmt="grid"))

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


    
