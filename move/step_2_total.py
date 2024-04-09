import ast
from datetime import datetime

print(__name__)

txt_file_name = ['occ_time', 'person', 'subject', 'content']

index = []

date_list = []
add_path = 'move/'
if __name__ == '__main__':
    add_path = ''
with open(add_path+'occ_date.txt', 'r') as f:
    date = ast.literal_eval(f.read())
    for i in range(len(date)):
        if date[i] != ['']:
            index.append(i)
            date_list.append(date[i])


time_list = []
person_list = []
subject_list = []
content_list = []
database_list = [time_list, person_list, subject_list, content_list]


for i in range(len(txt_file_name)):
    name = txt_file_name[i]+'.txt'
    with open(add_path+name, 'r', encoding='utf-8') as f:
        nonlan_list = ast.literal_eval(f.read())
        for j in index:
            database_list[i].append(nonlan_list[j])



database_list.insert(0, date_list)
# print(database_list)
with open(add_path+'total.txt', 'w', encoding='utf-8') as f:
    nonlan_total = []
    for i in range(len(date_list)):
        nonlan = []
        for category in database_list:
            nonlan.append(category[i])
        nonlan_total.append(nonlan)

    # print(nonlan_total)
    nonlan_result = []
    id_num = 0
    for data in nonlan_total:
        DD = [int(i) for i in data[0][0].split('.')]
        TT = []
        #print(data)
        if 'PM' in data[1][0] and data[1][0].split(':')[0] != '12':
            TT = [int(i) for i in data[1][0].split(':')[:2]]
            TT[0] += 12
        elif 'AM' in data[1][0]:
            TT = [int(i) for i in data[1][0].split(':')[:2]]
        else:
            TT = [0,0]
        # print(DD, TT)
        DDTT = datetime(DD[0], DD[1], DD[2], TT[0], TT[1])
        # print(DDTT)

        if data[2][0] == '':
            data[2][0] = '신원미상'
        if data[3][0] == '':
            data[3][0] = '제목없음'
        # print(nonlan_result)
        nonlan_result.append([DDTT, ', '.join(data[2]), ', '.join(data[3]), '\n'.join(data[4])])
        split_code = 'split_subuncream_point'
        total_content = split_code.join([str(id_num),str(DDTT), str(data[2]), str(data[3]), str(data[4])])
        id_num += 1
        f.write(total_content+'\n')
