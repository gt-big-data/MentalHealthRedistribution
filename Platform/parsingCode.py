import pandas
import pdfplumber
import re

pdf_file = 'National_Directory_MH_facilities.pdf' 

data = []

rx_dict = {
    'addressPattern2': re.compile(r'^[0-9]+[a-zA-Z\s-]'),
    'addressPattern1': re.compile(r'([a-zA-Z\s]+),(\s[a-zA-Z\s.0-9]+)\s(\d{5})'), 
    'phonePattern': re.compile(r'^Phone:\s([(]\d{3}[)]\s\d{3}[-]\d{4}[.\sa-zA-Z0-9]*)')
}

def parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, rx
    return None, None

address2 = ""
state = ""
city = ""
zips = ""
phone = ""

with pdfplumber.open(pdf_file) as pdf:
    for i in range(600, 920):
        page = pdf.pages[i]
        #track pages during parsing
        print("PAGE: " + str(i))
        left = page.crop((0, 0, 0.5 * float(page.width), page.height))
        right = page.crop((0.5 * float(page.width), 0, page.width, page.height))
        leftText = left.extract_text()
        rightText = right.extract_text()

        entireTextA = leftText.split('\n')
        for num in range(0, len(entireTextA)):
            line = entireTextA[num]
            key, match = parse_line(line)
            if key == 'addressPattern2' and "2020 DIRECTORY OF MENTAL HEALTH FACILITIES" not in line:
                address2 = line.strip()
                # j = num
                # item = entireTextA[j]
                # while(j < len(entireTextA) - 1):
                #     key2, match2 = parse_line(entireTextA[j])
                #     if key2 == "addressPattern1" or "2020 DIRECTORY OF MENTAL HEALTH FACILITIES" in entireTextA[j]:
                #         break
                #     if address2 == "":
                #         address2 = entireTextA[j].strip()
                #         j = j + 1
                #     else:
                #         address2 = address2 + ", " + entireTextA[j].strip()
                #         j = j + 1
            if key == 'addressPattern1':
                if address2 == "":
                    address2 = entireTextA[num - 1].strip()
                matches = match.finditer(line)
                for item in matches:
                    city = item.group(1).strip()
                    state = item.group(2).strip()
                    zips = item.group(3).strip()
                    address1 = item.group(0).strip()
            if key == 'phonePattern':
                matches = match.finditer(line)
                for item in matches:
                    phone = item.group(1).strip()
                row = {'State': state, 'City': city, 'Zip': zips, 'Address': address2, 'Phone': phone}
                data.append(row)
                address2 = ""
                state = ""
                city = ""
                zips = ""
                phone = ""

        entireTextB = rightText.split('\n')
        for num in range(0, len(entireTextB)):
            line = entireTextB[num]
            key, match = parse_line(line)
            if key == 'addressPattern2' and "2020 DIRECTORY OF MENTAL HEALTH FACILITIES" not in line:
                address2 = line.strip()
                # j = num
                # item = entireTextB[j]
                # while(j < len(entireTextB) - 1):
                #     key2, match2 = parse_line(entireTextB[j])
                #     if key2 == "addressPattern1" or "2020 DIRECTORY OF MENTAL HEALTH FACILITIES" in entireTextB[j]:
                #         break
                #     if address2 == "":
                #         address2 = entireTextB[j].strip()
                #         j = j + 1
                #     else:
                #         address2 = address2 + ", " + entireTextB[j].strip()
                #         j = j + 1
            if key == 'addressPattern1':
                if address2 == "":
                    address2 = entireTextB[num - 1].strip()
                matches = match.finditer(line)
                for item in matches:
                    city = item.group(1).strip()
                    state = item.group(2).strip()
                    zips = item.group(3).strip()
                    address1 = item.group(0).strip()
            if key == 'phonePattern':
                matches = match.finditer(line)
                for item in matches:
                    phone = item.group(1).strip()
                row = {'State': state, 'City': city, 'Zip': zips, 'Address': address2, 'Phone': phone}
                data.append(row)
                address2 = ""
                state = ""
                city = ""
                zips = ""
                phone = ""

df = pandas.DataFrame(data)

file_name = 'HealthData.xlsx'
  
# saving the excel 
df.to_excel(file_name) 
print('DataFrame is written to Excel File successfully.')
    

