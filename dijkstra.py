#studentID: O11746951
#Thinh Phan
import csv
import datetime
from hash import *
from package import *
from truck import *
from collections import deque
from tabulate import tabulate
import heapq

#returns distance between two weights. time complexity = O(N)
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

#The time complexity is 𝑂(𝑉2) * 𝑂(𝑉2)  where V is the number of vertices. With a priority queue, the complexity can be improved to 𝑂((𝑉+𝐸)log𝑉)O((V+E)logV), where 𝐸E is the number of edges.
def dijkstra(truck_address, packages):
    distances = {address: float('inf') for address in addressDict.values()}
    distances[truck_address] = 0
    #Queue to keep track of distances
    priority_queue = [(0, truck_address)]
    parent = {address: None for address in addressDict.values()}

    while priority_queue:
        current_distance, current_address = heapq.heappop(priority_queue)
        # If the current node has already been visited skip
        if current_distance > distances[current_address]:
            continue
        for package in packages:
            distance_to_next = distanceData[current_address][package.address]
            new_distance = current_distance + distance_to_next
            if new_distance < distances[package.address]:
                distances[package.address] = new_distance
                heapq.heappush(priority_queue, (new_distance, package.address))
                parent[package.address] = current_address
    return distances, parent

#time complexity is 𝑂(𝑁)⋅(𝑂(𝑁2)+𝑂(𝑁))=𝑂(𝑁3)O(N)⋅(O(N2)+O(N))=O(N3). Outer while loop and an inner loop, loop through list and add the packages. third loop creates the queue from truck packages
# space complexity = O(N) memory is used for DEqueue and shortestPaths, both of which are 𝑂(N).
def deliver(truck):
    package_queue = deque(truck.packages)
    DeliveryTime = datetime.timedelta(hours=10, minutes=20)

    while package_queue:
        shortest_paths, _ = dijkstra(truck.address, [lookUp(pid) for pid in package_queue])
        nearest_package = None
        nearest_distance = float('infinity')
        for package_id in package_queue:
            package = lookUp(package_id)
            if package:
                # Special case for package 9
                if package.id == '9' and truck.time > DeliveryTime:
                    package.address = addressDict["410 S State St"]
                distance_to_package = shortest_paths[package.address]
                if distance_to_package < nearest_distance:
                    nearest_distance = distance_to_package
                    nearest_package = package
        if nearest_package:
            # Move the truck to the nearest package's location and deliver it
            truck.miles += nearest_distance
            truck.time += datetime.timedelta(minutes=(nearest_distance / 0.3))
            print(f"Truck {truck.truckID} delivered package {nearest_package.id} at {truck.time}")
            truck.address = nearest_package.address
            nearest_package.time_delivered = truck.time
            nearest_package.truckID = truck.truckID
            package_queue.remove(nearest_package.id)
    #return to hub
    hub_address = addressDict["4001 South 700 East"]
    distance_to_hub = distanceData[truck.address][hub_address]
    truck.miles += distance_to_hub
    truck.time += datetime.timedelta(minutes=(distance_to_hub / 0.3))
    truck.address = hub_address

 
parsedPackages = []

# hash table
hashTable = HashTable()

#distance array , initialized
distanceData = []
    
#dictionary initilized 
addressDict = {}

#open csv file then add all row to the initialized dictionary as key-val pairs. time complexity O(N), space complexity O(N) where n is the exponential number of rows
def loadAddresses():
    with open('WGUPS_Addresses.csv',  encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            index = int(row[0]) #col1
            address = row[2] #col2
            addressDict[address] = index 

loadAddresses()
#print(addressDict) 

#open csv file and add every row from the file to the initialized data structure. time complexity O(N), space complexity O(N) where n is the exponential number of rows
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

#Loop array and check for zeroes. asert zeroes equal to length of the column for the perpendicular row. time complexity O(N^2), space complexity = 0(N)
def inflectionMatrix(matrix):
    size = len(matrix)
    reflectedMatrix = [[0] * size for i in range(size)]

    for i in range(size):
        for j in range(size):
            if i == j:
                reflectedMatrix[i][j] = 0
            elif i < j:
                reflectedMatrix[i][j] = matrix[i][j]
            else:
                reflectedMatrix[i][j] = matrix[j][i]

    return reflectedMatrix

distance_matrix = read_distance_data()
#reflected_distance_matrix = inflectionMatrix(distance_matrix)

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


            print(f"\nTimestamp: {timeStamp} \nPackageID: {tempStorage.id} \nStatus: {mg} \nDelivery Time: {tempStorage.time_delivered} \nDeliver to: {tempStorage.address} \nSpecial Notes: {tempStorage.notes} \nTruck Number: {tempStorage.truckID}")

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
                        
                table_data.append([Package.id, address, status, Package.deliveryTime, Package.truckID])

            print(tabulate(table_data, headers=["Package ID", "Address", "Status", "Delivery Deadline", "Truck ID"], tablefmt="pretty"))

        elif selectedNum == 3:
            print("Exiting program...")
            break

        else:
            print("Invalid command, please try again.")

#main executes what is called within scope
if __name__ == "__main__":
    run()
    interface()

    
