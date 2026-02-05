from selenium import webdriver, common
from selenium.webdriver.common.by import By
import os
import time
import datetime
os.chdir("D:\\R\\Crawler") # 设置工作目录
# os.system("start explorer D:\\R\\Crawler") # 打开工作目录

driver = webdriver.Chrome() # 创建Chrome WebDriver对象并定义为driver
driver.maximize_window() # 窗口最大化
driver.set_page_load_timeout(30)  # 设置页面加载超时时间为30秒
driver.implicitly_wait(30) # 设置隐式等待时间为30秒


## 打开JCR网页 -----------------------------------------------------

url = 'https://jcr.clarivate.com/jcr/browse-journals' # 设置网页地址
driver.get(url) # 打开上述网页
time.sleep(10) # 强制等候10秒以等待网页加载
# 点击接受所有协议
driver.find_element(By.CSS_SELECTOR, "#mat-mdc-checkbox-1-input").click()
driver.find_element(By.CSS_SELECTOR, "#mat-mdc-checkbox-2-input").click()
driver.find_element(By.CSS_SELECTOR, "#mat-mdc-dialog-0 > div > div > cross-border-data-acknowledgement > div:nth-child(3) > button:nth-child(2)").click()
time.sleep(5)
# 点击接受所有Cookies
driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()

driver.quit() # 关闭WebDriver对象


## 按条件筛选期刊 --------------------------------------------------

# 不按条件筛选期刊可跳过此步。

### 定位并打开期刊筛选器Filter -----------------------

# 定位目标元素"Filter"的父元素
icon_filter_up = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-root > div.ng-star-inserted > div > div > div.row.mr-0.ml-0.bottom-space > div.col-sm-1.col-md-1.col-lg-1.filter-col-pad > div > section')
# 进而定位目标元素"Filter"
icon_filter = icon_filter_up.find_element(By.CSS_SELECTOR, '#initial > mat-sidenav-content > div > mat-icon')
# 点击目标元素"Filter"
icon_filter.click()

### 指定筛选条件 -------------------------------------

# 定位并打开期刊类别Categories菜单
icon_category_up = icon_filter_up.find_element(By.CSS_SELECTOR, '#collapsed > div > div > section.accordion-section')
icon_category = icon_category_up.find_element(By.ID, 'panel-2')
icon_category.click()

# 利用循环语句勾选特定类别
search_area = icon_filter_up.find_element(By.CSS_SELECTOR, '#expandedCategories > div > div > section.accordion-section').find_element(By.ID, 'panel-2').find_element(By.CSS_SELECTOR, '#cdk-accordion-child-27 > div > section > div')

# 建立cate_array数组，手动放置特定期刊类别所对应的元素ID。利用浏览器开发人员工具从定位的元素代码中获取。
cate_array = [27, 28, 29, 30, 31, 39, 46, 47, 48, 49, 50, 51, 55, 56, 61, 71, 85, 99, 100, 105, 108, 109, 110, 114, 119, 120, 122, 123, 126, 127, 130, 137, 150, 185, 186, 190, 192, 193, 198, 220, 223, 224, 238, 232, 242, 245, 248, 255, 259, 260, 262, 268, 277]

# 创建空列表以用于后续每个类别对应的元素文字的暂时储存
labels_text = []

# 循环点击类别元素，同时储存其名称
for i in range(len(cate_array)):
    area_label = search_area.find_element(By.CSS_SELECTOR, '#mat-checkbox-' + str(cate_array[i]) + ' > label')
    labels_text.append(area_label.text)
    area_label.click()
pass

# 定义txt用于导出所筛选的期刊类别名称
output_file = 'Categories_Filtered.txt'
# 除非单独指定位置，不然创建/导出的文件储存在工作目录下。

# 将类别名称写入txt文件
with open(output_file, 'w', encoding = 'utf-8') as file:
    for text in labels_text:
        file.write(text + '\n')
pass

# 点击apply按钮进行筛选
icon_apply = icon_filter_up.find_element(By.CSS_SELECTOR, '#expandedCategories > div > div > section.btn-section > button.mat-focus-indicator.cdx-but-md.apply-btn-style.pull-right.mat-flat-button.mat-button-base')
icon_apply.click()


