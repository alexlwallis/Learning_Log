from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta: #nested class tells it to build off of forms module
        model = Topic #build from Topic
        fields = ['text'] #include just text field
        labels = {'text': ''} # Do not create a label for the text field

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})} #the area to write text is now larger