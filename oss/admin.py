from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Submission)
admin.site.register(Submission_Files)
admin.site.register(Article_Type)
admin.site.register(Article_Status)
admin.site.register(Category)
admin.site.register(Decision)
admin.site.register(File_Category)
admin.site.register(Journal)
admin.site.register(Journal_Editor_Assignment)
admin.site.register(Keyword)
admin.site.register(Accepted_Submission)