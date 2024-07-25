from django.db import models
from account.models import Author,Editor
from django.contrib.auth.models import User

class Journal(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

class Category(models.Model):
    catagory =models.CharField(max_length=50)
    
    def __str__(self):
        return self.catagory
    
class Article_Type(models.Model):
    article_type = models.CharField(max_length=50)
    article_description = models.CharField(max_length=255)

    def __str__(self):
        return self.article_type

class Article_Status(models.Model):
    article_status = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.article_status
    
class Specialization(models.Model):
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return self.specialization

class Decision(models.Model):
    decision = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.decision

class File_Category(models.Model):
    file_category = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.file_category
    
class Request_Status(models.Model):
    request_status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.request_status
    
class Reviewer_Specialization(models.Model):
    reviewer = models.ForeignKey(Author, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.author.user.username} - {self.specialization.specialization}'
 
class Submission(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    manuscript_id = models.CharField(max_length=255, null=True, blank=True)
    article_type = models.ForeignKey(Article_Type, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    is_funded = models.BooleanField(null=True, blank=True)
    no_of_figures = models.IntegerField(null=True, blank=True)
    no_of_tables = models.IntegerField(null=True, blank=True)
    no_of_words = models.IntegerField(null=True, blank=True)
    is_submitted_already = models.BooleanField(null=True, blank=True)
    acknowledgement_1 = models.BooleanField(default=False)
    acknowledgement_2 = models.BooleanField(default=False)
    acknowledgement_3 = models.BooleanField(default=False)
    conflict_of_interest = models.BooleanField(null=True, blank=True)
    coi_describe = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    cover_letter = models.TextField( null=True, blank=True)   #upload_to='submissions/',
    parent_submission = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='patent_submissions')
    submitted_on = models.DateField(auto_now_add=True, null=True, blank=True)
    decissioned_on = models.DateField(auto_now_add=True,null=True, blank=True)
    article_status = models.ForeignKey(Article_Status, on_delete=models.CASCADE, null=True, blank=True)
    is_decissioned = models.BooleanField(default=False)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, null=True, blank=True)
    final_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    admin_commments = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title or "No Title"


class Submission_Files(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    file_category = models.ForeignKey(File_Category, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    file_size = models.FloatField()

    def __str__(self):
        return f"{self.submission.title} - {self.file.name}"

class Submission_Reviewer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Author, on_delete=models.CASCADE)
    assigned_on = models.DateTimeField(auto_now_add=True)
    completion_on = models.DateTimeField(null=True, blank=True)
    accepted_on = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    request_status = models.ForeignKey(Request_Status, on_delete=models.CASCADE)
    REVIEW_RECOMMENDATION_CHOICES = [
        ('A', 'Accept'),
        ('R', 'Reject'),
        ('MIN_R', 'Minimum Revision'),
        ('MAJ_R', 'Major Revision'),
    ]
    review_recommendation = models.CharField(max_length=5, choices=REVIEW_RECOMMENDATION_CHOICES)
    review_comments = models.TextField()

    def __str__(self):
        return f"{self.submission.title} reviewed by {self.reviewer.user.username}"

class Reviewer_Invitation(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    expiring_date = models.DateField()

    def __str__(self):
        return f'Reviewer: {self.name} ({self.email}), Submission: {self.submission.title}'

class Communication(models.Model):
    title = models.CharField(max_length=255, null=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciever")
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    detail = models.TextField(blank=True)
    file = models.FileField(upload_to='communications/', blank=True, null=True)
    submission = models.ForeignKey(Submission , on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class AE_Assingment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True,null=True, blank=True)
    REVIEW_RECOMMENDATION_CHOICES = [
        ('A', 'Accept'),
        ('R', 'Reject'),
        ('MIN_R', 'Minimum Revision'),
        ('MAJ_R', 'Major Revision'),
    ]
    ae_recommendation = models.CharField(max_length=5, choices=REVIEW_RECOMMENDATION_CHOICES)
    ae_comments = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.submission}"
    
class Journal_Editor_Assignment(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.journal} - {self.editor}"
    

class Funder(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    grant_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class CoAuthor(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(max_length=255,null=True, blank=True)
    institution = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=225) 

    def __str__(self):
        return self.keyword