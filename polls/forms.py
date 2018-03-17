"""Modelos de los formularios"""

from django import forms
from .models import Question, Choice
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionForm(forms.Form):
    # id = forms.IntegerField(widget=forms.HiddenInput())
    question_text = forms.CharField(widget = forms.TextInput)
    pub_date = forms.DateField(widget=forms.SelectDateWidget)



class ChoiceForm(forms.Form):
    question = forms.CharField()
    choice_text = forms.CharField()


class EditarForm(forms.ModelForm):
    class Meta:
        model= Question
        fields = ['question_text', 'pub_date']


#falta la funcion def()
# class QuestionForm(forms.Form):
#     question_text = forms.CharField()
#     pub_date = forms.DateTimeField()

#     def postea_pregunta(self):
#         pass

class IngresarForm(forms.Form):
    usuario = forms.CharField()
    contraseña = forms.CharField(widget = forms.PasswordInput)

class RegistrarForm(forms.Form):
    usuario = forms.CharField()
    email = forms.EmailField()
    contraseña = forms.CharField(widget = forms.PasswordInput)
    contraseña2 = forms.CharField(label ="Confirme contraseña", widget = forms.PasswordInput)
    
    def clean_usuario(self):
        usuario = self.cleaned_data.get('Usuario')
        qs = User.objects.filter(usuario=usuario)
        if qs.exists():
            raise forms.ValidationError("Usuario ya registrado")
        return usuario

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Mail ya registrado")
        return email

    def clean(self):
        data = self.cleaned_data
        contraseña = self.cleaned_data.get('contraseña')
        contraseña2 = self.cleaned_data.get('contraseña2')
        if contraseña2 != contraseña:
            raise forms.ValidationError("Las contraseñas deben coincidir")
        return data