import requests
import pandas as pd
from bs4 import BeautifulSoup

page = requests.get("https://mhanational.org/issues/2021/mental-health-america-all-data")
soup = BeautifulSoup(page.content, "html.parser")

data = list(soup.select(".cols-4"))

for i in range(1, len(data)):
    rank = []
    state = []
    percentage = []
    number = []

    rankings = list(data[i].select(".rankings"))
    
    for j in range(0, len(rankings)):
        fields = list(rankings[j].select(".views-field"))
        for k in range(0, len(fields)):
            if (k == 0):
                rank.append(fields[k].get_text())
            elif (k == 1):
                state.append(fields[k].get_text())
            elif (k == 2):
                percentage.append(fields[k].get_text())
            elif (k == 3):
                number.append(fields[k].get_text())

    dfData = {"Rank": rank, "State": state, "Percentage": percentage, "Number": number}
    df = pd.DataFrame(dfData)
    
    if (i == 1):
        df.to_csv("did_not_cover_mental_or_emotional_problems.csv")
    elif (i == 2):
        df.to_csv("youth_past_year_substance_use.csv")
    elif (i == 3):
        df.to_csv("received_some_consistent_treatment.csv")
    elif (i == 4):
        df.to_csv("youth_with_severe_mde.csv")
    elif (i == 5):
        df.to_csv("students_identified_as_SED(IEP).csv")
    elif (i == 6):
        df.to_csv("youth_with_past_year_depression_who_did_not_receive_treatment.csv")
    elif (i == 7):
        df.to_csv("youth_ranking.csv")
    elif (i == 8):
        df.to_csv("youth_prevalence_of_MDE.csv")
    elif (i == 9):
        df.to_csv("adults_with_AMI_who_did_not_receive_treatment.csv")
    elif (i == 10):
        df.to_csv("adults_with_cognitive_disability_who_could_not_see_a_doctor_due_to_cost.csv")
    elif (i == 11):
        df.to_csv("adult_ranking.csv")
    elif (i == 12):
        df.to_csv("adult_suicidal_ideation.csv")
    elif (i == 13):
        df.to_csv("adult_prevalence_of_mental_illness.csv")
    elif (i == 14):
        df.to_csv("adults_with_AMI_who_are_uninsured.csv")
    elif (i == 15):
        df.to_csv("adult_substance_use_disorder.csv")
    elif (i == 16):
        df.to_csv("adults_with_AMI_who_report_unmet_need_for_treatment.csv")
    elif (i == 17):
        df.to_csv("prevalence_of_mental_illness.csv")
    elif (i == 18):
        df.to_csv("access_to_care_ranking.csv")
    elif (i == 19):
        df.to_csv("overall_ranking.csv")
    elif (i == 20):
        df.to_csv("workforce_need.csv")