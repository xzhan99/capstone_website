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


def get_summary(request):
    ill = request.GET.get('i', 'all')
    start_date = request.GET.get('s', '2009-01-01')
    end_date = request.GET.get('e', '2019-12-31')
    return JsonResponse(mongo.get_summary_counts(ill, start_date, end_date))


def list_tweets(request):
    ill = request.GET.get('i')
    tweet_type = request.GET.get('t')
    name = request.GET.get('n')
    start_date = request.GET.get('s')
    end_date = request.GET.get('e')

    tweets = mongo.get_tweets(ill, CATEGORY_TO_NAME[int(tweet_type)], name, start_date, end_date)

    return render(request, 'tweet_list.html',
                  context={
                      'illness': ill,
                      'category': CATEGORY_TO_NAME[int(tweet_type)],
                      's': start_date,
                      'e': end_date,
                      'name': name,
                      'list': tweets
                  })


def labelled_tweets(request):
    return render(request, 'cfg_tweets.html', context={'type': request.GET.get('t', 'manual')})


def get_labelled_tweets(request):
    label_type = request.GET.get('t', 'manual')
    start = int(request.GET.get('s', 0))
    tweets = mongo.get_cfg_tweets(label_type, start)
    return JsonResponse({'tweets': tweets, 'start': start, 'count': len(tweets)})


def dictionary(request):
    # Pneumonia
    pneumonia = {
        'symptoms': ['fever', 'chills', 'dehydration', 'fatigue', 'loss of appetite', 'malaise', 'clammy skin',
                     'sweating', 'chest pain', 'fast breathing', 'shallow breathing', 'shortness of breath', 'wheezing',
                     'coughing', 'fast heart rate'],
        'treatment': ['antibiotics', 'penicillin', 'supportive care', 'oxygen therapy', 'oral rehydration therapy',
                      'iv']

    }

    # Diabetes
    diabetes = {
        'symptoms': ['excessive thirst', 'frequent urination', 'bedwetting', "fatigue", 'weakness', 'excessive hunger',
                     'weight loss', 'blurred vision', 'having cuts that heal slowly', "itching", "skin infection",
                     'mood swings', 'headache', 'dizziness', 'leg cramps', 'vaginal discharge', 'nausea', 'vomiting',
                     'weight gain', 'recurrent infections', 'numbness in feet', 'numbness in legs', 'tingling feet',
                     'tingling legs'],
        'treatment': ['insulin', 'exercise', 'diet', 'weight reduction', 'weight loss']
    }

    # Common Cold
    common_cold = {
        'symptoms': ['runny nose', 'stuffy nose', 'sore throat', 'cough', 'congestion', 'body aches', 'headache',
                     'sneezing', 'low-grade fever', 'Generally feeling unwell', 'malaise'],
        'treatment': ['Stay hydrated', 'rest', 'warm liquids', 'add moisture to the air', 'cold medications',
                      'cough medication', 'vitamin C', 'echinacea', 'zinc']
    }

    return render(request, 'dictionary.html',
                  context={'pneumonia': pneumonia, 'diabetes': diabetes, 'common_cold': common_cold})
