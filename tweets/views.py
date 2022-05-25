import random
# from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
# from django.utils.http import is_safe_url

# from tweetme2.tweetme2.settings import ALLOWED_HOSTS

from .forms import TweetForm
from tweets.models import Tweet

# ALLOWED_HOSTS = settings.ALLOWED_HOSTS 

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    print("next_url", next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.save()
        if request.is_ajax():
            return JsonResponse({}, status=201) # 201 == created items
        if next_url != None: 
            return redirect(next_url)
            """and is_safe_url(next_url, ALLOWED_HOSTS)"""
        form = TweetForm()
    return render(request, 'components/form.html', context={'form': form})

def tweet_list_view(request, *args, **kwargs):
    """ 
    REST API VIEW
    Consume by javascript of Swift/Java/iOS/Andriod
    return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 122)} for x in qs]
    data = {
        "isUser":False,
        "response": tweets_list
    }
    return JsonResponse(data)
    

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """ 
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id = tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status = status) #json.dums content_type='appliction/json'
        