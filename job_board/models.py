from django.db import models

# Create your models here.

class JobPosting(models.Model):
    # id - starts at 1 and autoincrements
    title = models.CharField(max_length=500)
    description = models.TextField()
    link = models.TextField(default=' exit')
    
    

    '''def __str__(self):
        return f"{self.title} |  {self.company} | {self.is_active}"

'''