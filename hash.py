#HashTable class. 
class HashTable:
    def __init__(self, initial_capacity=41):
        # initialize the table with predefined capacity
        self.initial_capacity = initial_capacity
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    #function to add new item to table. O(1)
    def insert(self, key, item):
        #first hashes the key with length of table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # insert key/value pair as item to table
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    #search for an item with matching key in hash table. hashes the parameter key and checks if the hashed key matches with existing keys in the table. O(1)
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket 
        for kv in bucket_list:
            #return (key_value)
            if kv[1] == key:
                return kv[0]   
            else:
                return None
