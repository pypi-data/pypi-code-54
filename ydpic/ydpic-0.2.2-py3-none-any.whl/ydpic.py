import argparse
import os
import shutil
import sys
from urllib import parse

from PIL import ImageGrab
from prutils.pr_requests import downloadfile
from prutils.pr_utils import make_path_by_relfile

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), '..')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prutils.pr_string import rand_hex32, replace_chinese

from ydpic.config import Config
from ydpic.yd_note import YoudaoNote, CONFIG_TPL_PATH


def link_resourceId_func(img_file_path):
    # 有道对中文url支持有问题,将中文替换成"_"
    img_file_path = replace_chinese("_", img_file_path)
    return (os.path.basename(img_file_path).split(".", 1)[0] \
            + "_" + rand_hex32())


def default_resourceId_func(img_file_path):
    return "WEBRESOURCE" + rand_hex32()


def init_tmp_dir(args):
    if args.tmp_dir is None:
        args.tmp_dir = make_path_by_relfile(args.config_file_path, "tmp")
    if not os.path.exists(args.tmp_dir):
        os.makedirs(args.tmp_dir)


def downlad_img(url, img_path):
    r = parse.urlsplit(url)
    if r.scheme in ["http", "https"]:
        file_path = img_path
        downloadfile(url, file_path)
        url = file_path
    return url


def save_clip_img(img_path):
    pic = ImageGrab.grabclipboard()
    pic.save(img_path)


def foramt_img_urls(output_format, urls):
    if output_format == "markdown":
        format_urls = map(lambda url: "![]({})".format(url), urls)
        output = "\n".join(format_urls)
    elif output_format == "typora":
        output = '''
        Upload Success:
        {}
        '''.format("\n".join(urls))
    elif output_format == "raw":
        output = "\n".join(urls)
    return output


def _upload(args, conf):
    # 创建功能对象
    ydn = YoudaoNote(conf.tuku_note_url, conf.share_url, conf.session_file,
                     conf.username, conf.password, conf.proxy, args.tmp_dir)

    # 可选使用自己定义的resourceId
    if conf.link_resourceId:
        resourceId_func = link_resourceId_func
    else:
        resourceId_func = default_resourceId_func

    urls = ydn.process(args.files, resourceId_func)

    print(foramt_img_urls(args.output_format, urls))

def upload(args):
    init_tmp_dir(args)
    conf = Config(args.config_file_path)
    _upload(args, conf)


def upload_clip(args):
    init_tmp_dir(args)
    conf = Config(args.config_file_path)
    img_path = make_path_by_relfile(conf.session_file, rand_hex32()[24:] + ".png")
    save_clip_img(img_path)
    args.files = [img_path]
    _upload(args, conf)





def init(args):
    shutil.copy(CONFIG_TPL_PATH, args.output_file)


def add_common_param(parser):
    parser.add_argument("-c --config", dest="config_file_path", help="config file path.",
                        default=os.path.join(".", "config.ini"))

    parser.add_argument("-f --format", dest="output_format", help="img output format.",
                        choices=["raw", "typora", "markdown"], default="typora")

    parser.add_argument("-t --tmp_dir", dest="tmp_dir", help="tmp_dir.", default=None)


def main():
    # test()
    parser = argparse.ArgumentParser(description='上传图片到有道云笔记，返回指定格式的图片地址.')
    if sys.version_info >= (3, 7):
        subparsers = parser.add_subparsers(dest="cmd", required=True)
    else:
        subparsers = parser.add_subparsers(dest="cmd")
    parser_upload = subparsers.add_parser('upload')
    add_common_param(parser_upload)

    parser_upload.add_argument(dest="files", nargs='+', help='image files')
    parser_upload.set_defaults(func=upload)

    parser_new_config = subparsers.add_parser('init')
    parser_new_config.add_argument("-o", dest="output_file", default="config.ini")
    parser_new_config.set_defaults(func=init)

    parser_upload_clip = subparsers.add_parser('upload_clip')
    add_common_param(parser_upload_clip)
    parser_upload_clip.set_defaults(func=upload_clip)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
