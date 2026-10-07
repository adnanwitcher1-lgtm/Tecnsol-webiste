from django import forms
from .models import ContactMessage, Service, DownloadLead

INPUT_CLASSES = (
    "w-full bg-darkBg/80 border border-white/10 rounded-xl px-4 py-3 text-sm "
    "text-white focus:outline-none focus:border-maroon-glow transition-colors"
)


class ContactForm(forms.ModelForm):
    service_needed = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        empty_label="General Inquiry / Not Sure Yet",
        widget=forms.Select(attrs={'class': INPUT_CLASSES}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget'].required = False
    



    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'service_needed', 'budget', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'John Doe', 'class': INPUT_CLASSES,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'john@company.com', 'class': INPUT_CLASSES,
            }),
            'budget': forms.Select(attrs={'class': INPUT_CLASSES}),
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about your project goals and timeline...',
                'class': INPUT_CLASSES,
            }),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'service_needed': 'Service / Course Needed',
            'budget': 'Estimated Budget',
            'message': 'Your Message',
        }


class DownloadLeadForm(forms.ModelForm):
    class Meta:
        model = DownloadLead
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'John Doe', 'class': INPUT_CLASSES, 'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '03xx-xxxxxxx', 'class': INPUT_CLASSES, 'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'john@company.com', 'class': INPUT_CLASSES, 'required': True,
            }),
        }
        labels = {
            'name': 'Your Name',
            'phone': 'Phone Number',
            'email': 'Email Address',
        }
