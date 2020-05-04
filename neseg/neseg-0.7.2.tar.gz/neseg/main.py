import os;
import sys;
import argparse
from neseg import seg,NESEG_VERSION;

def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    parser = argparse.ArgumentParser(description='NESeg: Named Entity Segmentation v{}'.format(NESEG_VERSION))

    parser.add_argument('-n', '--name', required=True, action='store', help='待分割命名实体')
    parser.add_argument('-d', '--dict', required=True, action='store', help='字典路径')
    parser.add_argument('-dn', '--nation', required=False, action='store', default='dict-country.csv', help='字典文件: 国名前缀,默认dict-country.csv')
    parser.add_argument('-dp', '--province', required=False, action='store', default='dict-province.csv', help='字典文件: 省级行政区划,默认dict-province.csv')
    parser.add_argument('-ds', '--city', required=False, action='store', default='dict-city.csv', help='字典文件: 市级行政区划,默认dict-city.csv')
    parser.add_argument('-dx', '--county', required=False, action='store', default='dict-county.csv', help='字典文件: 县级行政区划,默认dict-county.csv')
    parser.add_argument('-db', '--suffix', required=False, action='store', default='dict-suffix.csv', help='字典文件: 机构名称后缀,默认dict-suffix.csv')

    args = parser.parse_args()

    #python main.py -n 中国北京海淀区飞图时代电力科技有限公司 -d dict -dn dict-country.csv -dp dict-province.csv -ds dict-city.csv -dx dict-county.csv -db dict-suffix.csv

    dictDir = args.dict

    dic_country = os.path.join(dictDir,args.nation)  # 国名词典
    dic_province = os.path.join(dictDir,args.province)    # 行政一级词典
    dic_city = os.path.join(dictDir,args.city)    # 行政二级词典
    dic_county = os.path.join(dictDir,args.county)    # 行政三级词典
    dic_suffix = os.path.join(dictDir,args.suffix)    # 核心词后面的部分

    st = args.name
    print(seg.segbydict(st,dic_country,dic_province,dic_city,dic_county,dic_suffix))

if __name__ == "__main__":
    main()