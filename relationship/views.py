from django.http import JsonResponse
from django.shortcuts import render

from relationship.data import data, links, new_links, new_data

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
    start_date = '2009-01-01'
    end_date = '9999-12-31'

    nodes = [{'name': i['name'], 'type_id': i['category'], 'type': CATEGORY_TO_NAME[i['category']]}
             for i in data if i['category'] != 0]
    return render(request, 'illness.html',
                  context={
                      'illness': ill,
                      'data': data,
                      'links': links,
                      'nodes': nodes
                  })


def update_diagram(request):
    ill = request.GET.get('i', 'all')
    start_date = request.GET.get('s', '2009-01-01')
    end_date = request.GET.get('e', '9999-12-31')

    # TODO: call identification method

    nodes = [{'name': i['name'], 'type_id': i['category'], 'type': CATEGORY_TO_NAME[i['category']]}
             for i in new_data if i['category'] != 0]
    return JsonResponse({'data': new_data, 'links': new_links, 'nodes': nodes})


def list_tweets(request):
    ill = request.GET.get('i')
    tweet_type = request.GET.get('t')
    name = request.GET.get('n')
    start_date = request.GET.get('s')
    end_date = request.GET.get('e')

    # TODO: fetch tweets from MongoDB

    tweets = [
        {
            'text': 'No one cares. Get bowel cancer. https://t.co/8SGMhJvZdf',
            'time': '2019-01-01',
            'topic': 'Symptoms'
        },
        {
            'text': 'Prime Minister Boris Johnson personally removes the breakfast of a 76-yr-old cancer patient, before returning it to the Treasury. And then somewhere discrete offshore. Britain, 2020. https://t.co/dIPzJDS0IR',
            'time': '2019-01-01',
            'topic': 'Treatments'
        },
        {
            'text': 'Nawaz Sharif &amp; Shehbaz Sharif made Punjab Police into the morally and professionally bankrupt Gullu Butt force over a period spanning 30 years - this cancer will take longer than 1 year to cure.\n',
            'time': '2019-01-01',
            'topic': 'Causes'
        },
        {
            'text': 'No one cares. Get bowel cancer. https://t.co/8SGMhJvZdf',
            'time': '2019-01-01',
            'topic': 'Symptoms'
        },
        {
            'text': 'Prime Minister Boris Johnson personally removes the breakfast of a 76-yr-old cancer patient, before returning it to the Treasury. And then somewhere discrete offshore. Britain, 2020. https://t.co/dIPzJDS0IR',
            'time': '2019-01-01',
            'topic': 'Symptoms'
        },
        {
            'text': 'Nawaz Sharif &amp; Shehbaz Sharif made Punjab Police into the morally and professionally bankrupt Gullu Butt force over a period spanning 30 years - this cancer will take longer than 1 year to cure.\n',
            'time': '2019-01-01',
            'topic': 'Symptoms'
        },
        {
            'text': 'No one cares. Get bowel cancer. https://t.co/8SGMhJvZdf',
            'time': '2019-01-01',
            'topic': 'Others'
        },
        {
            'text': 'Prime Minister Boris Johnson personally removes the breakfast of a 76-yr-old cancer patient, before returning it to the Treasury. And then somewhere discrete offshore. Britain, 2020. https://t.co/dIPzJDS0IR',
            'time': '2019-01-01',
            'topic': 'Symptoms'
        },
        {
            'text': 'Nawaz Sharif &amp; Shehbaz Sharif made Punjab Police into the morally and professionally bankrupt Gullu Butt force over a period spanning 30 years - this cancer will take longer than 1 year to cure.\n',
            'time': '2019-01-01',
            'topic': 'Symptoms'
        },
        {
            'text': 'No one cares. Get bowel cancer. https://t.co/8SGMhJvZdf',
            'time': '2019-01-01',
            'topic': 'Causes'
        },
        {
            'text': 'Prime Minister Boris Johnson personally removes the breakfast of a 76-yr-old cancer patient, before returning it to the Treasury. And then somewhere discrete offshore. Britain, 2020. https://t.co/dIPzJDS0IR',
            'time': '2019-01-01',
            'topic': 'Symptoms'
        },
        {
            'text': 'Nawaz Sharif &amp; Shehbaz Sharif made Punjab Police into the morally and professionally bankrupt Gullu Butt force over a period spanning 30 years - this cancer will take longer than 1 year to cure.\n',
            'time': '2019-01-01',
            'topic': 'Causes'
        },
    ]

    return render(request, 'tweet_list.html',
                  context={
                      'illness': ill,
                      'category': CATEGORY_TO_NAME[int(tweet_type)],
                      's': start_date,
                      'e': end_date,
                      'name': name,
                      'list': tweets
                  })
