import os
import glob

bigdata = open(r"E:\\上市公司数据\\年份—利润表数据.txt", "w+")

all_name = glob.glob(r"E:\\上市公司数据\\上市公司年度报表\\[0-9]*_benefit_year.txt")
gg = 1
for path in all_name:
    file_path = path
    print(file_path)
    scode = os.path.basename(os.path.realpath(file_path)).split("_")[0]
    # print(scode)
    gg += 1
    # print(gg)
    print('已完成：%s' % str(gg/3652))
    with open(file_path) as con:
        info_list = con.read().split("\n")

    # 日期纬度
    period_list = info_list[0].split("[")[-1].replace("]", "").split(",")

    for each in range(1, len(info_list)):
        #     print (info_list[each])

        #     项目纬度
        if len(info_list[each]) > 1:
            each_01 = info_list[each].replace("]", "").split("[")
            dw_name = each_01[-2].split(",")[0]
            fact_data = each_01[-1].split(",")

            for i in range(0, len(period_list)):
                name_date = (scode + "-" + dw_name + "-" + period_list[i] + "-" + fact_data[i]).replace("'", "")
                # print(name_date)
                bigdata.write(name_date + "\n" )

bigdata.close()
