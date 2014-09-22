from django.db import models
from yaml import *
from ModelsBuilder import *
yaml_file_path = 'PersonalManager/ManagerApp/model.yaml'


classes_list = build_class_from_yaml(yaml_file_path)
fields = []
for class_obj in classes_list:
    for class_name, field in class_obj.iteritems():
        create_model(class_name,field, 'ManagerApp', 'ManagerApp')
