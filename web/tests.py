from django.test import TestCase

# Create your tests here.


import re

a = "/admin/rbac/permission/"
b = r"/admin/.*"
print(re.match(b, a))
