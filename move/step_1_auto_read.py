import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

# chrome driver와 chrome의 버전을 맞추기 번거로우므로 driver 없이 실행할 수 있는 코드

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

driver.get('https://onedrive.live.com/edit.aspx?resid=1F117A02749EE87!110&ithint=file%2cxlsx&authkey=!ACIeFLQ1wz_yUX8')
driver.implicitly_wait(60)

# driver.find_element(By.ID, 'FormulaBar-NameBox-input').send_keys('A4')
# driver.switch_to.frame(driver.find_element(By.ID, 'FormulaBar-NameBox-input'))
position = driver.find_element(By.XPATH, "//iframe[@id='WacFrame_Excel_0']")
driver.switch_to.frame(position)

wait = WebDriverWait(driver, 10)
sheet_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.ewa-stb-tabs li")))

for sheet in sheet_list:
    if sheet.text == '본문':
        sheet.click()


element_pos = wait.until(EC.presence_of_element_located((By.ID, 'FormulaBar-NameBox-input')))
''' EC.~ 의 인수에 괄호를 두 번 감싸는 이유는, 첫 번째 괄호는 함수 호출용(일반적인 함수 사용법), 두 번째 괄호는 전달되는 인수를 튜플 형식으로 묶어주기 위함이다. '''
element_val = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#formulaBarTextDivId_textElement div')))
time.sleep(3)

'''
driver.execute_script("""
    var element = arguments[0];
    var value = arguments[1];
    
    element.value = value;
    
    element.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));
    """, element_pos, 'C4')
''' # -> 이유는 정확히 모르겠으나 제대로 동작하지 않음

'''
element_pos.click()
time.sleep(1)
element_pos.send_keys("C4", Keys.ENTER)
time.sleep(1)
print(element_val.text)
''' # -> 테스트용

col = ['A', 'B', 'C', 'D', 'E']
limit = 125
result = {}

from move.area import is_it_area as isit

pause = 1
row_start = 3

time.sleep(pause)
for c in col:
    content_list = []
    values = []
    count = 0
    start = row_start
    while True:
        content = []
        cell_info = ''
        position = c + str(start+count)
        element_pos.send_keys(Keys.CONTROL+"a")
        driver.implicitly_wait(pause)
        element_pos.send_keys(Keys.DELETE)
        driver.implicitly_wait(pause)
        element_pos.send_keys(position, Keys.ENTER)
        driver.implicitly_wait(pause)
        element_pos.send_keys(Keys.ESCAPE)
        driver.implicitly_wait(pause)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.select_one('#m_excelWebRenderer_ewaCtl_readoutElement1')
        cont_tag = soup.select_one('#formulaBarTextDivId > div').contents
        # print('tag = ', tag)
        if 'aria-label' not in tag.attrs and (start+count) != row_start:
            continue
        elif 'aria-label' in tag.attrs:
            cell_info = tag['aria-label']
        # print('여기까지 됨', position)
        # print(tag)
        if not isit.position_check(tag.attrs, cell_info, c, start+count):
            continue

        content = [i.text for i in cont_tag]
        # print(content, '\n')
        content_list.append(content)
        count += 1
        if (start+count) == limit:
            break

        time.sleep(0.1)
    result[c] = content_list







#    result[c] = values

# 코드 실행할 때, 이미 클릭되어 있는 다른 셀 주소의 정보가 가져와지는거 방지하기
# 셀에 하이퍼링크로 추가정보 연결되어있을 때 '내부링크. ~' 같은 형식으로 내용에 같이 적혀있는데 이거 잘라내기
# 그리고 A column 정보 가져오기 결과가
# ['전라도 김치 혐오. 내부 링크. 전김!"A" 1', '2022.11.21', 'A5', 'A5', '', 'A8', 'A8', 'A8', 'A8', 'A8', 'A8', 'A8', 'A15', '', '2023.4.11', '2023.4.11', '', 'A20', '2023.4.18', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.19', '2023.4.28', '2023.4.28', '2023.4.28', '2023.4.28', '2023.4.28', '2023.5.13', '2023.5.13', '', 'A37', 'A37', 'A37', 'A37', 'A37', 'A37', 'A37', 'A44', 'A44', 'A44', '2023.06.12', '', 'A49', '2023.06.13', '2023.06.13', '2023.06.13', '2023.06.13', '', 'A55', 'A55', 'A55', '2023.06.18', '2023.06.18', '2023.06.18', '2023.06.18', '2023.06.18']
# 이와 같은데 문제 파악하고 수정하기




time.sleep(1)
for c in col:
    print(result[c])


# 파일에 작성
# A : occ_date
# B : occ_time
# C : person
# D : subject
# E : content
# total.txt : 전체 내용 작성

txt_file_name = ['occ_date', 'occ_time', 'person', 'subject', 'content']
for i in range(len(txt_file_name)):
    name = txt_file_name[i] + '.txt'
    dict_key = col[i]
    with open(name, 'w', encoding='utf-8') as f:
        f.write(str(result[dict_key]))




