import re
import pdfplumber
import pandas as pd 

pdf_file = 'National_Directory_MH_facilities.pdf'

#arrays to store field values
cityData = []
stateData = []
zipData = []
addressData = []
phoneData = []

# regular expression compiles
cityStateZip_re = re.compile(r'^[A-Za-z\s]+,\s[A-Za-z]*\s[a-z]*\s?[A-Za-z]*\s?\d{5}')

address_re = re.compile(r'^\d*-?\d*[A-Za-z]*\s?[\d.]*\d{1,5}?[a-z\s]*\d{1,5}?-?\w?\s[A-Z.]*\d?\d?[a-z]*\s?[A-Z][a-z]+.*')
address_re2 = re.compile(r'^[A-Za-z]+\s[A-Z]\s[A-Za-z]+\s[a-z\s]+[A-Za-z]+')
address_re3 = re.compile(r'^\d\s\w[a-z]+\s[A-Z]?[a-z]*\s?[A-Z]?[a-z]*\s?[A-Z]?[a-z]*.*')
address_re4 = re.compile(r'^[A-Za-z]+\s[\d.]+\s[A-Za-z\s]+')
address_re5 = re.compile(r'^\d{1,5}\s[A-Z][A-Z]\s[\da-z]+\s[A-Z][a-z]+.*')
address_re6 = re.compile(r'^[A-Z][a-z]+\s[A-Z][a-z]+\s\d{1,4}\s?$')
address_re7 = re.compile(r'^\d{1,2}[a-z][a-z]\s[A-Za-z]+\s[A-Za-z][a-z]+\s[A-Z][a-z]+')
address_re8 = re.compile(r'^\d{1,5}\s\d{1,3}\s\d/\d\s[A-Z][a-z]+')
address_re9 = re.compile(r'^\d{3,5}\s\d{3,4}(th|nd)\s[A-Z][a-z]+')
address_re10 = re.compile(r'^[A-Z][a-z]+\s[A-Z][a-z]+\s\d{3,5}\s[A-Z][a-z]+\s[A-Z][a-z]+')

phone_re = re.compile(r'Phone:')

#opening the pdf and splitting the page vertically
for i in range(12, 300):
    if (i != 31):
        with pdfplumber.open(pdf_file) as pdf:
            page = pdf.pages[i]
            left = page.crop((0, 0, 0.5 * float(page.width), page.height))
            right = page.crop((0.5 * float(page.width), 0, page.width, page.height))
            text = left.extract_text()
            righttext = right.extract_text()

        # parsing the left side of the page
        for line in text.split('\n'):

            if cityStateZip_re.match(line):
                city, other = line.split(",")
                other = other[1:]
                if (other.count(" ") == 3):
                    state1, state2, zipcode = other.split()
                    state = state1 + " " + state2
                elif (other.count(" ") == 4):
                    state1, state2, state3, zipcode = other.split()
                    state = state1 + " " + state2 + " " + state3
                else:
                    state, zipcode = other.split()
                cityData.append(city)
                stateData.append(state)
                zipData.append(zipcode)

            if (address_re.match(line) or address_re2.match(line) or address_re3.match(line) or address_re4.match(line) or address_re5.match(line) 
                or address_re6.match(line) or address_re7.match(line) or address_re8.match(line) or address_re9.match(line) or address_re10.match(line)
                or "P.O. Box 1148" in line):
                if (not("Suite" in line or "12 South Recovery" in line or "Success 4 Kids and Families Inc" in line or "CHRIS 180 Inc" in line
                    or "2nd Chance Treatment Center" in line or "2nd Chance Mental Health Center" in line)):
                    address = line
                    addressData.append(address)

            if phone_re.match(line):
                helper, phone = line.split(':')
                phoneData.append(phone)

        #parsing the right side of the page
        for line in righttext.split('\n'):
            if cityStateZip_re.match(line):
                city, other = line.split(",")
                other = other[1:]
                if (other.count(" ") == 3):
                    state1, state2, zipcode = other.split()
                    state = state1 + " " + state2
                elif (other.count(" ") == 4):
                    state1, state2, state3, zipcode = other.split()
                    state = state1 + " " + state2 + " " + state3
                else:
                    state, zipcode = other.split()
                cityData.append(city)
                stateData.append(state)
                zipData.append(zipcode)

            if (address_re.match(line) or address_re2.match(line) or address_re3.match(line) or address_re4.match(line) 
                or address_re5.match(line) or address_re6.match(line) or address_re7.match(line) or address_re8.match(line) 
                or address_re9.match(line) or address_re10.match(line)):
                if (not("Suite" in line or "12 South Recovery" in line or "Recovery 4 Life" in line or "2nd Chance Treatment Center" in line
                        or "23rd Avenue Recovery Center" in line or "51st Avenue Recovery Center" in line)):
                    address = line
                    addressData.append(address)

            if phone_re.match(line):
                helper, phone = line.split(':')
                phoneData.append(phone)

    #check if there is an error for a page
    # if (not(len(cityData) == len(stateData) == len(zipData) == len(addressData) == len(phoneData))):
    #     print("Page:", (i + 1))
    #     quit()
            
#store field values into DataFrame
data = {'State': stateData, 'City': cityData, 'Zip': zipData, 'Address': addressData,
            'Phone': phoneData}
df = pd.DataFrame(data)
df.to_csv("mental_health_parse_1.csv")

#NOTES
#page 32: American Samoa

#address_re2: West C Street (page 31)
#address_re3: 5 Mareblu (page 79)
#address_re4: Mile 111.5 Old Richardson Highway (page 27)
#address_re5: 7722 NW 42nd Avenue (page 45)
#address_re6: Federal Route 9 (page 54)
#address_re7: 9th and Dahlia Street (page 151)
#address_re8: 515 28 3/4 Road (page 151)
#address_re9: 8823 115th Avenue (page 196)

#Facility Name: 12 South Recovery (page 97)
#P.O. Box 1148: No address, only P.O. Box on page 31



