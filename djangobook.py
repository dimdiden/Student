1. 
------------------------------
At any point in your view, temporarily insert an assert False to trigger the error page. 
------------------------------

1. CONTEXT VARIABLE LOOKUP http://djangobook.com/django-templates/

Similarly, dots also allow access to object attributes. For example, a Python datetime.date object has year, month, and day attributes, and you can use a dot to access those attributes in a Django template:

>>> from django.template import Template, Context
>>> import datetime
>>> d = datetime.date(1993, 5, 2)
>>> d.year
1993
>>> d.month
5
>>> d.day
2
>>> t = Template('The month is {{ date.month }}
and the year is {{ date.year }}.')
>>> c = Context({'date': d})
>>> t.render(c)
'The month is 5 and the year is 1993.'

===========

>>> from django.template import Template, Context
>>> class Person(object):
...     def __init__(self, first_name, last_name):
...         self.first_name, self.last_name =
first_name, last_name
>>> t = Template('Hello, {{ person.first_name }} {{ person.last_name }}.')
>>> c = Context({'person': Person('John', 'Smith')})
>>> t.render(c)
'Hello, John Smit

----------
it’s not possible to pass arguments to the methods; you can only call methods that have no required arguments.
----------
it’s not possible to pass arguments to method calls accessed from within templates.
Data should be calculated in views and then passed to templates for display.
----------
2. 