R Markdown文档及配套图片（Rmd文件及JCRPicture文件夹，可在Rstudio中查看与编辑）、[Python脚本](Crawler_JCR.py/ "Crawler_JCR.py")（纯代码）、[期刊信息txt文件](Abbreviation_JCR.txt/ "Abbreviation_JCR.txt")（利用本方法于2024/3/9~3/12从JCR网站爬取，包含21762个期刊的名称、ISO缩写和JCR缩写，可直接导入Endnote等期刊管理软件使用）已上传仓库，可按需下载。

本文将介绍利用Python库*Selenium*实现从[Journal Citation Reports](https://jcr.clarivate.com "Journal Citation Reports")网站爬取期刊JCR缩写和ISO缩写的操作步骤，包括网页知识背景、爬虫环境搭建（Python、Selenium、WebDriver的安装与配置）、期刊信息爬取（模拟浏览器操作、元素的定位与抓取、信息的导出与处理）等。

# 网页知识

通过浏览器访问万维网中的某个网站时会从服务器得到一个超文本标记文档，然后浏览器将文档渲染后展示在显示器上，这就是我们得到的页面。页面中可以包含文本、图像、声音、FLASH动画、客户端脚本（JavaScript）和ActiveX控件等，有些页面还可以注册、登录以及显示当前用户的相关信息。爬虫的爬取对象通常就是网页，我们需要对网页有基本的认识。

## 静态网页

静态网页每个网页都有一个固定的URL，且**网页URL以.htm、.html、.shtml等常见形式为后缀**（但不是以这些结尾的网页一定就是静态）；静态网页是实实在在保存在服务器上的文件，每个网页都是一个独立的文件；静态网页的内容相对稳定，因此容易被搜索引擎检索；静态网页没有数据库的支持，在网站制作和维护方面工作量较大，因此当网站信息量很大时完全依靠静态网页制作方式比较困难；静态网页的交互性较差，在功能方面有较大的限制；页面浏览速度迅速，过程无需连接数据库，开启页面速度快于动态页面；减轻了服务器的负担，工作量减少，也就降低了数据库的成本。

## 动态网页

当浏览器请求服务器的某个页面时，服务器根据当前时间、环境参数、数据库操作等动态的生成HTML页面，然后再发送给浏览器（后面的处理跟静态网页一样）。很明显，**动态网页中的“动态”是指服务器端页面的动态生成**，相反，“静态”则指页面是实实在在的、独立的文件。

动态网页一般以数据库技术为基础，可以大大降低网站维护的工作量；采用动态网页技术的网站可以实现更多的功能，如用户注册、用户登录、在线调查、用户管理、订单管理等；动态网页实际上并不是独立存在于服务器上的网页文件，只有当用户请求时服务器才返回一个完整的网页；动态网页的网站在进行搜索引擎推广时需要做一定的技术处理才能适应搜索引擎的要求。

爬取期刊信息所依赖的网页（如Journal Citation Reports网站）通常都是动态网页。

# 爬虫环境搭建

本文旨在利用Python模块*Selenium*爬取动态网页信息。Selenium可以模拟浏览器的点击、滚动、滑动以及文字输入等操作。

## 安装Python

-   从官网下载适合电脑系统的[Python安装包](https://www.python.org/downloads/ "Download Python")。

-   打开Python安装包，勾选 *Add python.exe to PATH* 选项（该选项可自动为Python添加变量环境），进行自定义安装（*Customize installation*）。

![](JCRPicture/1_Python安装_(1).png)

-   可选选项（Optional Features）默认，高级选项（Advanced Options）勾选 *Install for all users*，指定安装路径后，点击 *Install* 安装。

![](JCRPicture/1_Python安装_(2).png)

-   检查Python是否正常安装成功。打开电脑运行命令（快捷键Win+R），输入 `cmd` 并确定运行以打开CMD终端。

![](JCRPicture/1_Python安装_(3).png)

-   在CMD终端依次输入命令 `Python`、`exit()`、`pip show pip` 并分别回车运行。显示如下图样式即安装成功，否则卸载该软件、重启电脑后按上述要求重新安装。

![](JCRPicture/1_Python安装_(4).png)

## 安装Selenium

-   在CMD终端输入命令 `pip install selenium` 回车运行以安装。

-   在CMD终端输入命令 `pip show selenium` 回车运行以查看是否安装成功及版本。

## 安装WebDriver

WebDriver以本地化方式驱动浏览器，是语言绑定和各个浏览器控制代码的实现。

通过WebDriver, Selenium可以支持市场上流行的浏览器, 如Chrome、Firefox、Internet Explorer、Edge、Safari等。除Internet Explorer以外的所有驱动程序实现，都是由浏览器供应商各自提供的, 因此标准Selenium发行版中不包括这些驱动程序，需要用户单独下载，不同浏览器驱动信息可从[Selenium文档的Driver Location](https://www.selenium.dev/zh-cn/documentation/webdriver/troubleshooting/errors/driver_location/#download-the-driver)获取。

![](JCRPicture/2_安装WebDriver_(1).png)

本文以谷歌/Chrome浏览器为例，介绍其驱动ChromeDriver的获取及安装方式。

-   安装Chrome浏览器后，确定Chrome的版本：在浏览器 *设置* - *关于Chrome* 中查看。

![](JCRPicture/2_安装WebDriver_(2).png)

-   从[Chromedriver网站](https://chromedriver.com/ "ChromeDriver - WebDriver for Chrome")下载对应版本的Chromedriver。

![](JCRPicture/2_安装WebDriver_(3).png)

未找到完全一致的版本时，可选择前三位一致的chromedriver下载使用（如此处的 `122.0.6261` 一致即可）。

![](JCRPicture/2_安装WebDriver_(4).png)

-   Chromedriver下载后，解压到Python所在的目录（此步操作可免去额外的Chromedriver环境变量配置）。

![](JCRPicture/2_安装WebDriver_(5).png)

-   测试是否安装成功。在Python中运行下列代码：

```python
from selenium import webdriver
browser = webdriver.Chrome() # 打开浏览器WebDriver并定义为browser
browser.get('https://baidu.com') # 访问百度
browser.quit() # 关闭WebDriver
```

![](JCRPicture/2_安装WebDriver_(6).png)

# 期刊信息抓取

通过[Journal Citation Reports](https://jcr.clarivate.com "Journal Citation Reports")，按条件筛选目标期刊，打开期刊详情页，抓取其JCR缩写、ISO缩写等信息。

## 打开网页

```python
from selenium import webdriver, common
from selenium.webdriver.common.by import By
import os
import time
import datetime
os.chdir("D:\\R\\Crawler") # 设置工作目录
os.system("start explorer D:\\R\\Crawler") # 打开工作目录

driver = webdriver.Chrome() # 创建Chrome WebDriver对象并定义为driver
driver.maximize_window() # 窗口最大化
driver.implicitly_wait(30) # 设置隐性等待时间
```

```python
url = 'https://jcr.clarivate.com/jcr/browse-journals' # 设置网页地址
driver.get(url) # 打开上述网页
time.sleep(2) # 强制等候2秒以等待网页加载
driver.find_element(By.CSS_SELECTOR, 'body').find_element(By.CSS_SELECTOR, '#onetrust-consent-sdk').find_element(By.CSS_SELECTOR, '#onetrust-banner-sdk > div > div.ot-sdk-container > div').find_element(By.CSS_SELECTOR, '#onetrust-button-group-parent').find_element(By.CSS_SELECTOR, '#onetrust-button-group').find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler').click() # 点击接受所有Cookies
```

```python
# 关闭WebDriver对象
driver.quit()
```

## 按条件筛选期刊

不按条件筛选期刊可跳过此步。

### 定位并打开期刊筛选器*Filter*

-   打开浏览器开发人员工具（快捷键F12），查看网页元素对应的代码。

![](JCRPicture/3_网页元素定位_(1).png)

在开发人员工具控制面板的右上角扩展设置中可以调整面板布局。

-   单击控制面板左上角选择按钮以选取目标元素并定位代码位置。之后，在元素所对应的代码上右击，选择 复制 - 复制selector。

![](JCRPicture/3_网页元素定位_(2).png)

-   在Python代码中，通过`driver.find_element(By.CSS_SELECTOR, "value")` 实现目标元素的定位。

应注意，通过浏览器源码复制得到的某些元素的selector可能会比较短，无法直接获取对应的元素。此时，需要先定位其父元素，然后通过其父元素获取目标元素。

如此处的期刊筛选器*Filter*元素，直接复制得到的selector是 `#initial > mat-sidenav-content`，不能直接用于元素选取，因此需要先获取 `#initial` 对应的父元素。

从浏览器代码结构中能够找到目标元素的父元素（及n阶父元素），从下至上依次复制n阶父元素的selector进行观察，其不再包含 `#initial` 的最底一阶父元素的selector即为所需。如此处的 `<section class="browseJournals">` 元素所对应的selecor即不再包含代码 `#initial`。

![](JCRPicture/3_网页元素定位_(3).png)

最终期刊筛选器*Filter*元素的Python定位代码如下：

```python
# 定位目标元素的父元素
icon_filter_up = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-root > div.incites-jcr3-fe-browse-journals.ng-star-inserted > div > div.row.mr-0.ml-0.bottom-space > div.col-sm-1.col-md-1.col-lg-1.filter-col-pad > div > section')
# 进而定位目标元素
icon_filter = icon_filter_up.find_element(By.CSS_SELECTOR, '#initial > mat-sidenav-content')
```

利用 `.click()` 代码单击目标元素以打开期刊筛选器*Filter*。

```python
icon_filter.click()
```

### 指定筛选条件

以按类别*Categories*筛选期刊为例。

```python
# 定位并打开期刊类别Categories菜单
icon_category_up = icon_filter_up.find_element(By.CSS_SELECTOR, '#collapsed > div > div > section.accordion-section')
icon_category = icon_category_up.find_element(By.ID, 'panel-2')
icon_category.click()
```

```python
# 利用循环语句勾选特定类别
search_area = icon_filter_up.find_element(By.CSS_SELECTOR, '#expandedCategories > div > div > section.accordion-section').find_element(By.ID, 'panel-2').find_element(By.CSS_SELECTOR, '#cdk-accordion-child-28 > div > section > div')

# 建立cate_array数组，手动放置特定期刊类别所对应的元素ID。利用浏览器开发人员工具从定位的元素代码中获取。
cate_array = [27, 28, 29, 30, 31, 39, 46, 47, 48, 49, 50, 51, 55, 56, 61, 71, 85, 99, 100, 105, 108, 109, 110, 114, 119, 120, 122, 123, 126, 127, 130, 137, 150, 185, 186, 190, 192, 193, 198, 220, 223, 224, 238, 232, 242, 245, 248, 255, 259, 260, 262, 268, 277]

# 创建空列表以用于后续每个类别对应的元素文字的暂时储存
labels_text = []

# 循环点击类别元素，同时储存其名称
for i in range(len(cate_array)):
  area_label = search_area.find_element(By.CSS_SELECTOR, '#mat-checkbox-' + str(cate_array[i]) + ' > label')
  labels_text.append(area_label.text)
  area_label.click()

# 定义txt用于导出所筛选的期刊类别名称
output_file = 'Categories_Filtered.txt'
# 除非单独指定位置，不然创建/导出的文件储存在工作目录下。

# 将类别名称写入txt文件
with open(output_file, 'w', encoding = 'utf-8') as file:
    for text in labels_text:
        file.write(text + '\n')

```

```python
# 点击apply按钮进行筛选
icon_apply = icon_filter_up.find_element(By.CSS_SELECTOR, '#expandedCategories > div > div > section.btn-section > button.mat-focus-indicator.cdx-but-md.apply-btn-style.pull-right.mat-flat-button.mat-button-base')
icon_apply.click()
```

## 设置期刊列表页显示的期刊数目

设置每页显示的期刊数目为200个。

```python
Itemspp = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-root > div.incites-jcr3-fe-browse-journals.ng-star-inserted > div > div.row.mr-0.ml-0.bottom-space > div.col-sm-11.col-md-11.col-lg-11.pr-36.ng-star-inserted > div > section.paginate-section > div > div.col-sm-6.col-md-6.col-lg-6.p-0.ng-star-inserted > mat-paginator > div > div > div.mat-paginator-page-size.ng-star-inserted > mat-form-field > div > div:nth-child(1) > div > mat-select')
driver.execute_script('arguments[0].click();', Itemspp) # 该代码使用JavaScript在浏览器中执行点击操作，可以无视浏览器滑动滚动条位置。

time.sleep(2)

Itemspp200 = driver.find_element(By.CSS_SELECTOR, 'body > div.cdk-overlay-container > div.cdk-overlay-connected-position-bounding-box > div > div > div > mat-option:nth-child(5)')
driver.execute_script('arguments[0].click();', Itemspp200)
```

## 打开期刊详情页并爬取信息

筛选出需要的期刊后，打开期刊详情页，获取所需信息。

对期刊名的点击操作和前文没有区别。

应注意，计划爬取的期刊数量过多时，期刊通常不能在列表页中一次性全部显示，因此需要进行翻页操作。

### 设置列表页的期刊爬取数目与起始页码

```python
# 生成期刊选择器数组
element_selectors = [
  f'body > div.incites-jcr3-fe-root > div.incites-jcr3-fe-browse-journals.ng-star-inserted > div > div.row.mr-0.ml-0.bottom-space > div.col-sm-11.col-md-11.col-lg-11.pr-36.ng-star-inserted > div > section.table-section > mat-table > mat-row:nth-child({i}) > mat-cell.mat-cell.cdk-cell.cdk-column-journalName.mat-column-journalName.ng-star-inserted.mat-table-sticky > span'
  for i in range(2, 202) # 计划爬取期刊列表中的第1-200个
]

# 定位下一页按钮位置
next_page_button = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-root > div.incites-jcr3-fe-browse-journals.ng-star-inserted > div > div.row.mr-0.ml-0.bottom-space > div.col-sm-11.col-md-11.col-lg-11.pr-36.ng-star-inserted > div > section.paginate-section > div > div.col-sm-6.col-md-6.col-lg-6.p-0.ng-star-inserted > mat-paginator > div > div > div.mat-paginator-range-actions > button.mat-focus-indicator.mat-tooltip-trigger.mat-paginator-navigation-next.mat-icon-button.mat-button-base')

page = 80 # 设置期刊列表页起始页码

# 将期刊列表页切换到上述页码
for _ in range(page - 1):
    driver.execute_script('arguments[0].click();', next_page_button)
    time.sleep(2)
    
# total_journals = 0 # 设置起始总期刊数目
total_journals = (page - 1) * len(element_selectors)
```

### 期刊信息爬取

```python
# 设定导出文件夹
output_path = 'JCRoutput'

if not os.path.exists(output_path):
    os.makedirs(output_path)
    print("文件夹创建成功")
else:
    print("文件夹已存在")

# 利用循环语句爬取期刊信息
while True:
   output_file = os.path.join(output_path, f'journal_info_page_{page}.txt') # 建立空文档用于保存信息
   with open(output_file, 'w') as file: # 以可读模式打开新建的文档
     for index, selector in enumerate(element_selectors, start=1):
       tabs = driver.window_handles # 获取浏览器已打开的网页标签
       driver.switch_to.window(tabs[0]) # 强制切换到第一个标签页/期刊列表页
       journal_element = driver.find_element(By.CSS_SELECTOR, selector)
       driver.execute_script('arguments[0].click();', journal_element) # 点击期刊选择器数组中的元素
       tabs = driver.window_handles
       driver.switch_to.window(tabs[-1]) # 切换到最后一个/最新的标签
       summary_tile = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-journal-profile-page-root > div.incites-jcr3-fe-journal-profile.ng-star-inserted').find_element(By.CSS_SELECTOR, '#main-content > div.col-sm-6.col-md-6.col-lg-6.summary-tile')
       journal_title = summary_tile.find_element(By.CSS_SELECTOR, 'p.title').text # 获取期刊名
       jcr_abbreviation = summary_tile.find_element(By.CSS_SELECTOR, 'div > div:nth-child(3) > p.content-text').text # 获取期刊JCR缩写
       iso_abbreviation = summary_tile.find_element(By.CSS_SELECTOR, 'div > div:nth-child(4) > p.content-text').text # 获取期刊ISO缩写
       # iso_abbreviation = summary_tile.find_elements(By.CLASS_NAME, 'item')[3].find_element(By.CSS_SELECTOR, 'p.content-text').text
       iso_without_period = iso_abbreviation.replace(".", "") # 删掉ISO缩写中的句点
       journal_information = driver.find_element(By.CSS_SELECTOR, 'body > div.incites-jcr3-fe-journal-profile-page-root > div.incites-jcr3-fe-journal-profile.ng-star-inserted').find_element(By.CSS_SELECTOR, 'div:nth-child(4) > div > div:nth-child(2) > div:nth-child(6)')
       languages = journal_information.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > p.info-tile-p-text.mb-36.ng-star-inserted').text # 获取期刊语言
       region = journal_information.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > p.region-publisher-text.info-tile-p-text.mb-36').text # 获取期刊地区
       electronic_jcr_year = journal_information.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > p.info-tile-p-text.mb-36').text # 获取期刊1st Electronic JCR Year
       file.write(f"{journal_title}\t{iso_abbreviation}\t{iso_without_period}\t{jcr_abbreviation}\t{languages}\t{region}\t{electronic_jcr_year}\n") # 将期刊信息写入打开的文档中
       print(f"Total Journal Num: {total_journals + index}, Page: {page}, Journal Num: {index}, Journal Name: {journal_title}", datetime.datetime.now()) # 实时打印爬取进度
       driver.close() # 关掉期刊详情页
       tabs = driver.window_handles
       driver.switch_to.window(tabs[0]) # 切回期刊列表页
    
     # 进入下一页期刊列表
     driver.execute_script('arguments[0].click();', next_page_button)
    
     time.sleep(2)
   
     # 到达指定页码后停止爬取流程
     if page == 109:
         break

     page += 1
     total_journals += len(element_selectors)

```

## 期刊信息合并与提取

```python
file_list = sorted([file for file in os.listdir(output_path) if file.endswith('.txt')]) # 建立output_path中的所有txt文件的列表，并按文件名进行排序

merged_text = '' # 创建一个空字符串用于存储合并后的文本

# 循环遍历文件列表，依次读取每个txt文件的内容并添加到合并后的文本中
for file_name in file_list:
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'r') as file:
        merged_text += file.read()

# 过滤掉空行和不符合格式的行
valid_lines = [line for line in merged_text.split('\n') if line.strip() and '\t' in line]

# 对有效行进行排序。按第一列（即期刊名称）的字母顺序进行排序，不考虑大小写
sorted_lines = sorted(valid_lines, key=lambda line: line.split('\t')[0].lower())

# 重新组合排序后的行并用换行符连接
sorted_text = '\n'.join(sorted_lines)

# 将合并后的文本写入新文件中
output_file1 = 'output_merged.txt'
with open(output_file1, 'w') as file:
    file.write(sorted_text)
    
    
# 提取第1、2、4列的内容，分别对应期刊名称、ISO缩写和JCR缩写
extracted_lines = []
for line in sorted_text.split('\n'):
    columns = line.split('\t')
    if len(columns) >= 4:  # 确保列表至少有4个元素
        extracted_lines.append([columns[0], columns[1], columns[3]])

extracted_text = '\n'.join(['\t'.join(line) for line in extracted_lines])

# 将提取的文本写入新文件中
output_file2 = 'output_merged_extracted.txt'
with open(output_file2, 'w') as file:
    file.write(extracted_text)

```
