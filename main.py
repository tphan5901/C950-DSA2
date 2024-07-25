#studentID: O11746951
#Thinh Phan
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

#create truck class object
class Truck:
    def __init__(self, packages, address, miles, time, truckID):
        self.packages = packages
        self.address = address
        self.miles = miles
        self.time = time
        self.truckID = truckID

parsedPackages = []

# nearest neighbor algorithm. O(N^3)
def nearestNeighbor(truck):
    #for every package on truck, initialize variables
    for i in truck.packages:
        shortestPath = float('inf') 

        #Every ID on the truck, return the package object from the list if id matches
        for j in truck.packages:
            for Package in parsedPackages:
                if Package.id == j:
                    currentPackage = Package

            #Assign distance between truck address and the package destination
            distance = distanceData[addressDict[truck.address]][addressDict[currentPackage.address]]

            #recursively check whether current distance is less than initialized path and if package is not delivered yet. 
            while distance < shortestPath and currentPackage.time_delivered is None:
                nextPackage = currentPackage
                shortestPath = distance

        #current package with becomes next package to be delivered
        package = nextPackage

        #increment mileage and time using 18mph
        distance = distanceData[addressDict[truck.address]][addressDict[package.address]]
        truck.miles += distance
        truck.time += datetime.timedelta(minutes=(distance / (18 * (1 / 60))))

#       print(f"Truck {truck.truckID} delivered package {package.id} time: {truck.time}")
        truck.address = package.address
        package.time_delivered = truck.time
        package.truckID = truck.truckID

    #return to the hub
    distance = distanceData[addressDict[truck.address]][addressDict["4001 South 700 East"]]
    truck.miles += distance

 #   print(f"Truck {truck.truckID} delivered package {package.id} time: {truck.time}")
  
# hash table
hashTable = HashTable()

#distance array , initialized
distanceData = []
    
#dictionary initilized 
addressDict = {}

#open csv file then add all row to the initialized dictionary as key-val pairs. col1 is index, col3 is value. O(N)
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
        #enconded to utf-8 to avoid formatt issues
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
              
                new_package = Package(id, address, city, state, zip_code, deliveryTime, weight,
                                      special_notes)

                hashTable.insert(id ,new_package)
                parsedPackages.append(new_package)
    except Exception as e:
        print(f"Error parsing packages: {e}")

load_package_data(hashTable)

#open csv file and add every row in the file to the initialized array. O(N)
def read_distance_data():
    with open('distance_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # convert row to a list of floats
            distanceData.append([float(cell) if cell else 0.0 for cell in row])

    return distanceData


#Iterate through array and check for zeroes. complete matrix by adding zeroes equal to length of the column for the perpendicular row. O(N^2)
def inflectionMatrix(matrix):
    size = len(matrix)
    # Create an empty matrix with the same dimensions
    reflectedMatrix = [[0] * size for i in range(size)]

    # Populate the reflected matrix
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
for a in distanceData:
    print(a)


packageKey1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

#loop through every item in list above then loop through parsedPackages and check if keys match, if they do then add to truck1packages list. O(n^2)
truck1Packages = []
for a in packageKey1:
    for Package in parsedPackages:
        if Package.id == str(a):  
            truck1Packages.append(Package.id)

#truck initialization packages/departure location/time , truckID
truck1 = Truck(truck1Packages, "4001 South 700 East", 0,  datetime.timedelta(hours=8, minutes=30), 1)

#truck2
packageKey2 = [3, 6, 18, 22, 23, 25, 27, 28, 32, 33, 35, 36, 38]

#same thing as above. O(n^2)
truck2Packages = []
for b in packageKey2:
    for Package in parsedPackages:
        if Package.id == str(b):
            truck2Packages.append(Package.id)

truck2 = Truck(truck2Packages, "4001 South 700 East", 0, datetime.timedelta(hours=9, minutes=15) , 2)

# truck3
packageKey3 = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 24, 26, 39]

#same as above. O(n^2)
truck3Packages = []
for c in packageKey3:
    for Package in parsedPackages:
        if Package.id == str(c): #parse as str
            truck3Packages.append(Package.id)

truck3 = Truck(truck3Packages, "4001 South 700 East", 0, datetime.timedelta(hours=10, minutes=20)  , 3)


#based on package's truck ID, assign a time when the truck leaves hub and based on timestamp user enters and based on condition, return a msg value. O(1)
def returnStatus(package, timeStamp):
    truckDepartureTime = {
        1: datetime.timedelta(hours=8, minutes=0),
        2: datetime.timedelta(hours=9, minutes=15),
        3: datetime.timedelta(hours=10, minutes=20)
    }
    
    if package.truckID == 1:
        initTime = truckDepartureTime[1]
    elif package.truckID == 2:
        initTime = truckDepartureTime[2]
    elif package.truckID == 3:
        initTime = truckDepartureTime[3]
        
    if timeStamp <= initTime:
        return "at hub"
    elif initTime < timeStamp < package.time_delivered:
        return "en route"
    elif timeStamp >= package.time_delivered:
        return "delivered"

nearestNeighbor(truck1)
nearestNeighbor(truck2)
nearestNeighbor(truck3)

while True:
    #interface
    try:
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

        #if user selects #, conditional
        if selectedNum == 1:
                packageId = input('Enter a Package ID (1-40):')

                timeStamp = input('Enter a time using HH:MM format: ')
                #splices at : and removes semicolon
                (h, m) = timeStamp.split(':')

                timeStamp = datetime.timedelta(hours=int(h), minutes=int(m))
                
                returnPackage = hashTable.search(packageId)
             #   print(type(returnPackage))
             #   print(returnPackage.id)

                #if package obj in list matches the input, we return the package object. O(1)
                for Package in parsedPackages:
                    if Package.id == packageId:
                        tempStorage = Package
                
                #assign whats returned from the function 
                status = returnStatus(tempStorage, timeStamp)

                print(f"\nTimestamp: {timeStamp} \nPackageID: {tempStorage.id} \nStatus: {status} \nDelivery Time: {tempStorage.time_delivered} \nDeliver to: {tempStorage.address} \nSpecial Notes: {tempStorage.notes} \nTruck Number: {tempStorage.truckID}")

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
                1: datetime.timedelta(hours=8, minutes=30),
                2: datetime.timedelta(hours=9, minutes=15),
                3: datetime.timedelta(hours=10, minutes=20)
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

    except Exception as e:
        print(e)