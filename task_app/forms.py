from django import forms
from task_app.models import Task, Folder, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "folder"] 
        widgets = {
            'due_date': forms.DateInput(attrs={
                "class": "form-control transparent-input",
                "placeholder" : "Date",
                "type": "date"
            })
        }
    def __init__(self, *args, **kwargs):
        current_folder = kwargs.pop('current_folder', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if current_folder:
            self.fields['folder'].initial = current_folder
        
        self.fields['title'].widget.attrs.update({
            "class": "form-control noborder-input title-input",
            "placeholder" : "Title"
        })

        self.fields['description'].widget.attrs.update({
            "class": "form-control noborder-input content-input",
            "placeholder" : "Content"
        })

       
    

        self.fields['priority'].widget.attrs.update({
            "class": "form-control transparent-input",
            "placeholder" : "Priority"
            
        })

        

        

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name", "color"]
    def __init__(self, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)
        
            
        self.fields['name'].widget.attrs.update({
            "class": "form-control noborder-input content-input",
            "placeholder" : "Name"
        })

        self.fields['color'].widget.attrs.update({
            "class": "form-control transparent-input",
            "placeholder" : "Color"
            
        })




class SinginForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields = ("first_name", "last_name", "email", "username")
        
            

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'media']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                
            }),
            'media': forms.ClearableFileInput(attrs={
                'class': 'form-control', 
            })
        }




            
                 


class TaskFilterForm(forms.Form):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
                ]
        
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label="Priority")

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields['priority'].widget.attrs.update({"class": "form-select"})

   
    