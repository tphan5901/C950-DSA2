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
        
