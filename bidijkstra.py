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

# Time complexity: O(E log V), where E is edges and V is vertices. Space complexity: O(N).
def deliver(truck):
    truck.departure_time = truck.time
    dequeue = deque(truck.packages) 
    DeliveryTime = datetime.timedelta(hours=10, minutes=20)
    distances = {address: float('inf') for address in addressDict.values()}
    distances[truck.address] = 0
    priorityQueue = [(0, truck.address)]  
    #while packages enqueue
    while dequeue:
        visited = set()
        while priorityQueue:
            currentDistance, currentAddress = heapq.heappop(priorityQueue)
            if currentAddress in visited:
                continue
            visited.add(currentAddress)
            for packageID in dequeue:
                package = lookUp(packageID)
                if package:
                    if package.id == '9' and truck.time > DeliveryTime:
                        package.address = addressDict["410 S State St"]
                    # find the distance to each package
                    nextDistance = distanceData[currentAddress][package.address]
                    newDistance = currentDistance + nextDistance
                    if newDistance < distances[package.address]:
                        distances[package.address] = newDistance
                        heapq.heappush(priorityQueue, (newDistance, package.address))
        #deliver the nearest package
        nearestDistance = float('inf')
        nextPackage = None
        for packageID in dequeue:
            package = lookUp(packageID)
            if package:
                distance_to_package = distances[package.address]
                if distance_to_package < nearestDistance:
                    nearestDistance = distance_to_package
                    nextPackage = package
        if nextPackage:
            truck.miles += round(nearestDistance, 1)  
            truck.time += datetime.timedelta(minutes=(nearestDistance / 0.3))  
           #print(f"Truck {truck.truckID} delivered package {nextPackage.id} at {truck.time}")
            truck.address = nextPackage.address  
            nextPackage.time_delivered = truck.time  
            nextPackage.truckID = truck.truckID 
            #remove package after delivery
            dequeue.remove(nextPackage.id)  
            distances = {address: float('inf') for address in addressDict.values()}
            distances[truck.address] = 0
            priorityQueue = [(0, truck.address)]
    # return to hub
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

#open csv file and add every row from the file to the initialized data structure. Time complexity O(N)
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

#open csv file, parse every row in the file, append them to the array. time complexity O(N), space complexity O(N) where n is the exponential number of rows
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

    
