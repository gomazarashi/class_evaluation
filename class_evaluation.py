from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from time import sleep


def login(driver, okadai_id, password):
    element = driver.find_element(By.ID, "username_input")
    element.send_keys(okadai_id)
    element.send_keys(Keys.ENTER)
    sleep(1)
    element = driver.find_element(By.ID, "password_input")
    element.send_keys(password)
    element.send_keys(Keys.ENTER)
    sleep(1)


def get_course_numbers(driver, semester):
    course_number_list = []
    WEEK_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    driver.find_element(By.CSS_SELECTOR, "#ctl00_bhHeader_ctl18_lnk").click()
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#ctl00_bhHeader_ctl30_lnk").click()
    sleep(1)
    dropdown = driver.find_element(By.CSS_SELECTOR, "#ctl00_phContents_ucRegistTermSelector_ddlTerm")
    select = Select(dropdown)
    select.select_by_index(int(semester)-1)
    for day in WEEK_DAYS:
        for i in range(1, 11):
            try:
                element = driver.find_element(By.CSS_SELECTOR, "#ctl00_phContents_rrMain_ttTable_lct{}{}_ctl00_lblLctCd > a".format(day, i))
                course_number_list.append(element.text)
            except:
                pass
    return list(dict.fromkeys(course_number_list))


def class_evaluation(driver, course_number_list):
    for course_number in course_number_list:
        driver.get("https://moodle.el.okayama-u.ac.jp/course/view.php?idnumber={}".format(course_number))
        try:
            driver.find_element(By.CSS_SELECTOR, ".continuebutton button").click()
        except:
            pass
        sleep(5)
        try:
            driver.find_element(By.CSS_SELECTOR, "#page-course-view-tiles  div.modal-footer > button.btn.btn-primary").click()        
            sleep(5)
        except:
            pass
        try:
            element = driver.find_element(by=By.XPATH, value='//a[contains(., "授業評価アンケート")]')
            url = str(element.get_attribute('href'))
            driver.get(url)
            driver.find_element(By.CSS_SELECTOR, "#section-0 .ouquestionnr a").click()
        except:
            pass
        sleep(5)


def main():
    print("入力された情報は授業評価アンケートの回答にのみ使用され、外部に送信されることはありません。\n")

    okadai_id = input("岡大IDを入力してください。\n")
    password = getpass("パスワードを入力してください。(入力中のパスワードは表示されません)\n")

    # 授業の学期を入力
    semester = input("学期を半角数字で入力してください。(例:1学期→1)\n")
    # 授業のコース番号を入力
    course_number_list = []
    driver = webdriver.Chrome()

    driver.get("https://kyomu.adm.okayama-u.ac.jp/Portal/RichTimeOut.aspx")
    driver.find_element(By.ID, "error_lnkLogin_lnk").click()
    login(driver, okadai_id, password)  # ログイン
    course_number_list = get_course_numbers(driver, semester)
    print(course_number_list)
    class_evaluation(driver, course_number_list)


if __name__ == "__main__":
    main()
