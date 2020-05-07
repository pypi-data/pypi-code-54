# -*- coding: utf-8 -*-
import pytest

from zwpdf.pdf import Pdf

@pytest.mark.parametrize(
    't, pth, result', (
        (0, 'data/test/《政策预期差》系列篇七：土地改革是下一个突破口吗-20191226-国泰君安-10页.pdf', ('title','《政策预期差》系列篇七：土地改革是下一个突破口吗')),
        (1, 'data/test/巴克莱-美股-投资策略-宏观策略：数据显示市场热情尚未被激发-2019.12.10-33页.pdf', ('title', '宏观策略：数据显示市场热情尚未被激发')),
    )
)
def test_meta_from_filename(t, pth, result):
    p = Pdf(pth)
    if t == 0:
        r = r'(.+)-(\d+)-(.+)-(\d+)页'
        arr = ['title', 'pub_date', 'source', 'pages']
    elif t == 1:
        r = r'(.+)-(.+)-(.+)-(.+)-(.+)-(\d+)页'
        arr = ['source', 'cate', 'subcate', 'title', 'pub_date', 'pages']
    r = p.meta_from_filename(r, arr)
    assert r[result[0]] == result[1]