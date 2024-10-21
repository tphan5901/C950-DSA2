#studentID: O11746951
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

# 1.5sec for route completion using i5 10th gen cpu 3.6ghz / m.2 ssd. the algorithm may take longer to run initially on new systems
# if that happens, killswitch the program & rerun it in terminal or debug mode until issue fixes

#lookup matching packageID from dictionary. time - space complexity = O(1)
def lookUp(package_id):
    return parsedPackages.get(package_id, None)

#retrieves the edge weight between two addresses. time-space complexity = O(1)
def getdistance(truckaddress, packageaddress):
    try:
        distance = distanceData[truckaddress][packageaddress]
        if distance == '':
            distance = distanceData[packageaddress][truckaddress]
        return float(distance) 
    except:
        print(f"Index error: truckaddress={truckaddress}, packageaddress={packageaddress}")

#Parameters
POPULATION = 100
MUTATION = 0.01 
GENERATIONS = 100

#tally the edge weights from starting point to packageID address. time-space complexity = o(n)
def weights(route, truck):
    totaldistance = 0
    currentAddress = truck.address
    for package_id in route:
        package = lookUp(package_id)
        if package:
            totaldistance += getdistance(currentAddress, package.address)
            currentAddress = package.address
    totaldistance += getdistance(currentAddress, addressDict["4001 South 700 East"])
    return totaldistance

#create route from shuffling the packages for population size then append to the arr[]. time complexity = o(n)
def populate(packages):
    population = []
    for i in range(POPULATION):
        route = packages.copy()
        random.shuffle(route)  
        population.append(route)
    return population

# create a route from two parent routes. o(n^2)
def inheritance(parent1, parent2):
    size = len(parent2)
    #assign child route w/ size of parent
    child = [None] * size
    #select two points from sorted locations
    start, end = sorted([random.randint(0, size - 1) for i in range(2)])
    # assign sub-route to child from parent1 between start- end indices. can inherit 50/50 however more mutations
    child[start:end] = parent1[start:end]
    p2_pointer = 0
    #if child has an empty value. add from parent2. 
    for i in range(size):
        if child[i] is None:
            while parent2[p2_pointer] in child:
                p2_pointer += 1
            #add non-duplicate value from parent2.
            child[i] = parent2[p2_pointer]
    return child

#select two locations within the route and swap them. time-space complexity = o(1)
def mutation(route):
    if random.random() < MUTATION:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

#sort by weights, keep top 3rd of routes from population. time complexity o(1)
def selection(population, truck):
    sort = sorted(population, key=lambda route: weights(route, truck))
    return sort[:POPULATION // 3]  

#child route inherits attributes + mutations from parent routes and contiously in range of generations select optimal path based on shortest weights. 
# time-space complexity o(n^2)
def bestroute(truck):
    population = populate(truck.packages)
    for g in range(GENERATIONS):
        #select route
        selected = selection(population, truck)
        nextpopulation = []
        for i in range(POPULATION):
            #select two parents 
            parent1, parent2 = random.sample(selected, 2)
            #inherit routes from parent
            child = inheritance(parent1, parent2)
            #swap some addresses
            child = mutation(child)
            nextpopulation.append(child)
        population = nextpopulation
    route = min(population, key=lambda route: weights(route, truck))
    return route

#assign route, truck address, fetch packages and edge weights, and increment miles/time. time-space complexity o(n)
def init(truck):
    #best route is selected after 100 generations
    route = bestroute(truck)
    currentAddress = truck.address
    for package_id in route:
        #fetch package
        package = lookUp(package_id)
        if package:
            #obtain edge weights
            distance = getdistance(currentAddress, package.address)
            if package.id == '9' and truck.time > datetime.timedelta(hours=10, minutes=20):
                package.address = addressDict["410 S State St"]
            #increment edge weight / time = distance / 18 * (1 / 60) = 0.3
            truck.miles += distance
            truck.time += datetime.timedelta(minutes=(distance / (0.3)))
            print(f"Truck {truck.truckID} delivered package {package.id} at {truck.time}")
            currentAddress = package.address
            package.time_delivered = truck.time
            package.truckID = truck.truckID
    #return to the hub
    hub = addressDict["4001 South 700 East"] 
    distance_to_hub = getdistance(currentAddress, hub)
    truck.miles += distance_to_hub
    truck.time += datetime.timedelta(minutes=(distance_to_hub / (0.3)))
    truck.miles = float(f"{truck.miles:.1f}")

#init packages dictionary
parsedPackages = {}

#init distance array
distanceData = []

#init dictionary 
addressDict = {}

#parse data from csv file to the initialized dictionary as key-val pairs. time - space complexity O(N) where n is the number of rows
def loadAddresses():
    with open('WGUPS_Addresses.csv', encoding='utf-8-sig') as f:
        rida = csv.reader(f)
        for row in rida:
            index = int(row[0])  # col1 this will be the value
            address = row[2]  # col2 this will be the key. accessing the value, we can use the street name
            addressDict[address] = index 

loadAddresses()

# open csv file , add data from the file to the initialized data structure. time complexity - space complexity O(N) where n is the number of rows
def loadpackage():
    try:
        with open('WGUPS_Package.csv', encoding='utf-8-sig') as f: 
            reader = csv.reader(f, delimiter=',')
            
            for row in reader:
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

                # store package in the dictionary with ID as the key
                parsedPackages[id] = new_package

        return parsedPackages  
    except Exception as e:
        print(f"Error parsing packages: {e}")
        return {}

parsedPackages = loadpackage()

# open csv file, parse every row in the file, append them to the array. time-space complexity O(N) where n is the number of rows
def readdistance():
    with open('distance_data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            distanceData.append(row)
    return distanceData

distanceData = readdistance()

#instantiate new truck object.
truck1Packages = [str(a) for a in [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]]
truck1 = Truck(truck1Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=8, minutes=0), 1)

truck2Packages = [str(b) for b in [3, 6, 18, 22, 23, 25, 27, 28, 32, 33, 35, 36, 38]]
truck2 = Truck(truck2Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=9, minutes=5), 2)

