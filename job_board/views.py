from django.shortcuts import render, get_object_or_404

from .models import JobPosting
from job_board.jobs import get_data_frame


# Create your views here.
def index(request):

       
    JobPosting.objects.all().delete()
    # Convert dynamic data into DataFrame
    df = get_data_frame()
    
    # Create model instances from the DataFrame
    instances = [JobPosting(title=row['title'], description=row['description'], link=row['link']) for _, row in df.iterrows()]
    
    # Bulk insert into the database
    JobPosting.objects.bulk_create(instances)
    
            
    active_postings = JobPosting.objects.all()
    context = {
        'job_postings': active_postings
    }

    return render(request, 'job_board/index.html', context)

def job_detail(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    context = {
                'posting' : job_posting
            }
    return render(request, 'job_board/detail.html', context)