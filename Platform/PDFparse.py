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

#opening the pdf and splitting the page vertically
for i in range(12, 100):
    if (i != 31):
        with pdfplumber.open(pdf_file) as pdf:
            page = pdf.pages[i]
            left = page.crop((0, 0, 0.5 * float(page.width), page.height))
            right = page.crop((0.5 * float(page.width), 0, page.width, page.height))
            text = left.extract_text()
            righttext = right.extract_text()

    #previous regular expression compiles
    #city_re = re.compile(r'^[A-Z]*$')
    #intake_re = re.compile(r'Intake:')
    # address_re4 = re.compile(r'^\d\s\w[a-z]+\s[A-Z][a-z]+\s[A-Z]?[a-z]*\s?[A-Z]?[a-z]*.*')
    #cityStateZip_re = re.compile(r'^[A-Za-z]+\s?[A-Za-z]*\s?[A-Za-z]*,\s[A-Za-z]*\s[A-Za-z]*\s?\d{5}')
    #address_re = re.compile(r'^[A-Za-z]*\s?[\d.]*\d{1,5}?[a-z\s]*\d{1,5}?-?\w?\s[A-Z.]*\d?\d?[a-z]*\s?[A-Z][a-z]+.*')

    # regular expression compiles
    cityStateZip_re = re.compile(r'^[A-Za-z\s]+,\s[A-Za-z]*\s[A-Za-z]*\s?\d{5}')

    address_re = re.compile(r'^\d*-?\d*[A-Za-z]*\s?[\d.]*\d{1,5}?[a-z\s]*\d{1,5}?-?\w?\s[A-Z.]*\d?\d?[a-z]*\s?[A-Z][a-z]+.*')
    address_re2 = re.compile(r'^P\.O\.')
    address_re3 = re.compile(r'^[A-Za-z]+\s[A-Z]\s[A-Za-z]+\s[a-z\s]+[A-Za-z]+')
    address_re4 = re.compile(r'^\d\s\w[a-z]+\s[A-Z]?[a-z]*\s?[A-Z]?[a-z]*\s?[A-Z]?[a-z]*.*')
    address_re5 = re.compile(r'^[A-Za-z]+\s[\d.]+\s[A-Za-z\s]+')
    address_re6 = re.compile(r'^\d{1,5}\s[A-Z][A-Z]\s[\da-z]+\s[A-Z][a-z]+.*')
    address_re7 = re.compile(r'^[A-Z][a-z]+\s[A-Z][a-z]+\s\d{1,4}\s?$')

    phone_re = re.compile(r'Phone:')

    # parsing the left side of the page
    for line in text.split('\n'):

        if cityStateZip_re.match(line):
            city, other = line.split(",")
            other = other[1:]
            if (other.count(" ") == 3):
                state1, state2, zipcode = other.split()
                state = state1 + " " + state2
            else:
                state, zipcode = other.split()
            cityData.append(city)
            stateData.append(state)
            zipData.append(zipcode)

        if (address_re.match(line) or address_re2.match(line) or address_re3.match(line) or address_re4.match(line)
            or address_re5.match(line) or address_re6.match(line) or address_re7.match(line)):
            if (not("Suite" in line or "12 South Recovery" in line or "P.O. Box 400" in line)):
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
            else:
                state, zipcode = other.split()
            cityData.append(city)
            stateData.append(state)
            zipData.append(zipcode)

        if (address_re.match(line) or address_re2.match(line) or address_re3.match(line) or address_re4.match(line)
            or address_re5.match(line) or address_re6.match(line) or address_re7.match(line)):
            if (not("Suite" in line or "12 South Recovery" in line or "P.O. Box 400" in line)):
                address = line
                addressData.append(address)

        if phone_re.match(line):
            helper, phone = line.split(':')
            phoneData.append(phone)

#store field values into DataFrame
data = {'State': stateData, 'City': cityData, 'Zip': zipData, 'Address': addressData,
            'Phone': phoneData}
df = pd.DataFrame(data)
print(df)
#df.to_csv("mental_health_parse.csv")

#NOTES
#page 32: American Samoa
#address_re3: West C Street (page 31)
#address_re4: 5 Mareblu (page 79)
#address_re5: Mile 111.5 Old Richardson Highway (page 27)
#address_re6: 7722 NW 42nd Avenue (page 45)
#address_re7: Federal Route 9 (page 54)

#excludes
#Facility Name: 12 South Recovery (page 97)
#Two Address Lines: P.O. Box 400 (page 99)

#considerations/modifications
    # if (not(cityData.length == stateData.length == zipData.length == addressData == phoneData)):
    #     print("Page:", i)
    #     sys.exit()



