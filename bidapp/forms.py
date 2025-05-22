from django import forms

class ExcelProcessorMainForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        }),
        help_text="仅支持上传 (.xlsx or .xls)"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_groups = []

    def add_num_group(self, num_value, ranges):
        self.num_groups.append({
            'num_value': num_value,
            'ranges': ranges
        })

class NumRangeForm(forms.Form):
    start = forms.FloatField(required=True)
    end = forms.FloatField(required=True)
    min_value = forms.FloatField(required=True)
    max_value = forms.FloatField(required=True)

class NumGroupForm(forms.Form):
    num_value = forms.FloatField(required=True)
    reduc = forms.FloatField(
        required=True,
        min_value=0.0,
        max_value=10.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'max': '10',
            'placeholder': 0.95
        })
    )


