import datetime

from django import forms
from django.contrib.contenttypes import fields
from django.db.models.base import Model
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput

# from meal.models import Log
#
# class LogForm(ModelForm):
#         class Meta:
#             model=Log
#             fields='__all__'
from meal.models import Log


class LogForm(ModelForm):
    class Meta:
        model = Log
        # fields=['date']
        fields=['eid','date']


    # def clean_date(self):
    #     date = self.cleaned_data['date']
    #     # print(date)
    #     #date = datetime.datetime.now()
    #     # print(date.day)
    #     now = datetime.datetime.now()
    #     # if "fred@example.com" not in date:
    #     #     raise forms.ValidationError("You have forgotten about Fred!")
    #
    #     if date.day==now.day and date.year == now.year and date.month==now.month and now.hour > 10:
    #         #if datetime.datetime.now().time().hour>10:
    #         raise forms.ValidationError("Sorry! You're late :(")
    #     elif date.day<now.day or date.month<now.month or date.year<now.year:
    #         raise forms.ValidationError("Date passed")
    #
    #
    #
    #     return date



class multilogForm(ModelForm):
    class Meta:
        model = Log
        fields=['date']


    def clean_date(self):
        date = self.cleaned_data['date']
        # print(date)
        #date = datetime.datetime.now()
        # print(date.day)
        now = datetime.datetime.now()
        # if "fred@example.com" not in date:
        #     raise forms.ValidationError("You have forgotten about Fred!")

        if date.day==now.day and date.year == now.year and date.month==now.month and now.hour > 10:
            #if datetime.datetime.now().time().hour>10:
            raise forms.ValidationError("Sorry! You're late :(")
        elif date.day<now.day or date.month<now.month or date.year<now.year:
            raise forms.ValidationError("Date passed")



        return date