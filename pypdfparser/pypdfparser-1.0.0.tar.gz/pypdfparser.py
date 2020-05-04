# -*- coding: utf-8 -*-
from pdfminer.layout import LTImage
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator


def parser_text_layout(layout):
    """
    从LTTextBoxHorizontal中解析出文本.
    参数列表
    ----------
    layout : pdfminer.layout.LTTextBoxHorizontal 

    Returns
    -------
    texts : str list
        多行文本数组.
    """
    texts = []
    # 获取所有的文本
    text = layout.get_text()                
    # 按照换行符切割文本为一行行的数组
    for _text in text.split('\n'):
        if len(_text)>0:
            # 把一行的文本，去除空格后
            # 保存到结果数组中
            texts.append(
                _text.strip().replace(' ', '')
            )
    return texts


def get_text_layouts(layout):
    """
    深度遍历查找LTTextBoxHorizontal.

    参数列表
    ----------
    layout : pdfminer.layout.XXXXX 

    Returns
    -------
    layouts : LTTextBoxHorizontal list
        LTTextBoxHorizontal 列表.
    """
    layouts = []
    if isinstance(layout, LTTextBoxHorizontal):
        layouts.append(layout)
    else:
        try:
            for _layout in layout:
                layouts.extend(
                    get_text_layouts(_layout)
                )
        except:
            pass
    return layouts


def get_img_layouts(layout):
    """
    深度遍历查找 LTImage.
    
    参数列表
    ----------
    layout : pdfminer.layout.XXXXX         

    Returns
    -------
    layouts : LTImage list
        LTImage 列表.
    """
    layouts = []
    if isinstance(layout, LTImage):
        layouts.append(layout)
    else:
        try:
            for _layout in layout:
                layouts.extend(
                    get_img_layouts(_layout)
                )
        except:
            pass
    return layouts


def join_texts(texts):
    """
    合并文本

    Parameters
    ----------
    texts : str list
        文本数组.

    Returns
    -------
    str
        合并后的文本.

    """
    len_stat = {}
    for text in texts:
        l = len(text)
        if l in len_stat:
            len_stat[l] = len_stat[l] + 1
        else:
            len_stat[l] = 1
    
    max_freq_len = max(
        len_stat, key=len_stat.get
    )
    r_texts = []
    tmps = []
    for text in texts:
        if len(text)>=max_freq_len:
            tmps.append(text)
        else:
            tmps.append(text)
            r_texts.append("".join(tmps))
            tmps = []    
    return '\r\n'.join(r_texts)


def create_device(pdf_file):
    """
    创建解析 PDF 文档需要的设备对象
    Parameters
    ----------
    pdf_file : TYPE
        DESCRIPTION.

    Returns
    -------
    doc : TYPE
        DESCRIPTION.
    device : TYPE
        DESCRIPTION.
    interpreter : TYPE
        DESCRIPTION.

    """
    # 用文件对象创建一个 PDF 文档分析器
    parser = PDFParser(pdf_file)
    #创建一个PDF文档
    doc = PDFDocument(parser)
    
    # 创建 PDF 资源管理器
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    # 创建一个PDF设备对象
    device = PDFPageAggregator(
        rsrcmgr, 
        laparams=laparams
    )
    # 创建一个PDF解释其对象
    interpreter = PDFPageInterpreter(
        rsrcmgr, device
    )
    return doc, device, interpreter


def parser_text(pdf_file_path):
    """
    根据输入的 PDF 文档路径，解析 PDF 文档，得到文本

    Parameters
    ----------
    pdf_file_path : TYPE
        PDF 文档路径.

    Returns
    -------
    str
        文档文本.
    """
    # 打开PDF文档，得到 PDF 文件对象
    fp = open(pdf_file_path,'rb')
    # 创建 PDF 解析对象
    doc, device, interpreter = create_device(fp)
    
    # 用来保存结果的文本数组
    texts = []

    # 循环遍历列表，每次处理一个page内容
    for page in PDFPage.create_pages(doc):
        # 使用 PDF 解析器解析页面
        interpreter.process_page(page)
        # 获取整个 PDF 页面的布局
        layouts = device.get_result()
        # 获取该布局下，所有的文本
        for layout in layouts:
            # 解析出所有的文本框
            text_layouts = get_text_layouts(layout)
            for _layout in text_layouts:
                # 把文本框解析出来，追加到结果中
                texts.extend(
                    parser_text_layout(_layout)
                )
    fp.close()    
    return join_texts(texts)


def parser_img(pdf_file_path):
    """
    根据输入的 PDF 文件路径，解析 PDF 文档，得到图像

    Parameters
    ----------
    pdf_file_path : str
        PDF 文档路径.

    Returns
    -------
    imgs : raw data list
        图像列表.

    """
    # 打开PDF文档，得到 PDF 文件对象
    fp = open(pdf_file_path,'rb')
    # 创建 PDF 解析对象
    doc, device, interpreter = create_device(fp)
    
    # 用来保存结果的图片数组  
    imgs = []
    
    # 循环遍历列表，每次处理一个 page 内容
    for page in PDFPage.create_pages(doc):
        # 使用 PDF 解析器解析页面
        interpreter.process_page(page)
        # 获取整个PDF页面的布局
        layouts = device.get_result()
        
        for layout in layouts:
            # 获取该布局下，所有的图片
            img_layouts = get_img_layouts(layout)
            for _layout in img_layouts:
                #保存图片到图片数组
                imgs.append(_layout.stream.get_rawdata())
    fp.close()
    # 返回图片数组
    return imgs


def parser_img_text(pdf_file_path):
    # 打开PDF文档，得到 PDF 文件对象
    fp = open(pdf_file_path,'rb')
    # 创建 PDF 解析对象
    doc, device, interpreter = create_device(fp)
    
    # 用来保存结果的图片数组  
    imgs = []
    # 用来保存结果的文本数组
    texts = []
    # 循环遍历列表，每次处理一个 page 内容
    for page in PDFPage.create_pages(doc):
        # 使用 PDF 解析器解析页面
        interpreter.process_page(page)
        # 获取整个PDF页面的布局
        layouts = device.get_result()
        
        for layout in layouts:
            # 获取该布局下，所有的图片
            img_layouts = get_img_layouts(layout)
            for _layout in img_layouts:
                #保存图片到图片数组
                imgs.append(_layout.stream.get_rawdata())
            # 追加图片标记位
                texts.append(f"[image_{len(imgs)-1}]")
            # 获取该布局下，所有的文本
            text_layouts = get_text_layouts(layout)
            for _layout in text_layouts:                
                texts.extend(parser_text_layout(_layout))
    fp.close()
    # 返回图片数组
    return imgs, join_texts(texts)

