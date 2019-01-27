from app.utils.stringutil import strstr, empty

def get_course_table(curArr):
    tableArr = [[] for _ in range(11)]
    colornum = 0
    colorArr = [
    'FF4040','39E639',
    'FF9640','33CCCC',
    'FFBF40','4671D5',
    'FFDE40','6A48D7',
    '9F3ED5',
    'B9F73E','E6399B',
    ]
    greyArr=['fff','f7f7f7']
    for i in range(11):
        flag = 0
        for week in curArr:
            if i != 0 and i!=2 and i!=4 and i!=8 and i-1>=0 and strstr(week[i], week[i-1]):
                flag += 1
                continue
            num = 1
            while i+num!=4 and i+num!=2 and i+num!=8 and i+num<11 and strstr(week[i], week[i+num]):
                num += 1
            attr = num if num > 1 else 0
            tableArr[i].append([
                attr, 
                week[i], 
                greyArr[0] if empty(week[i]) else colorArr[colornum]
            ])
            if not empty(week[i]):
                colornum = 0 if colornum == len(colorArr)-1 else colornum+1
        if flag == 8:
            tableArr[i].append('')
    return tableArr
