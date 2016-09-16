from django import forms

class SubscriptionForm(forms.Form):
    name = forms.CharField(label='NOME')
    cpf = forms.CharField(label='CPF')
    email = forms.EmailField(label='EMAIL')
    phone = forms.CharField(label='TELEFONE')