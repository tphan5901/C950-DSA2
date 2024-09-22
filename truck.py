#truck class object
class Truck:
    # Truck status
    STATUS_IDLE = 'Idle'
    STATUS_EN_ROUTE = 'En Route'
    STATUS_RETURNED = 'Returned'
    STATUS_MAINTENANCE = 'In Maintenance'

    def __init__(self, packages, address, miles, time, truckID):
        self.packages = packages
        self.address = address
        self.miles = miles
        self.time = time
        self.truckID = truckID

    #load a package onto the truck
    def load_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            self.loaded_weight += package.weight
            package.assign_to_truck(self.truck_id)  # update package status 
        else:
            raise ValueError("Truck capacity reached, cannot load more packages.")
    
    #unload a package
    def unload_package(self, package):
        if package in self.packages:
            self.packages.remove(package)
            self.loaded_weight -= package.weight
            package.update_status('Delivered')  # Mark package as delivered 
        else:
            raise ValueError(f"Package {package.id} not found on truck.")