## 设置期刊列表页显示的期刊数目 ------------------------------------

# 设置每页显示的期刊数目为200个

Itemspp = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-root > div.ng-star-inserted > div > div > div.row.mr-0.ml-0.bottom-space > div.col-sm-11.col-md-11.col-lg-11.pr-36.ng-star-inserted > div > section.paginate-section > div > div.col-sm-6.col-md-6.col-lg-6.p-0.ng-star-inserted > mat-paginator > div > div > div.mat-paginator-page-size.ng-star-inserted > mat-form-field > div > div:nth-child(1) > div > mat-select')
driver.execute_script('arguments[0].click();', Itemspp) # 该代码使用JavaScript在浏览器中执行点击操作，可以无视浏览器滑动滚动条位置。

time.sleep(2)

Itemspp200 = driver.find_element(By.CSS_SELECTOR, 'body > div.cdk-overlay-container > div.cdk-overlay-connected-position-bounding-box > div > div > div > mat-option:nth-child(5)')
driver.execute_script('arguments[0].click();', Itemspp200)


## 打开期刊详情页并爬取信息 ----------------------------------------

### 设置列表页的期刊爬取数目与起始页码 ---------------

# 生成期刊选择器数组
element_selectors = [
    f'body > div.incites-jcr3-fe-root > div.ng-star-inserted > div > div > div.row.mr-0.ml-0.bottom-space > div.col-sm-11.col-md-11.col-lg-11.pr-36.ng-star-inserted > div > section.table-section > mat-table > mat-row:nth-child({i}) > mat-cell.mat-cell.cdk-cell.cdk-column-journalName.mat-column-journalName.ng-star-inserted > span'
    for i in range(2, 202) # 计划爬取期刊列表中的第1-200个
]

# 定位下一页按钮位置
next_page_button = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-root > div.ng-star-inserted > div > div > div.row.mr-0.ml-0.bottom-space > div.col-sm-11.col-md-11.col-lg-11.pr-36.ng-star-inserted > div > section.paginate-section > div > div.col-sm-6.col-md-6.col-lg-6.p-0.ng-star-inserted > mat-paginator > div > div > div.mat-paginator-range-actions > button.mat-focus-indicator.mat-tooltip-trigger.mat-paginator-navigation-next.mat-icon-button.mat-button-base')

page = 1 # 设置期刊列表页起始页码

# 将期刊列表页切换到上述页码
for _ in range(page - 1):
    driver.execute_script('arguments[0].click();', next_page_button)
    time.sleep(2)
pass

# total_journals = 0 # 设置起始总期刊数目
total_journals = (page - 1) * len(element_selectors)

### 期刊信息爬取 -------------------------------------

# 设定导出文件夹
output_path = 'JCRoutput'

if not os.path.exists(output_path):
    os.makedirs(output_path)
    print("文件夹创建成功")
else:
    print("文件夹已存在")
pass

