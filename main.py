#studentID: O11746951
import csv
import datetime
from hash import *

#package class object
class Package:
    def __init__(self, id, address, city, state, zip, deliveryTime, weight, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip 
        self.deliveryTime = deliveryTime
        self.weight = weight
        self.notes = notes
        self.time_delivered = None
        self.truckID = 0

    def __str__(self):
        return ("ID: %s, Address: %-20s, City: %s, State: %s, Zip: %s, "
                "Delivery Time: %s, Weight: %s, Notes: %s, "
                "Time Delivered: %s, Truck ID: %s") % (
            self.id, self.address, self.city, self.state, self.zip,
            self.deliveryTime, self.weight, self.notes, self.time_delivered, self.truckID
        )
        

#create truck class object
class Truck:
    def __init__(self, packages, address, miles, time, truckID):
        self.packages = packages
        self.address = address
        self.miles = miles
        self.time = time
        self.truckID = truckID


parsedPackages = []

#gives us diff between two locations. time complexity = O(N)
def heuristic(start, end):
    return abs(start - end)

#returns list of neighbor nodes. time complexity = O(1)
def get_neighbors(graph, node):
    return graph[node]

# time complexity = O(N^3), outer while loop and two inner loops. space complexity = O(N^2) memory is used for queue data structure and parsedpackages list
def deliver(truck):
    #while truck has packages , load queue 
    package_queue = deque(truck.packages)
    nextPackage = None
    time = datetime.timedelta(hours=10, minutes=20)

    while package_queue:
        for package_id in package_queue:
            for package in parsedPackages:
                if package.id == package_id:
                    #fetch packages, store distance between truck and next address
                    distance = distanceData[truck.address][package.address]
                    nextPackage = package

        if nextPackage:
            distance = distanceData[truck.address][nextPackage.address]
            truck.miles += distance
            truck.time += datetime.timedelta(minutes=(distance / (0.3)))
            print(f"Truck {truck.truckID} delivered package {nextPackage.id} at {truck.time}")
            truck.address = nextPackage.address
            nextPackage.time_delivered = truck.time
            nextPackage.truckID = truck.truckID
            #after delivered , remove package
            package_queue.remove(nextPackage.id)

  
# hash table
hashTable = HashTable()

#distance array , initialized
distanceData = []
    
#dictionary initilized 
addressDict = {}

#open csv file then add all row to the initialized dictionary as key-val pairs. 
def loadAddresses():
    with open('WGUPS_Addresses.csv',  encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            index = int(row[0]) #col1
            address = row[2] #col2
            addressDict[address] = index 

loadAddresses()
#print(addressDict) 

#open csv file and add every row from the file to the initialized data structure. O(N)
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
              
                # get the index of the address
                address_index = addressDict[address]
                new_package = Package(id, address_index, city, state, zip_code, deliveryTime, weight,
                                      special_notes)

                hashTable.insert(id ,new_package)
                parsedPackages.append(new_package)
    except Exception as e:
        print(f"Error parsing packages: {e}")

load_package_data(hashTable)

#open csv file and add every row in the file to the initialized array. O(N). N is row of data
def read_distance_data():
    with open('distance_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # convert row to a list of floats
            distanceData.append([float(cell) if cell else 0.0 for cell in row])

    return distanceData


#Loop array and check for zeroes. asert zeroes equal to length of the column for the perpendicular row. O(N^2)
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
reflected_distance_matrix = inflectionMatrix(distance_matrix)

#print each row in arr O(N)
#for a in distanceData:
#    print(a)

packageKey1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

#loop through every item in list above then loop through parsedPackages and check if keys match, if they do then add to truck1packages list. time complexity: O(n^2)
truck1Packages = []
for a in packageKey1:
    for Package in parsedPackages:
        if Package.id == str(a):  
            truck1Packages.append(Package.id)

#truck initialization packages/departure location/time , truckID
truck1 = Truck(truck1Packages, addressDict["4001 South 700 East"], 0,  datetime.timedelta(hours=8, minutes=0), 1)

#truck2
packageKey2 = [3, 6, 18, 22, 23, 25, 27, 28, 32, 33, 35, 36, 38]

#same thing as above. O(n^2)
truck2Packages = []
for b in packageKey2:
    for Package in parsedPackages:
        if Package.id == str(b):
            truck2Packages.append(Package.id)

truck2 = Truck(truck2Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=9, minutes=10) , 2)

# truck3
packageKey3 = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 24, 26, 39]

#same as above. O(n^2)
truck3Packages = []
for c in packageKey3:
    for Package in parsedPackages:
        if Package.id == str(c): #parse as str 
            truck3Packages.append(Package.id)

truck3 = Truck(truck3Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=11, minutes=0)  , 3)

deliver(truck1)
deliver(truck2)
deliver(truck3)

#interface
def interface():
    print('WGUPS Package delivery service')
    print("Route commpleted in: ", truck1.miles + truck2.miles + truck3.miles, "miles")
    print("Truck1 miles", truck1.miles)
    print("Truck2 miles", truck2.miles)
    print("Truck3 miles", truck3.miles)
    print("Enter a command (1-3):")
    print("1. Display specific package")
    print("2. Display all package status")
    print("3. Exit")
    selectedNum = int(input())

    while selectedNum != 3:

                #if user selects #, conditional
                if selectedNum == 1:
                        packageId = input('Enter a Package ID (1-40):')

                        timeStamp = input('Enter a time using HH:MM format: ')
                        (h, m) = timeStamp.split(':')

                        timeStamp = datetime.timedelta(hours=int(h), minutes=int(m))
                        
                    #    returnPackage = hashTable.search(packageId)
                    #   print(type(returnPackage))
                    #   print(returnPackage.id)

                        #if package obj in list matches the input, we return the package object. O(1)
                        for Package in parsedPackages:
                            if Package.id == packageId:
                                tempStorage = Package
                        
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
                    print("Status of packages at", timeStamp)

                    #fetch all packages stored from the parsedPackage list and insert them  into p4kages list, O(N) 
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
                        3: datetime.timedelta(hours=11, minutes=0)
                        }
            
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
                    
                        print(f"PackageID: {Package.id} \n\nStatus: {status} \n\nAddress: {Package.address} \n\nDeadline: {Package.deliveryTime} \n\n")

                elif selectedNum == 3:
                    exit()

                print("Enter a command (1-3):")
                print("1. Display specific package")
                print("2. Display all package status")
                print("3. Exit")
                selectedNum = int(input())

#main
if __name__ == "__main__":
    interface()
