#!/usr/bin/env python
from django.db import models
from yaml import *
from django.core.validators import ValidationError

def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """
    class Meta:
        pass

    if app_label:
        setattr(Meta, 'app_label', app_label)

    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    attrs = {'__module__': module, 'Meta': Meta}

    if fields:
        attrs.update(fields)

    model = type(name, (models.Model,), attrs)

    return model

def build_class_from_yaml(path):
    classes_list = []
    yaml_model = file(path,'r')
    for class_name, class_data in load(yaml_model).iteritems():
        fields_list = []
        field_dict = {}
        class_dict = {}
        for obj in class_data['fields']:
            if obj['type'] == 'int':
                field_dict[obj['id']] = models.IntegerField()
            if obj['type'] == 'char':
                field_dict[obj['id']] = models.TextField(max_length=30)
            if obj['type'] == 'date':
                field_dict[obj['id']] = models.DateField()
        class_dict[class_name] = field_dict
        classes_list.append(class_dict)
    return classes_list


