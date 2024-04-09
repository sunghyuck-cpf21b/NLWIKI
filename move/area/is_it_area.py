'''
def position_check(html, position):
    result = True
    html_list = html.split(' . ')
    dot_count = html.count(' . ')
    var = 0     # 상황에 따른 위치 조정 변수
    now_position = html_list[dot_count-1]
    if position in now_position:
        result = False
    return result
'''

def is_is_area(html, col, row):
    result = True
    if '선택한 범위' in html:
        html_list = html.split(' . ')
        dot_count = html.count(' . ')
        area = html_list[dot_count-1]
        if dot_count == 4:
            area = html_list[dot_count - 2]
        if ':' in area:
            limit = area.split(':')
            start = limit[0]
            end = limit[1]
            start_num = int(start.split(col)[-1])
            end_num = int(end.split(col)[-1])
            if start_num <= int(row) and int(row) <= end_num:
                result = False
    return result

# 코드 실행할 때, 이미 클릭되어 있는 다른 셀 주소의 정보가 가져와지는거 방지하기
# 셀에 하이퍼링크로 추가정보 연결되어있을 때 '내부링크. ~' 같은 형식으로 내용에 같이 적혀있는데 이거 잘라내기
# 그리고 A column 정보 가져오기 결과가
# ['전라도 김치 혐오. 내부 링크. 전김!"A" 1', '2022.11.21', 'A5', 'A5', '', 'A8', 'A8', 'A8', 'A8', 'A8', 'A8', 'A8', 'A15', '', '2023.4.11', '2023.4.11', '', 'A20', '2023.4.18', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.28', '2023.4.28', '2023.4.28', '2023.4.28', '2023.4.28', '2023.5.13', '2023.5.13', '', 'A37', 'A37', 'A37', 'A37', 'A37', 'A37', 'A37', 'A44', 'A44', 'A44', '2023.06.12', '', 'A49', '2023.06.13', '2023.06.13', '2023.06.13', '2023.06.13', '', 'A55', 'A55', 'A55', '2023.06.18', '2023.06.18', '2023.06.18', '2023.06.18', '2023.06.18']
# 이와 같은데 문제 파악하고 수정하기



# 조건
'''
1. aria-label 이라는 속성이 존재하는지 -> 본문에 if문으로 작성됨
2. 입력된 위치와 실제 위치가 동일한지

'''
'''
def position_check(html):
    result = 
    html_list = html.split
    return
'''

def position_check(tags, cell_info,col,row):
    result = False
    if 'aria-label' not in tags:
        result = True
        # print('1번 if', result)
        return result
    index = 1
    add_index = 0
    if '본문' in cell_info:
        add_index += 1
    if '선택한 범위' in cell_info:
        add_index += 1
    if cell_info.count(' . ') == 1:
        index = 0
    html_list = cell_info.split(' . ')
    # print(tags, cell_info)
    # print(col+str(row), 'list = ', html_list, index, add_index)
    if (len(html_list)-1) < (index+add_index):
        return result
    position = html_list[index+add_index]
    if '선택한 범위' in cell_info:
        area = position.split(col)
        area_1 = int(area[1][:-1])
        area_2 = int(area[2])
        if (area_1 <= row) and (row <= area_2):
            # print('2번 if', result)
            result = True
    elif (col+str(row)) == position:
        # print('3번 if', result)
        result = True

    if result:
        print('clear')
    return result
