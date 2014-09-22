from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import requires_csrf_token
from datetime import datetime, date, time
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import MySQLdb
from django import forms

mysql_host = 'localhost'
user_table = 'ManagerApp_users'
db_user_name = 'root'
db_password = 'root_password'
class DbManager(object):
    def __init__(self, mysql_host, db_user_name, db_password):
        self.db = MySQLdb.connect(mysql_host, db_user_name, db_password, "PersonalManager", charset = "utf8")
        self.db.set_character_set('utf8')
	self.cursor = self.db.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def save_to_db(self, name, paycheck, date_joined):
        tmp_sql = 'insert into ManagerApp_users '
        sql = tmp_sql + "(name, paycheck, date_joined) values( %s, %s, %s);"
        self.cursor.execute(sql, (str(name), str(paycheck), str(date_joined)))
        self.db.commit()

    def read_db(self, table_name):
        sql = "select * from %s;"%table_name
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update_db(self, table_name, column, new_value, id_):
        sql = "update %s set %s=\'%s\' where id=\'%s\';"%(table_name, column, new_value, id_)
        self.cursor.execute(sql)
        self.db.commit()

class NewUserForm(forms.Form):
    new_user_name = forms.CharField()
    new_user_salary_name = forms.CharField()
    new_user_date_joined_name = forms.CharField()

def get_users_column_name(id_):
    if id_ == 0:
       return 'name'
    if id_ == 1:
       return 'paycheck'
    if id_ == 2:
       return 'date_joined'

@csrf_exempt
def home(request):
    data = ''
    value = ''
    form = NewUserForm(request.POST)
    db = DbManager(mysql_host, db_user_name, db_password)
    if 'add_user' in  request.POST and form.is_valid():
        try:
            new_user_date_joined_name = smart_str(form.cleaned_data['new_user_date_joined_name'])
            new_user_name = smart_str(form.cleaned_data['new_user_name'])
            new_user_salary_name = smart_str(form.cleaned_data['new_user_salary_name'])
            db.save_to_db(new_user_name, new_user_salary_name, new_user_date_joined_name)
        except:
            return HttpResponseRedirect('')
        data = db.read_db(user_table)
        return HttpResponseRedirect('')

    if request.method == 'POST' and request.is_ajax():
        value = str(request.POST['value'])
        if int(request.POST['column']) == 2:
            d = datetime.strptime(str(value), "%d/%m/%Y")
            value = d.strftime('%Y-%m-%d')
        try:
            db.update_db(user_table, get_users_column_name(int(request.POST['column'])), value, request.POST['id'])
        except:
            return  HttpResponseRedirect('')
        data = db.read_db(user_table)
        return render_to_response('index.html',{'data':data}, context_instance=RequestContext(request))

    data = db.read_db(user_table)
    return render_to_response('index.html',{'data':data}, context_instance=RequestContext(request))
