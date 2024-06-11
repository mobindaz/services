from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def validate_class(form,field):
    validation_class = field.field.widget.attrs.get('class','')
    if hasattr(field.field.widget,'input_type') and field.field.widget.input_type == 'radio':
        pass
    else:
        validation_class = ' '.join([validation_class,'form-control'])
    if form.is_bound:
        if field.errors:
            validation_class = ' '.join([validation_class,'is-invalid'])
        else:
            validation_class = ' '.join([validation_class,'is-valid'])
    return validation_class

@register.filter
def error_class(form,field):
    field_error = ''
    if field.errors:
        for error in field.errors:
            field_error += '<div class="invalid-feedback">'
            field_error += error
            field_error += '</div>'
    return mark_safe(field_error)

@register.filter
def help_text_class(form,field):
    help_text = ''
    if field.help_text:
        field.help_text = field.help_text.replace("!@#$%^&*()[]{};:,./<>?|`-=_+", " ")
        field_help_text += f'<i data-toggle="tooltip" data-placement="top" data-html="true class="fa fa-info data-content={field.help_text}></i>'
    return mark_safe(help_text)

@register.filter
def feeconcession(value):
    if value :
        return 'Eligible'
    else:
        return 'Not Eligible'

@register.filter
def studentactive(value):
    if value :
        return 'Active'
    else:
        return 'Not Active'

@register.filter
def data_verified(value):
    if value :
        return 'Verified'
    else:
        return 'Not Verified'

@register.filter
def tc_issued(value):
    if value :
        return 'Issued'
    else:
        return 'Not Issued'