import numpy as np
from scipy.sparse import *
from collections import defaultdict
import itertools
from operator import itemgetter
import sys

##          Εφαρμογή Αραιών Μητρών
##          Αναλυτικά σχόλια για τον κώδικα στην αναφορά!


def presentation():
    print("Άσκηση αραιών μητρών!")
    print("Αρχικά, θα κατασκευάσουμε τις 10.000 τριάδες που αντιστοιχούν σε αραιά μήτρα διαστάσεων 1000x1000 που περιέχει μηδενικά στο 99% και τιμές από 1.0 εώς 5.0 σε ποσοστό 1%")
    print("Επιλέξτε 1 για απάντηση του ερωτήματος Α.")
    print("Επιλέξτε 2 για απάντηση των ερωτημάτων B και Γ.")
    e = int(input("Επιλογή:" ))
    if e==1:
        question_A()
    elif e==2:
        question_BC()
    else:
        print("Δεν υπάρχει αυτή η επιλογή! Ξαναπροσπαθήστε...")
        sys.exit()

def makeMatrix():
    global row
    global col
    global val
    np.random.seed(1053711)
    row = np.random.randint(0, 1000, 10000)
    col = np.random.randint(0, 1000, 10000)
    
    q=1
    while q:
        i=0
        for k in range(1000):
            if row[k]==col[k]:
                col[k]=np.random.randint(0, 1000)
                i += 1
        if i==0:
            break

    global mat_csr
    global mat

    val = np.round(np.random.uniform(1.0, 5.0, 10000), 1)        
    mat_coo = coo_matrix((val, (row, col)), shape=(1000, 1000))
    mat_csr = mat_coo.tocsr()

    global dnext
    dnext = defaultdict(list)
    for i,j in zip(row, col):
        dnext[i].append(j)
    
    return mat_csr



def question_A():

    print("Ταξίδια με 1 ή 2 πτήσεις:")
    print("Επιλέξτε τον αριθμό του αεροδρομίου σας (0 - 999) και δείτε τα διαθέσιμα ταξίδια με έως και 2 πτήσεις (0 - 999) σε αεροδρόμια:")
    e = int(input("Επιλογή:" ))
    if e<0 or e>999:
        print("Δεν υπάρχει αυτή η επιλογή! Ξαναπροσπαθήστε...")
        sys.exit()
    
    dest1 = sorted(dnext[e])
    dest2 = []
    print("Απευθείας ταξίδια από το αεροδρόμιό σας:", dest1)
    
    for i in (dest1):
        dest2.append(dnext [i])
        
    dest2_merged = sorted(list(itertools.chain(*dest2)))

    for i in range(len(dest1)):
        j = 0
        while j < len(dest2_merged):
            if dest1[i]==dest2_merged[j]:
                dest2_merged.pop(j)
            else:
                j += 1

                
    print("Ταξίδια 2 πτήσεων από το αεροδρόμιό σας:", sorted(dest2_merged))
    return



