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

# the algorithm may take longer to run initially on new systems
# if that happens, killswitch the program & rerun it in terminal or debug mode until issue fixes

#lookup with packageID from dictionary. time - space complexity = O(1)
def lookUp(id):
    return parsedPackages.get(id, None)

#retrieves the edge weight between two addresses. time-space complexity = O(1)
def getdistance(truckaddress, packageaddress):
    try:
        distance = distanceData[truckaddress][packageaddress]
        if distance == '' or distance is None:
            distance = distanceData[packageaddress][truckaddress]
        # return distance as float 
        return float(distance)
    except Exception as e:
        print(f"Error: {e}")


#Parameters
POPULATION = 100
MUTATION = 0.01 
GENERATIONS = 100

#create the routes from truck packages and randomized them. time complexity = o(n)
def populate(packages):
    population = []
    for i in range(POPULATION):
        route = packages.copy()
        random.shuffle(route)  
        population.append(route)
    return population

#tally the edge weights from starting point to package address. time-space complexity = o(n)
def weights(route, truck):
    totaldistance = 0
    currentAddress = truck.address
    for packageID in route:
        package = lookUp(packageID)
        if package:
            totaldistance += getdistance(currentAddress, package.address)
            currentAddress = package.address
    totaldistance += getdistance(currentAddress, addressDict["4001 South 700 East"])
    return totaldistance

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
        for p in range(POPULATION):
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
    #best route 
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

#distance arr
distanceData = []

#init dictionary 
addressDict = {}

#parse file, append data to initialized dictionary as key-val pairs. time - space complexity O(N) where n is the number of rows
def loadAddresses():
    with open('WGUPS_Addresses.csv', encoding='utf-8-sig') as f:
        rida = csv.reader(f)
        for row in rida:
            index = int(row[0])  # col1 this will be the value
            address = row[2]  # col2 this will be the key. accessing the value, we can use the street name
            addressDict[address] = index 

# parse file, append data to initialized dictionary. time complexity - space complexity O(N) where n is the number of rows
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
                address = addressDict[address]
                newpackage = Package(id, address, city, state, zip_code, deliveryTime, weight, special_notes)

                # store package in the dictionary with ID as the key
                parsedPackages[id] = newpackage

        return parsedPackages  
    except Exception as e:
        print(f"Error parsing packages: {e}")
        return {}

#parse data from the file, append them to the array. time-space complexity O(N) where n is the number of rows
def readdistance():
    with open('distance_data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            distanceData.append(row)
    return distanceData

loadAddresses()
parsedPackages = loadpackage()
distanceData = readdistance()


#instantiate new truck object. loadup truck
truck1Packages = [str(a) for a in [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]]
truck1 = Truck(truck1Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=8, minutes=0), 1)

truck2Packages = [str(b) for b in [3, 6, 18, 22, 23, 25, 27, 28, 32, 33, 35, 36, 38]]
truck2 = Truck(truck2Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=9, minutes=5), 2)

truck3Packages = [str(c) for c in [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 24, 26, 39]]
truck3 = Truck(truck3Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=10, minutes=10), 3)

#assign packages to trucks based on notes. space-time complexity O(N^2)
def assignPackages(parsedPackages, trucks):
    try:
        for package in parsedPackages.values():
            assigned = False
            special_notes = package.notes
            delivery_time = package.deliveryTime
        
            # assign to trucks based on special conditions
            if "Can only be on truck 2" in special_notes:
                trucks[1].packages.append(package)  
                assigned = True
            elif "Must be delivered with" in special_notes:
                # extract related packages in order to deliver
                related_ids = [id.strip() for id in special_notes.split("Must be delivered with")[1].split(",")]
                for related_id in related_ids:
                    related_package = parsedPackages.get(related_id.strip())
                    if related_package:
                        trucks[0].packages.append(related_package)  
                trucks[0].packages.append(package)  
                assigned = True
            elif "Delayed on flight---will not arrive to depot until 9:05 am" in special_notes:
                trucks[1].packages.append(package) 
                assigned = True
            elif "Wrong address listed" in special_notes:
                trucks[2].packages.append(package) 
                assigned = True
            elif "EOD" in delivery_time:
                trucks[2].packages.append(package)  
                assigned = True
            if not assigned:
                trucks[2].packages.append(package) 

    except Exception as e:
        print(f"Exception assigning packages: {e}")

trucks = [None, truck1, truck2, truck3]  
assignPackages(parsedPackages, trucks)


#print(truck1.lookUp(1))
#print(truck1.lookUp(2))
#print(truck1.lookUp(3))

#print each row in arr. time-space complexity: o(n)
#for a in distanceData:
#   print(a)

def run():
    init(truck1)
    init(truck2)
    init(truck3)

#interface. space-time complexity = o(n)
def interface():
    print('Package Parcel Delivery Service')
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
                3: datetime.timedelta(hours=10, minutes=10)
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
                    3: datetime.timedelta(hours=10, minutes=10)
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


    
