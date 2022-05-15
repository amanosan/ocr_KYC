import re


def extract_pan_info(text):
    lines = text.split('\n')
    lines = [x for x in lines if x != '']
    for i in range(len(lines)):
        if 'Permanent' in lines[i]:
            break
        i += 1

    pan_number = re.findall("[a-zA-Z0-9]+", lines[i + 1])[0]
    # print(pan_number)

    for i in range(len(lines)):
        if 'INCOME' in lines[i]:
            break
        i += 1
    names = lines[i+1].split(' ')
    first_name = names[0]
    middle_name = None
    last_name = None
    print(names)
    if len(names) == 2:
        last_name = names[1]
    elif len(names) == 3:
        middle_name = names[1]
        last_name = names[2]

    # date regex:
    date_re = re.compile('[0-9]+\/[0-9]+\/[0-9]+')
    dates = date_re.findall(text)
    dob = dates[0]
    # print(dob)
    return {
        'id_type': 'Pan Card',
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'DOB': dob,
        'pan_number': pan_number
    }
