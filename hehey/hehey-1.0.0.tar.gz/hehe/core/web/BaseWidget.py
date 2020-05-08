from hehe.core.web.WebController import WebController
from hehe.helper.ClassHelper import ClassHelper

class BaseWidget(WebController):

    def __init__(self, attrs):

        if attrs:
            ClassHelper.setAttrs(self,attrs)

        return;