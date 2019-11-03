from django.http import JsonResponse
from django.shortcuts import render

from health import mongo

ID_TO_TOPIC = {
    0: 'Others',
    1: 'Symptom',
    2: 'Cause',
    3: 'Treatment'
}

CATEGORY_TO_NAME = {
    0: 'Illness',
    1: 'Symptom',
    2: 'Treatment'
}


def index(request):
    return render(request, 'index.html')


def illness(request):
    ill = request.GET.get('i', 'all')
    return render(request, 'illness.html',
                  context={
                      'illness': ill,
                      # 'data': [],
                      # 'links': [],
                      # 'nodes': [],
                      'start': '2009-01-01',
                      'end': '2019-12-31'
                  })


def update_diagram(request):
    ill = request.GET.get('i', 'all')
    start_date = request.GET.get('s', '2009-01-01')
    end_date = request.GET.get('e', '2019-12-31')

    data, links = mongo.get_nodes_and_relations(ill, start_date, end_date)
    nodes = [{'name': i['name'], 'type_id': i['category'], 'type': CATEGORY_TO_NAME[i['category']]}
             for i in data if i['category'] != 0]

    return JsonResponse({'data': data, 'links': links, 'nodes': nodes})


def list_tweets(request):
    ill = request.GET.get('i')
    tweet_type = request.GET.get('t')
    name = request.GET.get('n')
    start_date = request.GET.get('s')
    end_date = request.GET.get('e')

    tweets = mongo.get_tweets(ill, CATEGORY_TO_NAME[int(tweet_type)], name, start_date, end_date)
    print(tweets)

    return render(request, 'tweet_list.html',
                  context={
                      'illness': ill,
                      'category': CATEGORY_TO_NAME[int(tweet_type)],
                      's': start_date,
                      'e': end_date,
                      'name': name,
                      'list': tweets
                  })
