#studentID: O11746951
#Thinh Phan
import csv
import datetime
from hash import *
from package import *
from collections import deque
from tabulate import tabulate #[pip install tabulate] in the CLI b4 running my code
import heapq
from colorama import Fore, Style
import random

POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.1

#truck class object
class Truck:
    def __init__(self, packages, address, miles, time, truckID):
        self.packages = packages
        self.address = address
        self.miles = miles
        self.time = time
        self.truckID = truckID
        self.return_time = None   
    def __str__(self):
        return (f"Truck ID: {self.truckID}, "
                f"Current Address: {self.address}, "
                f"Total Miles Driven: {self.miles:.2f}, "
                f"Total Time: {self.time}, "
                f"Packages: {', '.join(str(package) for package in self.packages)}")
    

#lookup matching packageID in parsedPackages with passed in parameter ID. time complexity = O(N). space complexity = O(1)
def lookUp(packageID):
    for package in parsedPackages:
        if package.id == packageID:
            return package
    return None

def genetic_algorithm(truck):
    population = [random.sample(truck.packages, len(truck.packages)) for _ in range(POPULATION_SIZE)]
    for generation in range(GENERATIONS):
        #Assign total distance (fitness) of route
        fitness_scores = [(route, calculate_route_distance(route, truck.address)) for route in population]
        #sort by fitness (lower distance is better)
        fitness_scores.sort(key=lambda x: x[1])
        if fitness_scores[0][1] == 0:
            break
        # selectism - top N routes survive (elitism)
        survivors = [route for route, distance in fitness_scores[:POPULATION_SIZE // 2]]
        #copulate new population from survivors
        population = crossover_and_mutate(survivors)
    best_route = fitness_scores[0][0]
    return best_route

def calculate_route_distance(route, starting_address):
    #Calculate the total distance for a given route.
    total_distance = 0
    current_address = starting_address
    for packageID in route:
        package = lookUp(packageID)
        if package:
            total_distance += distanceData[current_address][package.address]
            current_address = package.address
    # Return to hub
    hub = addressDict["4001 South 700 East"]
    total_distance += distanceData[current_address][hub]
    return total_distance

def crossover_and_mutate(survivors):
    """Generate new population with crossover and mutation."""
    new_population = []
    
    # Create offspring
    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.sample(survivors, 2)
        cut = random.randint(0, len(parent1))
        #inheritance
        child = parent1[:cut] + [p for p in parent2 if p not in parent1[:cut]]
        # Mutation (randomly swap two packages)
        if random.random() < MUTATION_RATE:
            i, j = random.sample(range(len(child)), 2)
            child[i], child[j] = child[j], child[i]
        new_population.append(child)
    return new_population


def deliver(truck):
    truck.departure_time = truck.time
    optimized_route = genetic_algorithm(truck)
    # Deliver the packages in the optimized route
    for packageID in optimized_route:
        package = lookUp(packageID)
        if package:
            nextDistance = distanceData[truck.address][package.address]
            truck.miles += round(nextDistance, 1)
            truck.time += datetime.timedelta(minutes=(nextDistance / 0.3)) 
            truck.address = package.address  
            package.time_delivered = truck.time  
            package.truckID = truck.truckID 
            print(f"Truck {truck.truckID} delivered package {package.id} at {truck.time}")
    # Return to hub
    hub = addressDict["4001 South 700 East"]
    distance_to_hub = distanceData[truck.address][hub]
    truck.miles += round(distance_to_hub, 1)
    truck.time += datetime.timedelta(minutes=(distance_to_hub / 0.3)) 
    truck.address = hub
    truck.miles = float(f"{truck.miles:.1f}")
    truck.return_time = truck.time


parsedPackages = []

# hash table
hashTable = HashTable()

#distance array , initialized
distanceData = []
    
#dictionary initilized 
addressDict = {}

#Parse csv file then add all row to the initialized dictionary as key-val pairs. Time complexity O(N)
def loadAddresses():
    with open('WGUPS_Addresses.csv',  encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            index = int(row[0]) #col1
            address = row[2] #col2
            addressDict[address] = index 

loadAddresses()
#print(addressDict) 

#Parse every row from the file, append to initialized data structure. Time complexity O(N)
def load_package_data(hashTable):
    try:
        with open('WGUPS_Package.csv', encoding='utf-8-sig') as csvfile: 
            package_reader = csv.reader(csvfile, delimiter=',')
            
            #for every row, read columns as package properties then insert them as a new package object
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
                new_package = Package(id, address_index, city, state, zip_code, deliveryTime, weight,
                                      special_notes)

                hashTable.insert(id ,new_package)
                parsedPackages.append(new_package)
    except Exception as e:
        print(f"Error parsing packages: {e}")

load_package_data(hashTable)

#Parse csv rows, append them to the array. time complexity O(N), space complexity O(N) where n is the exponential number of rows
def read_distance_data():
    with open('distance_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # convert row to a list of floats
            distanceData.append([float(cell) if cell else 0.0 for cell in row])

    return distanceData

distance_matrix = read_distance_data()

packageKey1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

#loop through every item in list then loop through parsedPackages, check if keys match. add to truck1packages list. time complexity = O(n), space complexity = O(N)
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

truck3 = Truck(truck3Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=11, minutes=0)  , 3)

#print each row in arr. time-space complexity: O(N)
#for a in distanceData:
#    print(a)

def run():
    deliver(truck1)
    deliver(truck2)
    deliver(truck3)

#interface
def interface():
    print(f"\nTruck 1 departed at: {truck1.departure_time} and returned at: {truck1.return_time}")
    print(f"Truck 2 departed at: {truck2.departure_time} and returned at: {truck2.return_time}")
    print(f"Truck 3 departed at: {truck3.departure_time} and returned at: {truck3.return_time}")
    print("")

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
        
        try:
            selectedNum = int(input())
        except ValueError:
            print("Invalid input. Please enter a number between 1 - 3.")
            continue 

        if selectedNum == 1:
            packageId = input('Enter a Package ID (1-40): ')
            while True:
                timeStamp = input('Enter a time in HH:MM format: ')
                try:
                    (h, m) = map(int, timeStamp.split(':'))
                    if h < 8 or h > 13 or m < 0 or m > 59:
                        print("Invalid time. Please enter a time HH:MM format.")
                        continue
                    timeStamp = datetime.timedelta(hours=h, minutes=m)
                    break 
                except (ValueError, IndexError):
                    print("Invalid format. Please enter a valid time in HH:MM format.")

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
            
            print('Time delivered: ', tempStorage.time_delivered)
            print('Departure time', initTime)

            if timeStamp <= initTime:
                mg = "at hub"
            elif initTime < timeStamp < tempStorage.time_delivered:
                mg =  "en route"
            elif timeStamp >= tempStorage.time_delivered:
                mg =  "delivered"

            address = next(key for key, value in addressDict.items() if value == tempStorage.address)
            print(f"\nTimestamp: {timeStamp} \nPackageID: {tempStorage.id} \nStatus: {mg} \nDeliver at: {tempStorage.time_delivered} \nDeliver to: {address} \nSpecial Notes: {tempStorage.notes} \nTruck Number: {tempStorage.truckID}")

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

#main
if __name__ == "__main__":
    run()
    interface()

    
