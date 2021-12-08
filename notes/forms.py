from django import forms
from django.utils.timezone import now

from .models import Note


class NoteCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)
    expires_at = forms.DateTimeField(input_formats=['%d-%m-%Y %H:%M:%S'], required=False)

    class Meta:
        model = Note
        fields = [
            'title',
            'content',
            'allowed_reads',
            'display_confirmation',
            'expires_at'
        ]

    def clean_allowed_reads(self):
        allowed_reads = self.cleaned_data['allowed_reads']
        if allowed_reads < 1:
            self.add_error('allowed_reads', 'Allowed reads cannot be less than 1')
        return allowed_reads

    def clean_expires_at(self):
        expires_at = self.cleaned_data['expires_at']
        if expires_at and expires_at < now():
            self.add_error('expires_at', 'Expires at should be after current time')

        return expires_at

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password2 = cleaned_data['password2']

        if password and password != password2:
            self.add_error('password2', 'Password do not match')

        return cleaned_data
