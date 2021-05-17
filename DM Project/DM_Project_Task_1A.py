import pandas as pd
import matplotlib.pyplot as plt
import sys

def ReadHealthcareData():
    
    #Ανάγνωση csv αρχείου
    try:
        df = pd.read_csv('healthcare-dataset-stroke-data.csv')
    except IOError:
        #Έξοδος αν αποτύχει
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    return df
    
def ShowPlots(df):   
    plt.figure(1)
    gender_series = df['gender']
    gender_series = gender_series.rename("Gender")
    count = gender_series.value_counts()
    count.plot(kind = 'pie', figsize = (12,12), autopct='%1.1f%%')
    
    plt.figure(2)
    age_series = df.sort_values('age')['age']
    count = age_series.value_counts().sort_index()
    line1 = count.plot(figsize = (12,12) )
    line1.set_ylabel("Number of People")
    line1.set_xlabel("Age")
    
    plt.figure(3)
    hp_series = df['hypertension']
    hp_series = hp_series.rename("Hypertension")
    count = hp_series.value_counts()
    count = count.rename(index = {0:'No', 1: 'Yes'})
    count.plot(kind = 'pie', figsize = (12,12), autopct='%1.1f%%')
    
    plt.figure(4)
    heart_disease_series = df['heart_disease']
    heart_disease_series = heart_disease_series.rename("Heart Disease")
    count = heart_disease_series.value_counts()
    count = count.rename(index = {0:'No', 1: 'Yes'})
    count.plot(kind = 'pie', figsize = (12,12), autopct='%1.1f%%')
    
    plt.figure(5)
    marriage_series = df['ever_married']
    marriage_series = marriage_series.rename("Ever Married")
    count = marriage_series.value_counts()
    count.plot(kind = 'pie', figsize = (12,12), autopct='%1.1f%%')
    
    plt.figure(6)
    marriage_series = df['work_type']
    marriage_series = marriage_series.rename("Work Type")
    count = marriage_series.value_counts()
    count.plot(kind = 'pie', figsize = (12,12), autopct='%1.1f%%')
    
    plt.figure(7)
    residence_series = df['Residence_type']
    residence_series = residence_series.rename("Residence Type")
    count = residence_series.value_counts()
    count.plot(kind = 'pie', figsize = (12,12), autopct='%1.1f%%')
    
    plt.figure(8)
    glucose_series = df['avg_glucose_level']
    glucose_series = glucose_series.rename("Average Glucose Level")
    level1 = glucose_series[(glucose_series>50) & (glucose_series<100)].count()
    level2 = glucose_series[(glucose_series>100) & (glucose_series<150)].count()
    level3 = glucose_series[(glucose_series>150) & (glucose_series<200)].count()
    level4 = glucose_series[(glucose_series>200)].count()
    glucose_series = pd.Series(
    data = {"50-100": level1, "100-150": level2, "150-200": level3, "200+": level4})
    bar1 = glucose_series.plot( kind = 'bar', figsize = (12,12))
    bar1.set_ylabel("Number of People")
    bar1.set_xlabel("Average Glucose Level")
    
    plt.figure(9)
    bmi_series = df['bmi']
    bmi_series = bmi_series.rename("BMI")
    level1 = bmi_series[(bmi_series>10) & (bmi_series<15)].count()
    level2 = bmi_series[(bmi_series>15) & (bmi_series<20)].count()
    level3 = bmi_series[(bmi_series>20) & (bmi_series<25)].count()
    level4 = bmi_series[(bmi_series>25) & (bmi_series<30)].count()
    level5 = bmi_series[(bmi_series>30) & (bmi_series<35)].count()
    level6 = bmi_series[(bmi_series>35) & (bmi_series<40)].count()
    level7 = bmi_series[(bmi_series>40) & (bmi_series<45)].count()
    level8 = bmi_series[(bmi_series>45)].count()
    bmi_series = pd.Series(
    data = {"10-15": level1, "15-20": level2, "20-25": level3, "25-30": level4,
            "30-35": level5, "35-40": level6, "40-45":level7, "45+": level8})
    bar2 = bmi_series.plot(kind = 'bar', figsize = (12,12))
    bar2.set_ylabel("Number of People")
    bar2.set_xlabel("BMI")
    
    plt.figure(10)
    smoking_series = df['smoking_status']
    smoking_series = smoking_series.rename("Smoking Status")
    count = smoking_series.value_counts()
    count.plot(kind = 'pie', figsize = (12,12), autopct='%1.1f%%')
    
    plt.figure(11)
    stroke_series = df['stroke']
    stroke_series = stroke_series.rename("Stroke")
    count = stroke_series.value_counts()
    count = count.rename(index = {0:'No', 1: 'Yes'})
    count.plot(kind = 'pie', figsize = (12,12), autopct='%1.1f%%')
    
    return


if __name__ == '__main__': 
    
    df = ReadHealthcareData()
    ShowPlots(df)