from django import forms


#user password change form
class ChangePasswordForm(forms.Form):
    old_pass = forms.CharField(label='Enter your old password', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Your Old Password", 'required':'True'}))
    new_pass = forms.CharField(label='Enter your new password', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Your New password", 'required':'True'}))
    repert_new_pass = forms.CharField(label='Enter Repert your new password', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Your Repert New password", 'required':'True'}))



