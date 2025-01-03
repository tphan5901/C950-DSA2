C950 WGUPS Package Delivery System
A. Identify a named self-adjusting algorithm (e.g., nearest neighbor algorithm, greedy algorithm) that could be used in your program to deliver the packages. 
GA will be used to deliver the packages.
 B. Identify a self-adjusting data structure, such as a hash table, that could be used with the algorithm identified in part A to store the package data. 
A Dictionary can be used in order to store the addresses.
1. Explain how your data structure accounts for the relationship between the data components you are storing.
A Dictionary stores data as key-value pair. With dictionaries, we can access and update the addresses in O(1) time if we know it's value. The relationship between the dictionary and other data components is important for mapping truckIDs to their corresponding routes, enabling quick lookups. Dictionaries can also easily add, update, or remove entries as data changes. If a new package is added, we can update the dictionary without restructuring the entire dataset.
C. Write an overview of your program in which you do the following:
1. Explain the algorithm’s logic using pseudocode.
define getdistance(truckaddress, packageaddress):
        distance = distanceData[truckaddress][packageaddress]
 
addressdict= {}
distanceData = []
POPULATION_SIZE: 100 
MUTATION_RATE: 0.01
GENERATIONS: 100

define totaldistance(route, truck):
      totaldistance = 0
      currentAddress = truck.address
    FOR each package_id in route:
           if package exists:
            totaldistance += getdistance(currentAddress, package.address)
            currentAddress = package.address
    totaldistance += getdistance(currentAddress, addressDict["At the hub"])
    return totaldistance

define population(truckpackages):
    population = empty list
    for i from 1 - POPULATION_SIZE:
        route = copy truckpackages
        random shuffle route
        population.append(route)
    return population

define inheritance(parent1, parent2):
    size = len(parent1)
    child = list of None values of size
    start, end = random indices in the range of size (2)
    child[start:end] = parent1[start:end]
    SET p2 = 0
    for i FROM 0 of size:
        if child[i] is empty:
            while parent2[p2] is in child:
                p2_pointer += 1
            child[i] = parent2[p2]
    return child

define mutation(route):
    if random value < mutation_rate:
         i, j = in the range of route
        swap route[i] with route[j]
    return route

define selection(population, truck):
    sort population by calculatetotal()
    return top[:50] of sort population

define bestroute(truck):
    set population = populate(truck.packages)
    for generation from 1 to GENERATIONS:
        selected = selection(population, truck)
        nextpopulation = []
        for i FROM 1 TO POPULATION_SIZE:
            parent1, parent2 = random.(selected, for i in range (2))
            child = inherit(parent1, parent2)
            child = mutate(child)
            nextpopulation.append(child)
        population = nextpopulation
    route = route with min(population)
    return route

getdistance() retrieves the edge weight between two addresses (truck's current location & package's location) from a distance matrix. population size, mutation_rate, generations are parameters to configure the algorithm. Totaldistance method calculates the total distance for a given route. It initializes totaldistance to zero and starts at the truck's initial address. Population function initializes the population of routes by generating random routes. It creates an empty list for the population. For each individual in the population, it makes a copy of the truck's packages and shuffles them randomly to create a new route. Each route is added to the population list. inheritance method creates a child route by combining routes from two parents. It creates a child list and randomly selects two points to copy from parent1. For each empty spot in the child route, it adds a non-duplicate package from parent2. Mutation method introduces random changes to a route to maintain diversity. If a randomly generated number is less than the mutation rate, it selects two random indices in the route and swaps the packages at those positions. Selection method sorts the population based on the objective function (total distance). It retains the top 50% of routes. The main function runs to find the best delivery route. It initializes the population with random routes based on the truck's packages. For each generation, it selects the best routes, creates a new population through inheritance and mutation, and repeats the process. After all generations are processed, it finds the route with the minimum total distance.

2.  Describe the programming environment you will use to create the Python application, including both the software and hardware you will use. 
Software: Windows 11 OS, VSCode IDE , IDE Terminal, Tabulate python package, Colorama package. Python version 3.8
Hardware: Intel i5 10th gen CPU 2.9-3.6ghz, 12GB DDR4 Ram, M.2 SSD.
3. Evaluate the space-time complexity of each major segment of the program and the entire program using big-O notation. 
- Address Dictionary has a time-space complexity of O(1). Nearest neighbor has a time complexity of O(N^3) , creating the deque requires reading package data from the list. There is also a while loop with an inner loop within deliver(). Space complexity is O(N), since one data structure is utilized. readAddresses() , readDistances() , readPackages() has a time complexity of O(n) which is dependant on the size of the csv files. Interface() has a complexity of O(n) as it loops the package list in order to retrieve the package so the program can display the information. Overall the program has a space-time complexity of O(n^2).
4. Explain the capability of your solution to scale and adapt to a growing number of packages. 
The program currently relies on manually loading the packages instead of automatically handling them. If there were more packages parsed , they would not be added. Some packages have special conditions that isn't implemented yet in the system.
5. Discuss why the software design would be efficient and easy to maintain.
The code is modular, each function handles a specific part of the logic, such as loadAddresses(), loadPackages(). This separation of concerns makes it easier to maintain individual pieces without affecting the entire system. The program is straightforward to use with an implementation of terminal interface. Calculations are performed in the background and stored within class objects. Useful functions are implemented, that are accessible through dot operators. It maintainable , using basic programming principles , there are comments throughout the program explaining the code structure. Print statements on initialized memory structures are performed to verify data integrity.
 6. Describe both the strengths and weaknesses of the self-adjusting data structure (e.g., the hash table). 
