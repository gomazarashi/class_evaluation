from getpass import getpass
from packaging import version
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from time import sleep


def login(driver, okadai_id, password):
    try:
        element = driver.find_element(By.ID, "username_input")
        element.send_keys(okadai_id)
        element.send_keys(Keys.ENTER)
        sleep(1)
        element = driver.find_element(By.ID, "password_input")
        element.send_keys(password)
        element.send_keys(Keys.ENTER)
        sleep(1)
        if driver.find_elements(By.CLASS_NAME, "error"):
            return -1
        else:
            return 0
    except:
        return -1


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
        try:
            # 授業評価アンケートのページを開く
            driver.find_element(By.CSS_SELECTOR, "#region-main > div:nth-child(2) > div.box.py-3.generalbox.boxaligncenter.boxwidthwide > a").click()
        except:
            pass

        try:
            # 授業評価アンケートのラジオボタンをクリック
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0001").click()
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0004").click()
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0007").click()
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0010").click()
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0013").click()
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0016").click()
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0019").click()
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0022").click()
            driver.find_element(By.CSS_SELECTOR, "#auto-rb0025").click()
            driver.find_element(
                By.CSS_SELECTOR, "#phpesp_response > fieldset:nth-child(14) > div > div.qn-answer > table > tbody > tr.raterow > td:nth-child(6) > input").click()
            driver.find_element(
                By.CSS_SELECTOR, "#phpesp_response > fieldset:nth-child(15) > div > div.qn-answer > table > tbody > tr.raterow > td:nth-child(6) > input").click()
            sleep(5)
            driver.find_element(By.CSS_SELECTOR, "#phpesp_response > div.notice > div > div > input[type=submit]:nth-child(2)").click()
        except:
            pass


def main():
    print("入力された情報は授業評価アンケートの回答にのみ使用され、外部に送信されることはありません。\n")

    okadai_id = input("岡大IDを入力してください。\n")
    password = getpass("パスワードを入力してください。(入力中のパスワードは表示されません)\n")
    # 授業の学期を入力
    semester = input("学期を半角数字で入力してください。(例:1学期→1)\n")
    # 授業のコース番号を入力
    course_number_list = []

    if version.parse(webdriver.__version__) < version.parse("4.6.0"):
        driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        driver = webdriver.Chrome()

    driver.get("https://kyomu.adm.okayama-u.ac.jp/Portal/RichTimeOut.aspx")
    driver.find_element(By.ID, "error_lnkLogin_lnk").click()
    if login(driver, okadai_id, password) == -1:
        print("ログインに失敗しました。入力された岡大IDまたはパスワードに誤りがあります。")
        driver.quit()
        return
    else:
        print("ログインに成功しました。")
    course_number_list = get_course_numbers(driver, semester)
    class_evaluation(driver, course_number_list)
    driver.quit()
    print("授業評価アンケートの回答が完了しました。")


if __name__ == "__main__":
    main()
