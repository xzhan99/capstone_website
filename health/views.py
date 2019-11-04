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
    return render(request, 'illness.html', context={'illness': ill, 'start': '2009-01-01', 'end': '2019-12-31'})


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

    return render(request, 'tweet_list.html',
                  context={
                      'illness': ill,
                      'category': CATEGORY_TO_NAME[int(tweet_type)],
                      's': start_date,
                      'e': end_date,
                      'name': name,
                      'list': tweets
                  })


def manual(request):
    return render(request, 'manual.html')


def get_manual_tweets(request):
    start = int(request.GET.get('s', 0))
    tweets = mongo.get_manual_tweets(start)
    return JsonResponse({'tweets': tweets, 'start': start, 'count': len(tweets)})


def dictionary(request):
    # Pneumonia
    p_symptoms = {"fever": 0, "chills": 0, "dehydration": 0, "fatigue": 0, "loss of appetite": 0, "malaise": 0,
                  "clammy skin": 0,
                  "sweating": 0, "chest pain": 0, "fast breathing": 0, "shallow breathing": 0,
                  "shortness of breath": 0,
                  "wheezing": 0, "coughing": 0, "fast heart rate": 0}
    p_treatment = {"antibiotics": 0, "penicillin": 0, "supportive care": 0, "oxygen therapy": 0,
                   "oral rehydration therapy": 0, "iv": 0}

    # Diabetes
    d_symptoms = {"excessive thirst": 0, "frequent urination": 0, "bedwetting": 0, "fatigue": 0, 'weakness': 0,
                  'excessive hunger': 0, 'weight loss': 0, 'blurred vision': 0,
                  'having cuts that heal slowly': 0, "itching": 0, "skin infection": 0, 'mood swings': 0,
                  'headache': 0, 'dizziness': 0, 'leg cramps': 0, 'vaginal discharge': 0,
                  'nausea': 0, 'vomiting': 0, 'weight gain': 0, 'recurrent infections': 0, 'numbness in feet': 0,
                  'numbness in legs': 0, 'tingling feet': 0, 'tingling legs': 0}
    d_treatment = {'insulin': 0, 'exercise': 0, 'diet': 0, 'weight reduction': 0, 'weight loss': 0}

    # Common Cold
    c_symptoms = {"runny nose": 0, "stuffy nose": 0, "sore throat": 0, "cough": 0, "congestion": 0, "body aches": 0,
                  "headache": 0, "sneezing": 0, "low-grade fever": 0, "Generally feeling unwell": 0, "malaise": 0}

    c_treatment = {"Stay hydrated": 0, "rest": 0, "warm liquids": 0, "add moisture to the air": 0,
                   "cold medications": 0, "cough medication": 0, "vitamin C": 0, "echinacea": 0, "zinc": 0}
    pass


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

    return render(request, 'tweet_list.html',
                  context={
                      'illness': ill,
                      'category': CATEGORY_TO_NAME[int(tweet_type)],
                      's': start_date,
                      'e': end_date,
                      'name': name,
                      'list': tweets
                  })


def manual(request):
    return render(request, 'manual.html')


def get_manual_tweets(request):
    start = int(request.GET.get('s', 0))
    tweets = mongo.get_manual_tweets(start)
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
