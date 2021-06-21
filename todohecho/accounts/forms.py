import re
from django import forms
from django.forms import ModelForm
from django.forms.widgets import EmailInput, PasswordInput
from .models import Account, get_profile_image_filepath
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password

# Create forms


class RegisterForm(ModelForm):
    email = forms.EmailField(widget=EmailInput, help_text="Ese mail no es correcto!")
    username = forms.CharField(max_length=60)
    password1 = forms.CharField(widget=PasswordInput)
    password2 = forms.CharField(widget=PasswordInput)
    password_mismatch = "¡Las contraseñas no coinciden!"
    password_length = "La contraseña es muy corta"
    password_characters = "La contraseña debe incluir al menos una letra y un número"
    
    class Meta:
        model = Account
        fields = ['email','username','password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'El mail {email} ya está siendo usado. ¿Olvidaste tu contraseña?')
    
    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f'El usuario {username} ya está siendo usado. ¿Olvidaste tu contraseña?')
    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        # Validaciones

        #Longitud contraseña
        if len(password1)<8: 
            raise forms.ValidationError(
                self.password_length
            )

        if not re.search('[a-z]',password1):
            raise forms.ValidationError(
                self.password_characters
            )

        if not re.search('[0-9]',password1):
            raise forms.ValidationError(
                self.password_characters
            )

        #Contraseñas coinciden
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.password_mismatch
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class LoginForm(ModelForm):
    email = forms.EmailField(label="email", widget=EmailInput)
    password = forms.CharField(label="password", widget=PasswordInput)

    class Meta:
        model = Account
        fields = ['email','password']

    # def clean_email(self):
    #     if self.is_valid():
    #         email = self.cleaned_data.get('email')

    #     try:
    #         account = Account.objects.get(email != email)
    #     except Exception as e:
    #         return email
    #     raise forms.ValidationError(f'El mail {email} no está registrado')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Combinación de email/contraseña incorrecta")
            

class ChangePassword(ModelForm):
    old_password = forms.CharField(label="old_password", widget=PasswordInput)                
    password1 = forms.CharField(label="new_password1", widget=PasswordInput)                
    password2 = forms.CharField(label="new_password2", widget=PasswordInput)                

    class Meta:
        model = Account
        fields = ['old_password','password1', 'password2']

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        check = Account.objects.get['password']
        if old_password != check:
            raise forms.ValidationError("La contraseña actual es incorrecta")
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super(ChangePassword, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class ChangeImage(ModelForm):
    class Meta:
        model = Account
        fields = ('profile_image',)

    
