from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import csv
import urllib.parse
import logging

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ตั้งค่า Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_argument("--headless")  # เปิดถ้าต้องการไม่ให้เปิด browser

driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
wait = WebDriverWait(driver, 20)

def wait_for_page_load(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(3)
        return True
    except Exception as e:
        logger.error(f"❌ Error while waiting for page load: {e}")
        return False

def find_search_box(driver):
    selectors = [
        "input[type='search']",
        "input[name*='search']",
        "input[placeholder*='ค้นหา']",
        "input[class*='search']",
        "input[id*='search']",
        "input"
    ]
    for selector in selectors:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            if element.is_displayed() and element.is_enabled():
                return element
        except:
            continue
    return None

def make_absolute_url(url, base_url):
    if url.startswith('http'):
        return url
    return urllib.parse.urljoin(base_url, url)

def extract_course_info(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    course_links = []
    links = soup.find_all("a", href=True)
    for link in links:
        text = link.get_text(strip=True)
        if "วิศวกรรมคอมพิวเตอร์" in text or "วิศวกรรมปัญญาประดิษฐ์" in text:
            course_links.append({
                'url': link['href'],
                'title': text,
                'type': 'link_text'
            })
    return course_links

def extract_university_name(soup):
    university_name = ""

    # วิธีที่ 1: ลิงก์ /universities/
    try:
        links = soup.find_all('a', href=re.compile(r'/universities/\d+'))
        for link in links:
            text = link.get_text(strip=True)
            if any(k in text for k in ['มหาวิทยาลัย', 'วิทยาลัย', 'สถาบัน', 'University', 'College']):
                university_name = text
                break
    except:
        pass

    # วิธีที่ 2: selectors
    if not university_name:
        try:
            selectors = [
                'h1', 'h2', 'h3', '.university', '.school', '.institution',
                '[class*="university"]', '[class*="school"]', '[id*="university"]',
                '.college', '[class*="college"]', '.univ', '[class*="univ"]'
            ]
            for selector in selectors:
                elements = soup.select(selector)
                for elem in elements:
                    text = elem.get_text(strip=True)
                    if any(k in text for k in ['มหาวิทยาลัย', 'วิทยาลัย', 'สถาบัน', 'University', 'College']):
                        if not any(c in text for c in ['วิศวกรรม', 'Engineering', 'หลักสูตร']):
                            university_name = text
                            break
                if university_name:
                    break
        except:
            pass

    # วิธีที่ 3: breadcrumbs
    if not university_name:
        try:
            breadcrumbs = soup.find_all(['nav', 'ol', 'ul'], class_=re.compile(r'breadcrumb|nav', re.I))
            for bc in breadcrumbs:
                links = bc.find_all('a')
                for link in links:
                    text = link.get_text(strip=True)
                    if any(k in text for k in ['มหาวิทยาลัย', 'วิทยาลัย', 'สถาบัน']):
                        university_name = text
                        break
                if university_name:
                    break
        except:
            pass

    # วิธีที่ 4: regex
    if not university_name:
        try:
            text = soup.get_text()
            patterns = [
                r'(มหาวิทยาลัย[^\n\r:]{1,60})',
                r'(วิทยาลัย[^\n\r:]{1,60})',
                r'(สถาบัน[^\n\r:]{1,60})',
                r'([A-Z][a-z]+ University)',
                r'([A-Z][a-z]+ College)',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    university_name = min(matches, key=len).strip()
                    break
        except:
            pass

    return university_name

def extract_detail_from_course(url):
    driver.get(url)
    wait_for_page_load(driver)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    university = extract_university_name(soup)

    # ชื่อหลักสูตร
    course_name = ""
    try:
        h1 = soup.find('h1')
        if h1:
            course_name = h1.get_text(strip=True)
    except:
        pass

    # ชื่อหลักสูตรภาษาอังกฤษ
    course_name_eng = ""
    try:
        eng_tag = soup.find(text=re.compile(r'หลักสูตรภาษาอังกฤษ|ชื่อหลักสูตรภาษาอังกฤษ'))
        if eng_tag and eng_tag.find_parent():
            course_name_eng = eng_tag.find_parent().find_next_sibling().get_text(strip=True)
    except:
        pass

    # ค่าใช้จ่าย
    fee = ""
    try:
        dt_tags = soup.find_all('dt')
        for dt in dt_tags:
            if any(k in dt.get_text() for k in ['ค่าใช้จ่าย', 'ค่าเล่าเรียน', 'อัตราค่าเล่าเรียน']):
                dd = dt.find_next_sibling('dd')
                if dd:
                    fee = dd.get_text(strip=True)
                    break
    except:
        pass

    return {
        'url': url,
        'มหาวิทยาลัย': university,
        'ค่าใช้จ่าย': fee,
        'ชื่อหลักสูตร': course_name,
        'ชื่อหลักสูตรภาษาอังกฤษ': course_name_eng
    }

def search_and_extract(driver, keyword):
    logger.info(f"\n🔍 Searching: {keyword}")
    driver.get("https://course.mytcas.com/")
    wait_for_page_load(driver)

    search_box = find_search_box(driver)
    if not search_box:
        logger.warning("❌ Search box not found")
        return []

    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    wait_for_page_load(driver)
    time.sleep(3)
    return extract_course_info(driver)

def main():
    keywords = ["วิศวกรรมคอมพิวเตอร์", "วิศวกรรมปัญญาประดิษฐ์"]
    all_course_data = []

    for keyword in keywords:
        course_links = search_and_extract(driver, keyword)
        for course in course_links:
            absolute_url = make_absolute_url(course['url'], "https://course.mytcas.com/")
            try:
                detailed_info = extract_detail_from_course(absolute_url)
                detailed_info['url'] = absolute_url
                all_course_data.append(detailed_info)
                logger.info(f"✅ Extracted course: {detailed_info['ชื่อหลักสูตร']}")

                # 👉 แจ้งเตือนเมื่อเจอมหาวิทยาลัยที่ขึ้นต้นด้วย "สถาบัน" (แต่ไม่หยุด)
                if detailed_info['มหาวิทยาลัย'].strip().startswith("สถาบัน"):
                    logger.info(f"🛑 พบมหาวิทยาลัยขึ้นต้นด้วย 'สถาบัน': {detailed_info['มหาวิทยาลัย']}")

            except Exception as e:
                logger.warning(f"❌ Failed to extract from {absolute_url}: {e}")
            time.sleep(2)

    # เขียนลง CSV
    if all_course_data:
        with open("perfect.csv", "w", newline='', encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'มหาวิทยาลัย', 'ค่าใช้จ่าย', 'ชื่อหลักสูตร', 'ชื่อหลักสูตรภาษาอังกฤษ'])
            writer.writeheader()
            writer.writerows(all_course_data)
        logger.info("💾 Data saved to perfect.csv")
    else:
        logger.warning("⚠️ No course data found")

    driver.quit()


if __name__ == "__main__":
    main()
