from django import forms

class SubmissionForm(forms.Form):
    first_name = forms.CharField(max_length=32, label='First Name')
    last_name = forms.CharField(max_length=32, label='Last Name')
    doc = forms.FileField(label='Select any document.')

    def validate_doc(self):
        doc = self.cleaned_data.get('doc')
        if doc:
            allowed_extensions = ['docx', 'pdf', 'odt', 'epub']
            doc_extension = doc.name.split('.')[-1].lower()
            if doc_extension not in allowed_extensions:
                raise forms.ValidationError("Unsupported file type.")
        return doc