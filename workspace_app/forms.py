from django import forms
from task_app.models import Workspace, Box
from django.contrib.auth.models import User

class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = ["name", "workspace_space", "invite_role"]
    def __init__(self, *args, **kwargs):
        super(WorkspaceForm, self).__init__(*args, **kwargs)
            
        self.fields['name'].widget.attrs.update({
            "class": "form-control noborder-input content-input",
            "placeholder" : "Name"
        })

        self.fields['workspace_space'].widget.attrs.update({
            "class": "form-control transparent-input",
            "placeholder" : "Invite limit"
            
        })

        self.fields['invite_role'].widget.attrs.update({
            "class": "form-control transparent-input",
            "placeholder" : "Inviters roles"
            
        })


class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ["name", "color"]
    def __init__(self, *args, **kwargs):
        super(BoxForm, self).__init__(*args, **kwargs)
            
        self.fields['name'].widget.attrs.update({
            "class": "form-control noborder-input content-input",
            "placeholder" : "Name"
        })

        self.fields['color'].widget.attrs.update({
            "class": "form-control transparent-input",
            "placeholder" : "Color"
            
        })