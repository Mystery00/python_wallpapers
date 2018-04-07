import xml.dom.minidom


def get_xml_value(path, tag_name):
    dom = xml.dom.minidom.parse(path)
    # 得到文档对象
    root = dom.documentElement
    tag = root.getElementsByTagName(tag_name)
    return tag[0].childNodes[0].data
