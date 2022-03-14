import pandas as pd
import sys
import matplotlib.pyplot as plt

#Αποθήκευση αρχείου σε dataset
def ReadHousingData():
    
    #Ανάγνωση csv αρχείου
    try:
        df = pd.read_csv('housing.csv')
    except IOError:
        #Έξοδος αν αποτύχει
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    return df

if __name__ == '__main__': 
    
    df = ReadHousingData()
    
    print("\n---------------Οπτικοποίηση Δεδομένων---------------")
    
    plt.figure(1)
    df["longitude"].plot.hist(grid=True, bins=10, rwidth=1,
                   color='#607c8e', figsize = (10,10))
    plt.title('Longitude Histogram')
    plt.xlabel('Longitude Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(2)
    df["latitude"].plot.hist(grid=True, bins=10, rwidth=1,
                   color='#607c8e', figsize = (10,10))
    plt.title('Latitude Histogram')
    plt.xlabel('Latitude Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(3)
    df["housing_median_age"].plot.hist(grid=True, bins=50, rwidth=1,
                    color='#607c8e', figsize = (10,10))
    plt.title('Housing Median Age Histogram')
    plt.xlabel('Housing Median Age')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(4)
    df["total_rooms"].plot.hist(grid=True, bins=100, rwidth=1,
                    color='#607c8e', figsize = (10,10), range = (0,10000))
    plt.title('Total Rooms Histogram')
    plt.xlabel('Total Rooms')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(5)
    df["total_bedrooms"].plot.hist(grid=True, bins=100, rwidth=1,
                    color='#607c8e', figsize = (10,10), range = (0,3000))
    plt.title('Total Bedrooms Histogram')
    plt.xlabel('Total Bedrooms')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(6)
    df["population"].plot.hist(grid=True, bins=200, rwidth=1,
                    color='#607c8e', figsize = (10,10), range = (0,5000))
    plt.title('Population Histogram')
    plt.xlabel('Population')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(7)
    df["households"].plot.hist(grid=True, bins=100, rwidth=1,
                    color='#607c8e', figsize = (10,10), range = (0,3000))
    plt.title('Households Histogram')
    plt.xlabel('Households')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(8)
    df["median_income"].plot.hist(grid=True, bins=75, rwidth=1,
                    color='#607c8e', figsize = (10,10))
    plt.title('Median Income Histogram')
    plt.xlabel('Median Income')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(9)
    df["median_house_value"].plot.hist(grid=True, bins=100, rwidth=1,
                    color='#607c8e', figsize = (10,10))
    plt.title('Median House Value Histogram')
    plt.xlabel('Median House Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(10)
    df["ocean_proximity"].value_counts(sort=False).plot(kind="bar", figsize = (10,10))
    plt.title('Ocean Proximity Histogram')
    plt.xlabel('Ocean Proximity Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(11)
    df["longitude"].plot.hist(grid=True, bins=5, rwidth=1,
                   color='yellow', figsize = (10,10))
    df["latitude"].plot.hist(grid=True, bins=5, rwidth=1,
                   color='orange', figsize = (10,10))
    plt.title('Longitude (yellow) - Latitude (orange) Histogram')
    plt.xlabel('Longitude - Latitude Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(12)
    df["total_rooms"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='yellow', figsize = (10,10), range = (0,10000))
    df["total_bedrooms"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='orange', figsize = (10,10), range = (0,3000))
    plt.title('Total Rooms (yellow) - Total Bedrooms (orange) Histogram')
    plt.xlabel('Total Rooms - Total Bedrooms')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(13)
    df["population"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='yellow', figsize = (10,10), range = (0,5000))
    df["households"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='orange', figsize = (10,10), range = (0,3000))
    plt.title('Population (yellow) - Households (orange) Histogram')
    plt.xlabel('Population - Households')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(14)
    df["total_bedrooms"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='yellow', figsize = (10,10), range = (0,3000))
    df["households"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='orange', figsize = (10,10), range = (0,3000))
    plt.title('Total Bedrooms (yellow) - Households (orange) Histogram')
    plt.xlabel('Total Bedrooms - Households')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(15)
    df["total_rooms"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='yellow', figsize = (10,10), range = (0,10000))
    df["population"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='orange', figsize = (10,10), range = (0,5000))
    plt.title('Total Rooms (yellow) - Population (orange) Histogram')
    plt.xlabel('Total Rooms - Population')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    plt.figure(16)
    df["total_rooms"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='yellow', figsize = (10,10), range = (0,10000))
    df["population"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='orange', figsize = (10,10), range = (0,5000))
    df["total_bedrooms"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='blue', figsize = (10,10), range = (0,3000))
    df["households"].plot.hist(grid=True, bins=100, rwidth=1,
                   color='green', figsize = (10,10), range = (0,3000))
    plt.title("Total Rooms (yellow) - Population (orange) - Total Bedrooms (blue) - Households (green) Histogram")
    plt.xlabel('Total Rooms - Population - Total Bedrooms - Households')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=1)
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    