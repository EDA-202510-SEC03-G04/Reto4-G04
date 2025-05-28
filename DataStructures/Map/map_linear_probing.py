class Map:
    
    def __init__(self, capacity=10, loadfactor=0.5):
        self.capacity = max(1, capacity)
        self.loadfactor = loadfactor
        self.size_count = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        index = self._hash(key)
        start_index = index  
        while self.keys[index] is not None:
            if self.keys[index] == key:
                self.values[index] = value
                return
            index = (index + 1) % self.capacity
            if index == start_index:
                self._rehash()
                return self.put(key, value)

        self.keys[index] = key
        self.values[index] = value
        self.size_count += 1

        # Rehash preventivo por si supera el factor de carga
        if self.size_count / self.capacity > self.loadfactor:
            self._rehash()

    def _rehash(self):
        old_keys = self.keys
        old_values = self.values
        self.capacity *= 2
        self.size_count = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity

        for i in range(len(old_keys)):
            if old_keys[i] is not None:
                self.put(old_keys[i], old_values[i])

    def get(self, key):
        index = self._hash(key)
        start_index = index
        while self.keys[index] is not None:
            if self.keys[index] == key:
                return {"key": self.keys[index], "value": self.values[index]}
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return None

    def contains(self, key):
        return self.get(key) is not None

    def remove(self, key):
        index = self._hash(key)
        start_index = index
        while self.keys[index] is not None:
            if self.keys[index] == key:
                self.keys[index] = None
                self.values[index] = None
                self.size_count -= 1
                return True
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return False

    def size(self):
        return self.size_count

    def key_set(self):
        return [k for k in self.keys if k is not None]

    def value_set(self):
        return [self.values[i] for i in range(self.capacity) if self.keys[i] is not None]



def newMap(numelements=10, factorcarga=0.5):
    return Map(numelements, factorcarga)

def put(map_obj, key, value):
    return map_obj.put(key, value)

def get(map_obj, key):
    return map_obj.get(key)

def contains(map_obj, key):
    return map_obj.contains(key)

def remove(map_obj, key):
    return map_obj.remove(key)

def size(map_obj):
    return map_obj.size()

def key_set(map_obj):
    return map_obj.key_set()

def value_set(map_obj):
    return map_obj.value_set()

