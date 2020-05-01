from django import forms
from mdeditor.widgets import MarkdownWidget


class MDeditorTestForm(forms.Form):
    text1 = forms.CharField()
    text2 = forms.CharField()
   

    def __init__(self, *args, **kwargs):
        super(MDeditorTestForm, self).__init__(*args, **kwargs)
        self.fields['text1'].widget = MarkdownWidget()
        self.fields['text2'].widget = MarkdownWidget()       
