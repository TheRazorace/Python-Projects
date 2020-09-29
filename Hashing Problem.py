import random
import sys

##          Εφαρμογή Hashing
##          Αναλυτικά σχόλια για τον κώδικα στην αναφορά!

def presentation():
    print("Εφαρμογή Hashing")
    print("")

def is_prime(n):
    if n == 1:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def next_prime(num):
    if (not num & 1) and (num != 2):
        num += 1
    if is_prime(num):
        num += 2
    while True:
        if is_prime(num):
            break
        num += 2
    return num

            
class HashTable(object):

    def __init__(self):
        self.size = 1000
        self.value_array = []
        self.total_entries = 0
        self.max_cost = 0
        self.max_cost_card = []
        self.max_days = 0
        self.max_days_card = []
        self.collisions = 0
        print("Επιλέξτε τη σταθερά φόρτωσης (load factor), σε ποσοστό, της διαδικασίας (από 1 εώς 99)")
        print("Για παράδειγμα, η επιλογή 30 αντιστοιχει σε 30%, δηλαδή load factor = 0.3")
        self.load_factor = int(input("Επιλογή:" ))/100
        if self.load_factor<0.01 or self.load_factor>0.99:
            print("Δεν υπάρχει αυτή η επιλογή! Ξαναπροσπαθήστε...")
            sys.exit()
        for i in range(1000):
            self.value_array.append(None)
        print("")
        
    def __str__(self):
        output_lines = []
        for item in self.value_array:
            if item != None:
                output_lines.append("Πιστωτική: " + ('{}'*16).format(*item[0]) + " Αγορά: " + str(item[1]))

        return "\n".join(output_lines)
    
    def resize(self):
        new_value_array = []
        new_size = next_prime(2 * self.size)
        for i in range(new_size):
            new_value_array.append(None)
        for i in range(self.size):
            if self.value_array[i] != None:
                self.add_internal(self.value_array[i][0], self.value_array[i][1], new_value_array, new_size, self.max_cost, self.max_cost_card, self.max_days, self.max_days_card, self.collisions, True)
        self.value_array = new_value_array
        self.size = new_size
        
    def add(self, key, value):
        self.add_internal(key, value, self.value_array, self.size, self.max_cost, self.max_cost_card, self.max_days, self.collisions, self.max_days_card)
    
    def add_internal(self, key, value, value_array, size, max_cost, max_cost_card, max_days, max_days_card, collisions, during_resize = False):
        if value_array[self.hash1(key)] == None:
            value_array[self.hash1(key)] = key, value
        else:
            added = False
            attempt_count = 1
            while (not added):
                if self.get(key):
                    new_val = [0 for i in range(7)]
                    for i in range(7):
                            new_val[i] = value[i] + self.get(key)[i]
                    value_array[self.hash1(key)] = key, new_val
                    
                    if new_val[0] > self.max_cost:
                        self.max_cost = new_val[0]
                        self.max_cost_card = key
                        
                    day_sum = 0
                    for i in range(1,7):
                        day_sum = day_sum + value[i]
                    if day_sum > max_days:
                        self.max_days = day_sum
                        self.max_days_card = key

                    added = True

                else:
                    self.collisions = self.collisions + 1
                    newhash = (self.hash1(key) + attempt_count*self.hash2(key)) % size
                    if value_array[newhash] == None:
                        value_array[newhash] = key, value
                        added = True
                    else:
                        attempt_count += 1
        if not during_resize:
            self.total_entries += 1
            if self.total_entries/size > self.load_factor:
                self.collisions = 0
                self.resize()
    
    def get(self, key):
        got_value = self.value_array[self.hash1(key)]
        if got_value == None:
            return None
        retrieved_key, retrieved_value = got_value
        if retrieved_key != key:
            found = False
            attempt_count = 1
            while (not found and attempt_count < 100):
                newhash = (self.hash1(key) + attempt_count*self.hash2(key)) % self.size
                value_at_hash = self.value_array[newhash]
                if value_at_hash != None:
                    retrieved_key, retrieved_value = value_at_hash
                    if retrieved_key == key:
                        found = True
                    attempt_count += 1
                else:
                    attempt_count += 1
        return retrieved_value
    
    def hash1(self, key):
        return id(key) % self.size
    
    def hash2(self, key):
        hashval = (id(key) + 501) % self.size
        return hashval


def make_card(base_card):
    card = [base_card[i] for i in range(16)]
    replace_position = []*4
    letters = ["A", "B", "C", "D"]
    replace_position = random.sample(range(16), 4)
    for j in range(4):
        card[replace_position[j]] = letters[j]
    return card
                
def hash_table():
    random.seed(1053711)
    visits = 10000
    
    base_card = [random.randrange(10) for count in range(16)]
    value = [0 for i in range(7)]

    day_list = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο"]
    day_count = [0 for i in range(6)]
    
    ht = HashTable()    

    for i in range(visits):
        card = make_card(base_card)
        value = [0 for i in range(7)]
        cost = round(random.randrange(10, 100), 1)
        day = random.randrange(6)
        day_count[day] = day_count[day] + 1
        value[0] = cost
        value[day + 1] = 1
        ht.add(card, value)

    print("Τα δεδομένα αποθηκεύονται στο Hash Table...")
    print("Γίνονται υπολογισμοί...")
    print("")

    print("Η κάρτα με το μεγαλύτερο συνολικό ποσό πληρωμών είναι η", ('{}'*16).format(*ht.max_cost_card), " συνολικών αγορών ίσων με ", ht.max_cost,"€.")
    print("Η κάρτα με το μεγαλύτερο πλήθος επισκέψεων είναι η", ('{}'*16).format(*ht.max_days_card), "με συνολικά ", ht.max_days, ".")
    print("Η ημέρα με το μεγαλύτερο πλήθος επισκέψεων είναι η", day_list[day_count.index(max(day_count))], ".")
    print("Ο συνολικός αριθμός συγκρούσεων στον τελικό πίνακα είναι", ht.collisions)


if __name__ == '__main__':
    presentation()
    hash_table()