Dictionaries provide a more organized way to manage key-value pairs. However, they can encounter issues with hash collisions as more addresses are added, leading to slow lookups. When multiple values hash to the same bucket, it results in decreased performance.
D.  Provide an intuitive interface for the user to view the delivery status (including the delivery time) of any package at any time and the total mileage traveled by all trucks.  
define interface():
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
            p4ckages = []

            for Package in parsedPackages:
                p4ckages.append(Package)
            status = ""
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
if __name__ == "__main__":
    interface()

1.  Provide screenshots to show the status of all packages loaded onto each truck at a time between 8:35 a.m. and 9:25 a.m. 
 


2.  Provide screenshots to show the status of all packages loaded onto each truck at a time between 9:35 a.m. and 10:25 a.m. 
 


3.  Provide screenshots to show the status of all packages loaded onto each truck at a time between 12:03 p.m. and 1:12 p.m. 
 



E.  Provide screenshots showing successful completion of the code that includes the total mileage traveled by all trucks. 
 



F.  Justify the package delivery algorithm used in the solution as written in the original program by doing the following: 
1.  Describe two or more strengths of the algorithm used in the solution. 
GA can evaluate multiple routes which increases the likelihood of finding optimal solutions. This is useful for package delivery where the number of routes can grow exponentially. GA is able to adapt over time which makes the algorithm adaptable against changes in input data, such as variations in the number of packages. If a new package is added or an address needs to be altered, the algorithm can quickly re-evaluate and optimize the routes without requiring a rewrite of the system. GA also uses concepts like crossover to introduce diversity into the population. This increases the chances of escaping local optima and finding more optimal routes.
2.  Verify that the algorithm used in the solution meets all requirements in the scenario. 
Special conditions: The program addresses specific conditions, such as handling package#9, which requires a different delivery address if delivered after 10:20 AM. The code checks the time (if package.id == '9' and truck.time > DeliveryTime) and dynamically adjusts the delivery address while delivering packages under 140miles.
3.  Identify two other named algorithms that are different from the algorithm implemented in the solution and would meet all requirements in the scenario. 
Prim's Algorithm and Nearest Neighbor. 
a.  Describe how both algorithms identified in part F3 are different from nearest neighbor used in the solution. 
- Nearest Neighbor starts at a given vertex and iteratively visits the nearest unvisited vertex until all vertices have been visited, then returns to the starting vertex.The Algorithm makes locally optimal choices at each step to finding a global optimum. In contrast, genetic looks at multiple potential solutions simultaneously and can escape local optima through concepts like crossover and mutation. While the Nearest Neighbor is faster and simpler to implement, it can produce suboptimal solutions, especially for larger datasets. While GA tends to produce better solutions over time, but requires more computational resource.
-Prim's algorithm constructs a Minimum Spanning Tree for a weighted graph by starting from an random vertex then adding the minimum weight edge that connects a vertex within a tree to a vertex outside it. It is generally used in scenarios for problems like network design. Prim's Algorithm runs in O(E log V) time, where E is the number of edges and V is the number of vertices, making it efficient for dense graphs. GA does require more significant amount of computational time depending on the population size and number of generations.
H.  Describe what you would do differently, other than the two algorithms identified in part F3, if you did this project again, including details of the modifications that would be made. 
A control structure would likely have been implemented to determine the appropriate truck assignment for packages based on delivery deadlines and special notes. This conditional logic allows the program to scale as additional packages are added and automates the process of handling packages without manually adding them onto the trucks. This logic would likely be implemented within the method which parses the csv file.
1. Identify two other data structures that could meet the same requirements in the scenario  
A doubly linked list and An Adjacency matrix 
a.  Describe how each data structure identified in H1 is different from the data structure used in the solution. 
Doubly linked list is a data structure where each node contains a reference to both next and previous node. This allows traversal in both directions. Each node stores data with two pointers, one pointing to the next node another to the previous node.
An adjacency matrix requires O(V2)space, where V is the number of vertices. An adjacency matrix works well for weighted graphs, where edges have associated weights. The matrix can store weights in cells, making edge lookups fast. O(1) Time complexity. 
I. References:
