import os
import datetime
import xml.dom.minidom

from wand.image import Image


def get_xml_value(path, tag_name):
    dom = xml.dom.minidom.parse(path)
    # 得到文档对象
    root = dom.documentElement
    tag = root.getElementsByTagName(tag_name)
    return tag[0].childNodes[0].data


BASE = os.getcwd()
PDF_PATH = BASE + '\\assert\\code_calendar.pdf[{}]'  # PDF路径
CONFIG_PATH = BASE + '\\_config.xml'  # 配置文件路径
WALLPAPERS_DIR = get_xml_value(CONFIG_PATH, 'wallpaper_dir')  # 壁纸目录
OUTPUT_DIR = get_xml_value(CONFIG_PATH, 'wallpaper_out')  # 输出壁纸目录
WALLPAPER_WIDTH = int(get_xml_value(CONFIG_PATH, 'wallpaper_width'))  # 壁纸最小宽度
WALLPAPER_HEIGHT = int(get_xml_value(CONFIG_PATH, 'wallpaper_height'))  # 壁纸最小高度

PAGE_OFFSET_WEEK = 6  # PDF文档中星期开始页数
PAGE_OFFSET_MONTH = 0  # PDF文档月数开始页数

files = os.listdir(WALLPAPERS_DIR)
wallpapers = []
# 过滤不满足条件的路径
for file in files:
    with Image(filename=WALLPAPERS_DIR + file) as tempImage:
        if tempImage.height >= WALLPAPER_HEIGHT and tempImage.width >= WALLPAPER_WIDTH:
            wallpapers.append(file)
LENS = len(wallpapers)
if LENS <= 0:
    print('No image available...')
    exit(0)
print('Find ' + str(LENS) + ' wallpapers...')

current_week = datetime.datetime.now().isocalendar()[1]
current_month = datetime.datetime.now().month + 1
page_week = PAGE_OFFSET_WEEK + current_week  # 计算星期数所在页数
page_month = PAGE_OFFSET_MONTH + current_month // 2  # 计算月份应该在那一页

with Image(filename=PDF_PATH.format(page_week), resolution=200) as week:
    with Image(filename=PDF_PATH.format(page_month), resolution=200) as month:
        for temp in wallpapers:
            print(temp)
            with Image(filename=WALLPAPERS_DIR + temp) as background:
                # 重设pdf大小为适应屏幕
                week.resize(week.width * WALLPAPER_HEIGHT // week.height, WALLPAPER_HEIGHT)
                month.resize(month.width * WALLPAPER_HEIGHT // month.height, WALLPAPER_HEIGHT)
                # 重设背景图大小为适应屏幕
                background.resize(background.width * WALLPAPER_HEIGHT // background.height,
                                  WALLPAPER_HEIGHT)
                MARGIN_LEFT_MONTH = background.width - month.width
                background.composite_channel('default_channels', week, 'blend', 0, 0)
                background.composite_channel('default_channels', month, 'blend', MARGIN_LEFT_MONTH,
                                             0)
                background.save(filename=OUTPUT_DIR + temp)
