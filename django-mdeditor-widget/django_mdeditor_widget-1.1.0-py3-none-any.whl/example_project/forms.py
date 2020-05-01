from django import forms
from mdeditor.widgets import MDeditorWidget


class MDeditorTestForm(forms.Form):
    text1 = forms.CharField()
    text2 = forms.CharField()
   
    def __init__(self, *args, **kwargs):
        super(MDeditorTestForm, self).__init__(*args, **kwargs)
        self.fields['text1'].widget = MDeditorWidget(attrs={'rows': '30', })
        self.fields['text2'].widget = MDeditorWidget()   
