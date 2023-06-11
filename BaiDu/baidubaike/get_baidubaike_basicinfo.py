

def get_basicInfo(response_data):
    basicinfo = {}
    # 获得dd/dt的个数，转成整数类型
    basicinfo_left_count = response_data.xpath(
        "count(//dl[@class='basicInfo-block basicInfo-left']/dt[@class='basicInfo-item name'])")
    basicinfo_right_count = response_data.xpath(
        "count(//dl[@class='basicInfo-block basicInfo-right']/dt[@class='basicInfo-item name'])")
    left_num = int(basicinfo_left_count)
    right_num = int(basicinfo_right_count)
    # 左侧数据
    for i in range(1, left_num + 1):
        name = response_data.xpath(
            "//dl[@class='basicInfo-block basicInfo-left']/dt[@class='basicInfo-item name'][" + str(i) + "]/text()")[0]
        name = name.replace("\xa0", "")
        value = response_data.xpath(
            "//dl[@class='basicInfo-block basicInfo-left']/dd[@class='basicInfo-item value'][" + str(i) + "]//text()")
        value = " ".join(value).replace("\n", "")
        print(name, value)
        basicinfo.update({name: value})

    # 右侧数据
    for i in range(1, right_num + 1):
        name = response_data.xpath(
            "//dl[@class='basicInfo-block basicInfo-right']/dt[@class='basicInfo-item name'][" + str(i) + "]/text()")[0]
        name = name.replace("\xa0", "")
        value = response_data.xpath(
            "//dl[@class='basicInfo-block basicInfo-right']/dd[@class='basicInfo-item value'][" + str(i) + "]//text()")
        value = " ".join(value).replace("\n", "")
        print(name, value)
        basicinfo.update({name: value})

    return basicinfo