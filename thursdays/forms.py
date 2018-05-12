from django import forms
from .models import Company, Thursday


class ThursdayForm(forms.ModelForm):
    pmm_date = forms.ModelChoiceField(
        queryset=Thursday.objects.filter(assigned_company__isnull=True).filter(is_currently_available=True),
        widget=forms.Select(attrs={'class': 'form-control',
                                   'id': 'inputDate'}), )

    class Meta:
        model = Company
        fields = ('name', 'website', 'facebook', 'description',
                  'email_one', 'email_two', 'pmm_date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Company Name',
                                           'id': 'inputName'}),
            'website': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Website',
                                              'id': 'inputWebsite'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Facebook',
                                               'id': 'inputFacebook'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Description',
                                                 'id': 'inputDescription'}),
            'email_one': forms.EmailInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Email one',
                                                 'id': 'inputEmailOne'}),
            'email_two': forms.EmailInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Email two',
                                                 'id': 'inputEmailTwo'}),
        }

    def clean(self):
        cleaned_data = super(ThursdayForm, self).clean()
        email_one = cleaned_data.get('email_one')
        email_two = cleaned_data.get('email_two')

        if email_two:
            if email_one == email_two:
                raise forms.ValidationError('Emails Cannot be the Same')

        return cleaned_data


class UpdateThursdayForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'website', 'facebook', 'description',
                  'email_one', 'email_two', 'pmm_date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Company Name',
                                           'id': 'inputName'}),
            'website': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Website',
                                              'id': 'inputWebsite'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Facebook',
                                               'id': 'inputFacebook'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Description',
                                                 'id': 'inputDescription'}),
            'email_one': forms.EmailInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Email one',
                                                 'id': 'inputEmailOne'}),
            'email_two': forms.EmailInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Email two',
                                                 'id': 'inputEmailTwo'}),
            'pmm_date': forms.Select(attrs={'class': 'form-control',
                                            'id': 'inputDate'})

        }


class CreateThursdayForm(forms.ModelForm):
    class Meta:
        model = Thursday
        fields = ('date',)
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control date-input',
                                           'placeholder': 'Enter a date',
                                           'id': 'inputDate'}),
        }

    def __init__(self, *args, **kwargs):
        extra = []
        if 'extra' in kwargs:
            extra = kwargs.pop('extra')

        # super call required so the non-dynamic fields are filled
        super(CreateThursdayForm, self).__init__(*args, **kwargs)

        # iterate through extra dates and add them to this class' fields as DateField objects
        for i, date in enumerate(extra):
            if date != '':
                self.fields['date_%s' % i] = forms.DateField()

    # Returns a tuple of the field object and its value
    def extra_dates(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('date_'):
                yield (self.fields[name], value)
