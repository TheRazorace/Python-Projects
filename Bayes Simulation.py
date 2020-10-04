import numpy as np

pair_number = 1000000 ##Αριθμός ζευγαριών = 1.000.000

h0_0 = 0              ##Μετρητής για προβλέψεις H0 και η σωστή πρόβλεψη είναι H0
h0_1 = 0              ##Μετρητής για προβλέψεις H1 και η σωστή πρόβλεψη είναι H0
h1_0 = 0              ##Μετρητής για προβλέψεις H0 και η σωστή πρόβλεψη είναι H1
h1_1 = 0              ##Μετρητής για προβλέψεις H1 και η σωστή πρόβλεψη είναι H1

##Αρχικοποίηση 1.000.000 ζευγαριών [x1,x2] από την f0(x1,x2) και άλλων 1.000.000 ζευγαριών από την f1(x1,x2)
f0_data = np.random.multivariate_normal([0, 0] , [[1 , 0],[0 , 1]] ,pair_number)
f1_data = np.random.multivariate_normal([-1, 1] , [[1 , 0],[0 , 1]] ,pair_number)

##Αρχικοποίηση κενών πινάκων για τις συναρτήσεις f0 = f0(x1)*f0(x2) και f1 = f1(x1)*f1(x2)
f0 = [0 for q in range(pair_number)]
f1 = [0 for q in range(pair_number)]

##Δημιουργία συνάρτησης κανονικής κατανομής
def normal(x,m,s):
    return (1/np.sqrt(2*np.pi*s*s)) * np.exp(-((x - m)**2)/(2*s*s))

## 1ος υπολογισμός: Για τα ζευγάρια [x1,x2] από την f0(x1,x2)
for i in range(pair_number):
    ## Υπολογισμός f0, f1
    f0[i] = normal(f0_data[i][0], 0, 1)* normal(f0_data[i][1], 0, 1)
    f1[i] = (0.5 *normal(f0_data[i][0], -1, 1) + 0.5*normal(f0_data[i][0], 1, 1)) * (0.5*normal(f0_data[i][1], -1, 1) + 0.5*normal(f0_data[i][1], 1, 1))
    
    ## Τεστ λόγου πιθανοφάνειας: Αν (f1/f0) > 1 -> Απόφαση υπέρ της υπόθεσης H1
    if(f1[i] > f0[i]):
        h0_1 = h0_1 + 1
    ##Αλλιώς, Απόφαση υπέρ της υπόθεσης H0
    else:
        h0_0 = h0_0 + +1

## 2ος υπολογισμός: Για τα ζευγάρια [x1,x2] από την f1(x1,x2)
for i in range(pair_number):
    ## Υπολογισμός f0, f1
    f0[i] = normal(f1_data[i][0], 0, 1)* normal(f1_data[i][1], 0, 1)
    f1[i] = (0.5 *normal(f1_data[i][0], -1, 1) + 0.5*normal(f1_data[i][0], 1, 1)) * (0.5*normal(f1_data[i][1], -1, 1) + 0.5*normal(f1_data[i][1], 1, 1))
    
    ## Τεστ λόγου πιθανοφάνειας: Αν (f1/f0) > 1 -> Απόφαση υπέρ της υπόθεσης H1
    if(f1[i] > f0[i]):
        h1_1 = h1_1 + 1
    ##Αλλιώς, Απόφαση υπέρ της υπόθεσης H0
    else:
        h1_0 = h1_0 + +1

##Μέτρηση επιμέρους σφαλμάτων και συνολικού σφάλματος
print("Σφάλμα στην H0:", (h0_1/pair_number) * 100,"%")
print("Σφάλμα στην H1:", (h1_0/pair_number) * 100,"%")
print("Συνολικό σφάλμα:", (((0.5*h1_0 + 0.5*h0_1))/pair_number) * 100,"%")







         