# 利用循环语句爬取期刊信息
while True:
    # 建立空文档用于保存信息
    output_file = os.path.join(output_path, f'journal_info_page_{page}.txt')
    # 以可读模式打开新建的文档
    with open(output_file, 'w') as file:
        for index, selector in enumerate(element_selectors, start=1):
            # 强制切换到第一个标签页（期刊列表页）
            tabs = driver.window_handles # 获取浏览器已打开的网页标签
            driver.switch_to.window(tabs[0])
            
            # 点击期刊选择器数组中的元素
            journal_element = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script('arguments[0].click();', journal_element)
            # 切换到最后一个/最新的标签（期刊详情页）
            tabs = driver.window_handles
            driver.switch_to.window(tabs[-1])
            # 设置2秒后超时
            driver.set_page_load_timeout(2)
            try:
                driver.get(driver.current_url) # 重新加载当前URL，但会在2秒后停止
            except:
                print("页面加载超时，继续执行提取操作")
            pass
            # 恢复默认超时
            driver.set_page_load_timeout(30)
            
            # 提取期刊信息
            summary_tile = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-journal-profile-page-root > div.incites-jcr3-fe-journal-profile.ng-star-inserted').find_element(By.CSS_SELECTOR, '#main-content > div.col-sm-6.col-md-6.col-lg-6.summary-tile')
            journal_information = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-journal-profile-page-root > div.incites-jcr3-fe-journal-profile.ng-star-inserted').find_element(By.CSS_SELECTOR, 'div:nth-child(4) > div > div:nth-child(2) > div:nth-child(6)')
            # 获取期刊名
            journal_title = summary_tile.find_element(By.CSS_SELECTOR, 'p.title').text
            # 获取期刊JCR缩写
            jcr_abbreviation = summary_tile.find_element(By.CSS_SELECTOR, 'div > div:nth-child(3) > p.content-text').text
            # 获取期刊ISO缩写
            iso_abbreviation = summary_tile.find_element(By.CSS_SELECTOR, 'div > div:nth-child(4) > p.content-text').text
            # iso_abbreviation = summary_tile.find_elements(By.CLASS_NAME, 'item')[3].find_element(By.CSS_SELECTOR, 'p.content-text').text
            # 删掉ISO缩写中的句点
            iso_without_period = iso_abbreviation.replace(".", "")
            # 获取期刊语言
            languages = journal_information.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > p.info-tile-p-text.mb-36.ng-star-inserted').text
            # 获取期刊地区
            region = journal_information.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > p.region-publisher-text.info-tile-p-text.mb-36').text
            # 获取期刊1st Electronic JCR Year
            electronic_jcr_year = journal_information.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > p.info-tile-p-text.mb-36').text
            
            # 将期刊信息写入打开的文档中
            file.write(f"{journal_title}\t{iso_abbreviation}\t{iso_without_period}\t{jcr_abbreviation}\t{languages}\t{region}\t{electronic_jcr_year}\n")
            # 实时打印爬取进度
            print(f"Total Journal Num: {total_journals + index}, Page: {page}, Journal Num: {index}, Journal Name: {journal_title}", datetime.datetime.now())
            
            # 关掉期刊详情页
            driver.close()
            tabs = driver.window_handles
            driver.switch_to.window(tabs[0]) # 切回期刊列表页
        pass
        
        # 进入下一页期刊列表
        driver.execute_script('arguments[0].click();', next_page_button)
        time.sleep(2)
        
        # 在完成指定页码信息提取后停止爬取流程
        if page == 112:
            break
        pass
        
        page += 1
        total_journals += len(element_selectors)
    pass
pass


## 期刊信息合并与提取 ----------------------------------------------

import os
os.chdir("D:\\R\\Crawler") # 指定工作目录
output_path = 'JCRoutput' # 指定所提取的期刊信息原文件所在文件夹

file_list = sorted([file for file in os.listdir(output_path) if file.endswith('.txt')]) # 建立output_path中的所有txt文件的列表，并按文件名进行排序

merged_text = '' # 创建一个空字符串用于存储合并后的文本

# 循环遍历文件列表，依次读取每个txt文件的内容并添加到合并后的文本中
for file_name in file_list:
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'r') as file:
        merged_text += file.read()
pass

# 过滤掉空行和不符合格式的行
valid_lines = [line for line in merged_text.split('\n') if line.strip() and '\t' in line]

# 对有效行进行排序。按第一列（即期刊名称）的字母顺序进行排序，不考虑大小写
sorted_lines = sorted(valid_lines, key=lambda line: line.split('\t')[0].lower())

# 重新组合排序后的行并用换行符连接
sorted_text = '\n'.join(sorted_lines)

# 将合并后的文本写入新文件中
output_file1 = 'output_merged.txt' # 所有提取信息的储存文件名
with open(output_file1, 'w') as file:
    file.write(sorted_text)
pass

# 提取第1、2、4列的内容，分别对应期刊名称、ISO缩写和JCR缩写
extracted_lines = []
for line in sorted_text.split('\n'):
    columns = line.split('\t')
    if len(columns) >= 4:  # 确保列表至少有4个元素
        extracted_lines.append([columns[0], columns[1], columns[3]])
pass

extracted_text = '\n'.join(['\t'.join(line) for line in extracted_lines])

# 将提取的文本写入新文件中
output_file2 = 'output_merged_extracted.txt' # 进一步精简的储存文件名
with open(output_file2, 'w') as file:
    file.write(extracted_text)
pass