def question_BC():
    
    print("Κυκλικά ταξίδια:")
    print("Επιλέξτε τον αριθμό του αεροδρομίου σας (0 - 999) και δείτε τα διαθέσιμα κυκλικά ταξίδια (0 - 999) σε αεροδρόμια:")
    e = int(input("Επιλογή:" ))
    if e<0 or e>999:
        print("Δεν υπάρχει αυτή η επιλογή! Ξαναπροσπαθήστε...")
        sys.exit()

    two_flights = defaultdict(list)
    three_flights = defaultdict(list)
    four_flights = defaultdict(list)
    five_flights = defaultdict(list)
    six_flights = defaultdict(list)
    seven_flights = defaultdict(list)
    eight_flights = defaultdict(list)
    final_trip_list = defaultdict(list)
    trips = []

    print("Επιλέξτε τον μέγιστο αριθμό των πτητικών σκελών του ταξιδιού")
    print("Προειδοποίηση: Για επιλογή μεγαλύτερη των 6 πτητικών σκελών ενδέχεται να υπάρχει καθυστέρηση αρκετών λεπτών!")
    nmax = int(input("Επιλογή:" )) + 1
    if nmax<0 or nmax>10:
        print("Δεν υπάρχει αυτή η επιλογή! Ξαναπροσπαθήστε...")
        sys.exit()
    print(" ")
    print("Επιλέξατε μέχρι", nmax - 1, "πτητικά σκέλη.")
    
    def find_round_trips(begin, end, graph, nmax):
        trip = [(begin, [begin])]
        while len(trip):
            node, path = trip.pop(0)
            if path[-1] == end:
               yield path
            for next_node in graph[node]:
                if next_node in path[1:]:
                    continue
                else:
                    if len(path)<nmax:
                        trip.append((next_node, path + [next_node]))

    print("Επιλέξτε 1 για να δείτε όλα τα κυκλικά ταξίδια από το αεροδρόμιό σας.")
    print("Επιλέξτε 2 για να δείτε τα νόμιμα κυκλικά ταξίδια βάσει των χρονικών ορίων, μαζί με τον χρόνο που απαιτούν και τα μικρότερα/μεγαλύτερα ταξίδια, χωρίς να επιτρέπεται να γίνει ταξίδι στην ίδια ενδιάμεση πόλη 2 φορές.")
    a = int(input("Επιλογή:" ))
    print(" ")
    print("Γίνονται υπολογισμοί...")
    print(" ")
    if a==1:
        [print(x) for x in find_round_trips(e, e, dnext, nmax)]
    elif a==2:
        [trips.append(x[:]) for x in find_round_trips(e, e, dnext, nmax)]
        trips.pop(0)
        
        def find_legal_trips(trip):
            return len(trip) == len(set(trip))
        
        i = 0
        while i < len(trips):
           if find_legal_trips(trips[i][1:-1]):
               i += 1
           else:
               trips.pop(i)
            
        def find_time(l):
            time = 0
            value_list = []
            for i in range(len(l)-1):
                value_list.append(l[i:i+2])
            for i in range(len(value_list)):
                time += (mat_csr[value_list[i][0], value_list[i][1]])
            return time

        
        for i in range(len(trips)):
            time = find_time(trips[i])
            trip = tuple(trips[i])
            if len(trips[i])==3:
                two_flights[trip]=time
                if time <= 4:
                    final_trip_list[trip]=time
            elif len(trips[i])==4:
                three_flights[trip]=time
                if time <= 7.5:
                    final_trip_list[trip]=time
            elif len(trips[i])==5:
                four_flights[trip]=time
                if time <= 10.5:
                    final_trip_list[trip]=time
            elif len(trips[i])==6:
                five_flights[trip]=time
                if time <= 14:
                    final_trip_list[trip]=time
            elif len(trips[i])==7:
                six_flights[trip]=time
                if time <= 17:
                    final_trip_list[trip]=time
            elif len(trips[i])==8:
                seven_flights[trip]=time
                if time <= 20.5:
                    final_trip_list[trip]=time
            elif len(trips[i])==9:
                eight_flights[trip]=time
                if time <= 24:
                    final_trip_list[trip]=time

        print("Διαθέσιμα κυκλικά ταξίδια που πληρούν τις χρονικές προϋποθέσεις:")
        for key in final_trip_list:  
            print(key, "των",len(list(key))-1,"πτητικών σκελών με συνολικό χρόνο", final_trip_list[key],"ωρών." )
        

        print(" ")
        print("Για το ερώτημα Γ:")
        print(" ")

        two_flights = sorted(two_flights.items(), key=itemgetter(1))
        three_flights = sorted(three_flights.items(), key=itemgetter(1))
        four_flights = sorted(four_flights.items(), key=itemgetter(1))
        five_flights = sorted(five_flights.items(), key=itemgetter(1))
        six_flights = sorted(six_flights.items(), key=itemgetter(1))
        seven_flights = sorted(seven_flights.items(), key=itemgetter(1))
        eight_flights = sorted(eight_flights.items(), key=itemgetter(1))

        if len(two_flights):
            print("Το μικρότερο ταξίδι με 2 πτητικά σκέλη είναι το", two_flights[0][0],"διάρκειας", two_flights[0][1],"ωρών." )
            print("Το μεγαλύτερο ταξίδι με 2 πτητικά σκέλη είναι το", two_flights[len(two_flights)-1][0],"διάρκειας", two_flights[len(two_flights)-1][1],"ωρών." )
        if len(three_flights):
            print("Το μικρότερο ταξίδι με 3 πτητικά σκέλη είναι το", three_flights[0][0],"διάρκειας", three_flights[0][1],"ωρών." )
            print("Το μεγαλύτερο ταξίδι με 3 πτητικά σκέλη είναι το", three_flights[len(three_flights)-1][0],"διάρκειας", three_flights[len(three_flights)-1][1],"ωρών." )
        if len(four_flights):
            print("Το μικρότερο ταξίδι με 4 πτητικά σκέλη είναι το", four_flights[0][0],"διάρκειας", four_flights[0][1],"ωρών." )
            print("Το μεγαλύτερο ταξίδι με 4 πτητικά σκέλη είναι το", four_flights[len(four_flights)-1][0],"διάρκειας", four_flights[len(four_flights)-1][1],"ωρών." )
        if len(five_flights):
            print("Το μικρότερο ταξίδι με 5 πτητικά σκέλη είναι το", five_flights[0][0],"διάρκειας", five_flights[0][1],"ωρών." )
            print("Το μεγαλύτερο ταξίδι με 5 πτητικά σκέλη είναι το", five_flights[len(five_flights)-1][0],"διάρκειας", five_flights[len(five_flights)-1][1],"ωρών." )
        if len(six_flights):
            print("Το μικρότερο ταξίδι με 6 πτητικά σκέλη είναι το", six_flights[0][0],"διάρκειας", six_flights[0][1],"ωρών." )
            print("Το μεγαλύτερο ταξίδι με 6 πτητικά σκέλη είναι το", six_flights[len(six_flights)-1][0],"διάρκειας", six_flights[len(six_flights)-1][1],"ωρών." )
        if len(seven_flights):
            print("Το μικρότερο ταξίδι με 7 πτητικά σκέλη είναι το", seven_flights[0][0],"διάρκειας", seven_flights[0][1],"ωρών." )
            print("Το μεγαλύτερο ταξίδι με 7 πτητικά σκέλη είναι το", seven_flights[len(seven_flights)-1][0],"διάρκειας", seven_flights[len(seven_flights)-1][1],"ωρών." )
        if len(eight_flights):
            print("Το μικρότερο ταξίδι με 8 πτητικά σκέλη είναι το", eight_flights[0][0],"διάρκειας", eight_flights[0][1],"ωρών." )
            print("Το μεγαλύτερο ταξίδι με 8 πτητικά σκέλη είναι το", eight_flights[len(eight_flights)-1][0],"διάρκειας", eight_flights[len(eight_flights)-1][1],"ωρών." )
    else:
        print("Δεν υπάρχει αυτή η επιλογή! Ξαναπροσπαθήστε...")
        sys.exit()
    
    
    
    
    return

    
if __name__ == '__main__':
    mat_csr = makeMatrix()
    presentation()

    
    
    