truck3Packages = [str(c) for c in [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 24, 26, 39]]
truck3 = Truck(truck3Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=10, minutes=30), 3)

#print each row in arr. time-space complexity: o(n)
#for a in distanceData:
 #   print(a)
def run():
    init(truck1)
    init(truck2)
    init(truck3)

#interface. space-time complexity = o(n)
def interface():
    print('パキッジ パーセル デリバリー サービス')
    print('**********************')
    totalmiles = round(truck1.miles + truck2.miles + truck3.miles, 2)
    print(f"Route completed in: {totalmiles} miles")
    print(f"Truck 1 miles: {truck1.miles}")
    print(f"Truck 2 miles: {truck2.miles}")
    print(f"Truck 3 miles: {truck3.miles}")
    print('**********************')

 #   print(f"Truck 1 leaves hub at: {datetime.timedelta(hours=8, minutes=0)}")
 #   print(f"Truck 1 returns to hub at: {truck1.time}")
 #   print(f"Truck 2 leaves hub at: {datetime.timedelta(hours=9, minutes=5)}")
 #   print(f"Truck 2 returns to hub at: {truck2.time}")
 #   print(f"Truck 3 leaves hub at: {datetime.timedelta(hours=10, minutes=30)}")
 #   print(f"Truck 3 returns to hub at: {truck3.time}")

    while True:
        print("\nEnter a command (1-3):")
        print("1. Display specific package")
        print("2. Display all package status")
        print("3. Exit")
        selectedNum = int(input())

    
        if selectedNum == 1:
            packageId = input('Enter a Package ID (1-40): ')
            timestamp = input('Enter a time in HH:MM format: ')
            (h, m) = timestamp.split(':')
            timestamp = datetime.timedelta(hours=int(h), minutes=int(m))

            #if package obj in dictionary matches the input, return the package object. O(1)
            tempStorage = lookUp(packageId)
            
            #based on package's truck ID, assign a time when the truck leaves hub and based on timestamp user enters and based on condition, return a msg value. O(1)
            mg = ''
            truckDepartureTime = {
                1: datetime.timedelta(hours=8, minutes=0),
                2: datetime.timedelta(hours=9, minutes=5),
                3: datetime.timedelta(hours=10, minutes=30)
            }
            if tempStorage.truckID == 1:
                initTime = truckDepartureTime[1]
            elif tempStorage.truckID == 2:
                initTime = truckDepartureTime[2]
            elif tempStorage.truckID == 3:
                initTime = truckDepartureTime[3]
            if timestamp <= initTime:
                mg = "at hub"
            elif initTime < timestamp < tempStorage.time_delivered:
                mg =  "en route"
            elif timestamp >= tempStorage.time_delivered:
                mg =  "delivered"

            headers = ["Package ID", "Left Hub at", "Status", "Delivered at", "Deliver to", "Special Notes", "Truck Number"]
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
            timestamp = input('Enter a time in HH:MM format: ')
            (h, m) = timestamp.split(':')
            timestamp = datetime.timedelta(hours=int(h), minutes=int(m))

            print(f"Status of packages at {timestamp}:")
            table_data = []

            #fetch all packages stored from the parsedPackage and insert into p4kages list. time complexity =  O(N), space complexity = O(N) 
            p4ckages = []

            for Package in parsedPackages:
                p4ckages.append(Package)

            status = ""

            #every package obj in list based on its truck ID, we assign truck departure time and based on condition we assign a msg
            for Package in parsedPackages.values():
                msg = ''
                truckDepartureTime = {
                    1: datetime.timedelta(hours=8, minutes=0),
                    2: datetime.timedelta(hours=9, minutes=5),
                    3: datetime.timedelta(hours=10, minutes=30)
                }

                address = Package.address

                if Package.truckID == 1:
                    initTime = truckDepartureTime[1]
                elif Package.truckID == 2:
                    initTime = truckDepartureTime[2]
                elif Package.truckID == 3:
                    initTime = truckDepartureTime[3]
                    
                if timestamp <= initTime:
                    status = "at hub"
                    time_delivered = "Havent left hub"  
                elif initTime < timestamp < Package.time_delivered:
                    status = "en route"
                    time_delivered = Package.time_delivered  
                elif timestamp >= Package.time_delivered:
                    status = "delivered"
                    time_delivered = Package.time_delivered  
                    
                table_data.append([Package.id, address, initTime, status, time_delivered, Package.truckID])
            print(tabulate(table_data, headers=[f"{Fore.BLUE}Package ID{Style.RESET_ALL}", "Address", f"{Fore.LIGHTGREEN_EX}Left hub at{Style.RESET_ALL}", "Status", f"{Fore.CYAN}Current time{Style.RESET_ALL}", "Truck ID"], tablefmt="pretty"))

        elif selectedNum == 3:
            print("Exiting program...")
            break
        else:
            print("incorrect command, retry.")

#main
if "__main__":
    run()
    interface()


    
