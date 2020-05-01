import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import email.encoders as encoders


class ExEmail(object):
    """ 腾讯企业邮箱发邮件封装"""
    def __init__(self):
        self.user = None
        self.passwd = None
        self.to_list = []
        self.cc_list = []
        self.tag = None
        self.body = None
        self.doc = None
        # 正文类型, 默认为plain
        self.subtype = 'plain'

    def send(self):
        """
        发送邮件
        """
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
        server.login(self.user, self.passwd)
        server.sendmail("<%s>" % self.user, self.to_list+self.cc_list, self.get_attach())
        server.close()

    def get_attach(self):
        """
        构造邮件内容
        """
        attach = MIMEMultipart()
        attach["Accept-Language"] = "zh-CN"
        attach["Accept-Charset"] = "ISO-8859-1,utf-8"
        if self.tag is not None:
            # 主题,最上面的一行
            attach["Subject"] = self.tag
        if self.body:
            body = MIMEText(self.body, _subtype=self.subtype, _charset='utf-8')
            attach.attach(body)
        if self.user is not None:
            # 显示在发件人
            attach["From"] = "<%s>" % self.user
        if self.to_list:
            # 收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            # 抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            # 估计任何文件都可以用base64，比如rar等
            # 文件名汉字用gbk编码代替
            for doc in self.doc:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(doc, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', os.path.basename(doc)))
                attach.attach(part)
        return attach.as_string()

    def send_email(self, to_list, cc_list, tag=None, body=None, doc=None, subtype=None):
        """ 发邮件"""
        self.to_list = to_list
        self.cc_list = cc_list
        self.subtype = subtype
        if tag is not None:
            self.tag = tag
            if doc is None:
                pass
            else:
                self.doc = [doc, ]
        else:
            out_dir = doc.split(os.sep)[-1]
            self.tag = out_dir.split('.')[0]
            self.doc = [doc, ]

        self.body = body
        self.send()
