def get_catalogue(response_data):
    catalogue = {}
    # 获得最后一个div[@class="para-title level-2  J-chapter"]的data-index
    data_index_num = response_data.xpath('//div[@class="main-content J-content"]//div[@class="para-title level-2  J-chapter"][last()]/@data-index')[0]
    for num in range(1, int(data_index_num) + 1):
        start_num = num
        # 目录标题h2
        para_title = response_data.xpath('//div[@class="main-content J-content"]//div[@data-index=' + str(start_num) + ']/h2/text()')[0]
        print(para_title)

        if num == int(data_index_num):
            # 获得两个div标签之间的同级div包含label-module='para'或'para-title'的标签
            para_items = response_data.xpath( "//div[contains(@label-module,'para') or contains(@label-module,'para-title')][preceding-sibling::div[@data-index = " + str(start_num) + "] and following-sibling::div[@id = 'J-main-content-end-dom']]")
        else:
            end_num = num + 1
            # 获得两个div标签之间的同级div包含label-module='para'或'para-title'的标签
            para_items = response_data.xpath("//div[contains(@label-module,'para') or contains(@label-module,'para-title')][preceding-sibling::div[@data-index = " + str(start_num) + "] and following-sibling::div[@data-index = " + str(end_num) + "]]")

        # 用于存储目录标题h2对应的列表
        para_list = ""
        for para_item in para_items:
            if para_item.xpath("./@label-module")[0] == 'para-title':
                listitem = para_item.xpath("./h3/text()")[0] + " : "
            else:
                listitem = para_item.xpath(".//text()")
                listitem = ''.join(listitem).replace("\n", "").replace("\xa0", "") + '\n'
            para_list = para_list + listitem
        catalogue.update({para_title: para_list})

    return catalogue