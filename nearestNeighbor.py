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
import heapq

#returns distance between two weights. time complexity = O(1)
def heuristic(start, end):
    return abs(start - end)

#returns list of neighbor nodes. time complexity = O(1)
def get_neighbors(graph, node):
    return graph[node]

#lookup matching packageID in parsedPackages with passed in parameter ID. time complexity = O(N). space complexity = O(1)
def lookUp(package_id):
    return parsedPackages.get(package_id, None)

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
def deliver(truck):
    # create list of packages 
    package_list = list(truck.packages)
    currentAddress = truck.address
    visited_packages = []

    while package_list:
        nextPackage = None
        nextDistance = float('inf')
        # find nearest package from the current address
        for pkg_id in package_list:
            package = lookUp(pkg_id)
            if package:
                distance = get_distance(currentAddress, package.address)
                if distance < nextDistance:
                    nextDistance = distance
                    nextPackage = package
        if nextPackage:
            if nextPackage.id == '9' and truck.time > datetime.timedelta(hours=10, minutes=20):
                nextPackage.address = addressDict["410 S State St"]
            truck.miles += nextDistance
            truck.time += datetime.timedelta(minutes=(nextDistance / (0.3)))
            print(f"Truck {truck.truckID} delivered package {nextPackage.id} at {truck.time}")
            visited_packages.append(nextPackage.id)
            package_list.remove(nextPackage.id)
            currentAddress = nextPackage.address 
            nextPackage.time_delivered = truck.time
            nextPackage.truckID = truck.truckID
    # Return to hub
    hub = addressDict["4001 South 700 East"]
    distance_to_hub = get_distance(currentAddress, hub)
    truck.miles += distance_to_hub
    truck.time += datetime.timedelta(minutes=(distance_to_hub / (0.3)))
    truck.miles = float(f"{truck.miles:.1f}")



#init packages list
parsedPackages = {}

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


# open csv file and add every row from the file to the initialized data structure. time complexity O(N) - space complexity O(N) where n is the number of rows
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

                # store package in the dictionary with ID as the key
                parsedPackages[id] = new_package

        return parsedPackages  
    except Exception as e:
        print(f"Error parsing packages: {e}")
        return {}

parsedPackages = load_package_data()

# open CSV file, parse every row in the file, append them to the array. time-space complexity O(N) where n is the number of rows
def read_distance_data():
    with open('distance_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            distanceData.append(row)

    return distanceData

distanceData = read_distance_data()


truck1Packages = [str(a) for a in [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]]
truck1 = Truck(truck1Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=8, minutes=0), 1)

truck2Packages = [str(b) for b in [3, 6, 18, 22, 23, 25, 27, 28, 32, 33, 35, 36, 38]]
truck2 = Truck(truck2Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=9, minutes=10), 2)

truck3Packages = [str(c) for c in [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 24, 26, 39]]
truck3 = Truck(truck3Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=10, minutes=0), 3)

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
            for Package in parsedPackages.values():
                msg = ''
                truckDepartureTime = {
                    1: datetime.timedelta(hours=8, minutes=0),
                    2: datetime.timedelta(hours=9, minutes=5),
                    3: datetime.timedelta(hours=10, minutes=0)
                }

                address = Package.address

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


    
