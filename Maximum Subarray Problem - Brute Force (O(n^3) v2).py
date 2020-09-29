import time
import random
import sys

print("Αλγόριθμος BruteForce2.1 --> O(n^2)")
print("Θα δημιουργήσουμε δύο λίστες, η μία με διπλάσιο αριθμό στοιχείων από την άλλη, με seed τον ΑΜ και τιμές στο διάστημα (-100, 100)")
print("Επιλέξτε 1 για λίστες 5000 και 10000 στοιχείων αντιστοίχως.")
print("Επιλέξτε 2 για να καθορίσετε τον αριθμό στοιχείων")

#Καθορισμός μεγέθου λίστας
e = int(input("Επιλογή:" ))
if e==1:
    num=5000
elif e==2:
    print("Επιλογή αριθμού στοιχείων. Για παράδειγμα, επιλέξτε 100 για να δημιουργήσετε δύο λίστες των 100 και των 200 στοιχείων αντιστοίχως.")
    num=int(input("Επιλογή:" ))
else:
    print("Δεν υπάρχει αυτή η επιλογή! Ξαναπροσπαθήστε...")
    sys.exit()
    

#Συνάρτηση που δημιουργεί την λίστα με seed τον ΑΜ
random.seed(1053711)
def makeArr(num, maxn):
    arr = [0]*num                              #Δημιουργώ μία κενή λίστα με το δοσμένο μέγεθος
    for i in range (num):                      #Την γεμίζω με τυχαίους αριθμούς στο δοσμένο διάστημα
        arr[i] = random.randint(-maxn, maxn)
    return arr

arr = makeArr(num,100)
double_arr = makeArr(2*num, 100)



arr2 = [0]*(len(arr)+1)                             #Βοηθητική λιστα, αρχικά μηδενικός, ίδιου μήκους με την πρώτη λίστα
arr3 = [0]*(len(double_arr)+1)                      #Βοηθητική λιστα, αρχικά μηδενικός, ίδιου μήκους με την δεύτερη λίστα

#Συνάρτηση που υπολογίζει το μέγιστο υποάθροισμα
def bf2b(arr, arr2):
    n = len(arr)                                    #Μήκος λίστας
    m = (0, 0, 0)
    for i in range (n):                  
        arr2[i+1]=arr2[i]+arr[i]                    #Αποθήκευση υποαθροισμάτων στον βοηθητική λιστα
    for i in range (n):                             #Πρώτο σκανάρισμα της βοηθητικής λίστας
        for j in range (i+1,n+1):                   #Δεύτερο σκανάρισμα της βοηθητικής λίστας
            s = arr2[j] - arr2[i] 
            if s > m[0]:
                m = (s, i, j)                       #Καταχώρηση αποτελέσματος αν είναι καλύτερο
    return m                                        #Επιστρέφει το αποτέλεσμα
    
print("Γίνεται υπολογισμός...")
to = time.time()                        #Αρχή πρώτης χρονομέτρησης
m = bf2b(arr, arr2)                     #Υπολογισμός μέγιστου υποαθροίσματος πρώτου πίνακα
t1 = time.time()                        #Τέλος πρώτης χρονομέτρησης, αρχή δεύτερης χρονομέτρησησς                       
d = bf2b(double_arr, arr3)              #Υπολογισμός μέγιστου υποαθροίσματος δεύτερου πίνακα
t2 = time.time()                        #Τέλος δεύτερης χρονομέτρησης


print("Μέγιστο υπό-άθροισμα λίστας", num,"στοιχείων:", m[0])
print("Θέση αρχής μέγιστης υπό-λίστας:", m[1],". Θέση τέλους μέγιστης υπό-λίστας:", m[2],".")
print("Χρόνος υπολογισμού:",t1 - to,'seconds')
print("Μέγιστο υπό-άθροισμα λίστας", 2*num,"στοιχείων:", d[0])
print("Θέση αρχής μέγιστης υπό-λίστας:", d[1],". Θέση τέλους μέγιστης υπό-λίστας:", d[2],".")
print("Χρόνος υπολογισμού:",t2 - t1,'seconds')

