#truck class object
class Truck:
    def __init__(self, packages, address, miles, time, truckID):
        self.packages = packages
        self.address = address
        self.miles = miles
        self.time = time
        self.truckID = truckID

    def __str__(self):
        #string representation of the Truck object
        return (f"Truck ID: {self.truckID}, "
                f"Current Address: {self.address}, "
                f"Total Miles Driven: {self.miles:.2f}, "
                f"Total Time: {self.time}, "
                f"Packages: {', '.join(str(package) for package in self.packages)}")
        
    #load a package onto the truck
    def load_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            self.loaded_weight += package.weight
            package.assign_to_truck(self.truck_id) 
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
