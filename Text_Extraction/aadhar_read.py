import re


def extract_aadhar_info(text):
    text = text.strip()
    lines = text.split('\n')
    lines = [x for x in lines if x != '']

    names = lines[1].split(' ')
    first_name = names[0]
    last_name = None
    middle_name = None
    if len(names) == 2:
        last_name = names[1]
    elif len(names) == 3:
        middle_name = names[1]
        last_name = names[2]
    # date regex:
    date_re = re.compile('[0-9]+\/[0-9]+\/[0-9]+')
    dates = date_re.findall(text)
    dob = dates[0]

    # Gender:
    if 'female' in text.lower():
        gender = "FEMALE"
    else:
        gender = "MALE"

    # aadhar number:
    aadhar_re = re.compile('[0-9]+ [0-9]+ [0-9]+')
    aadhar_number = aadhar_re.findall(text)[0]
    return {
        'id_type': 'Aadhar Card',
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'DOB': dob,
        'gender': gender,
        'aadhar_number': aadhar_number
    }
