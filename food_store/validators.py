from django.core.exceptions import ValidationError

def validate_integers(value): 
    if value.isdigit() == False:
        raise ValidationError('Accepts numbers only.')


def validate_file_size(file):
    max_size_kb = 1024

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size_kb / 1024}MB!')