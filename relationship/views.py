import urllib

import pymongo
from django.http import JsonResponse
from django.shortcuts import render

from capstone_website.settings import MONGODB

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


class MongoHandler(object):
    client = None
    db = None
    collection = None

    def __init__(self):
        username = urllib.parse.quote_plus(MONGODB['username'])
        password = urllib.parse.quote_plus(MONGODB['password'])
        if username == '' and password == '':
            url = 'mongodb://%s:%d' % (MONGODB['host'], MONGODB['port'])
        else:
            url = 'mongodb://%s:%s@%s:%d' % (username, password, MONGODB['host'], MONGODB['port'])
        self.client = pymongo.MongoClient(url)
        self.db = self.client[MONGODB['db']]
        self.collection = self.db[MONGODB['col']]

    def count_tweets(self, ill, start, end):
        if ill != 'all':
            return self.collection.count({'illness': ill, 'post_date': {'$gte': start, '$lte': end}})
        else:
            return self.collection.count({'post_date': {'$gte': start, '$lte': end}})

    def extract_symptoms(self, ill, start, end):
        return self.collection.aggregate([
            {'$match': {'illness': ill, 'post_date': {'$gte': start, '$lte': end}}},
            {'$project': {'symptoms': 1}},
            {'$match': {'symptoms': {'$exists': True, '$ne': []}}},
            {'$unwind': '$symptoms'},
            {'$group': {'_id': '$symptoms', 'count': {'$sum': 1}}}
        ])

    def extract_treatments(self, ill, start, end):
        return self.collection.aggregate([
            {'$match': {'illness': ill, 'post_date': {'$gte': start, '$lte': end}}},
            {'$project': {'treatments': 1}},
            {'$match': {'treatments': {'$exists': True, '$ne': []}}},
            {'$unwind': '$treatments'},
            {'$group': {'_id': '$treatments', 'count': {'$sum': 1}}}
        ])

    def extract_relations(self, ill, start, end):
        cursor = self.collection.aggregate([
            {'$match': {'illness': ill, 'post_date': {'$gte': start, '$lte': end}}},
            {'$project': {'symptoms': 1, 'treatments': 1}},
            {'$match': {'symptoms': {'$exists': True, '$ne': []}, 'treatments': {'$exists': True, '$ne': []}}},
            {'$unwind': '$symptoms'},
            {'$unwind': '$treatments'},
            {'$group': {'_id': {'symptoms': '$symptoms', 'treatments': '$treatments'}, 'count': {'$sum': 1}}}
        ])
        return [{
            'source': r['_id']['symptoms'],
            'target': r['_id']['treatments'],
            'lineStyle': {'normal': {'width': 1}}
        } for r in cursor]

    def get_nodes_and_relations(self, ill, start='2009-01-01', end='2019-12-31'):
        if ill != 'all':
            ill = ill.replace('_', ' ')
            nodes = [
                {
                    'category': 0,
                    'name': ill,
                    'symbolSize': 15,
                    'value': self.count_tweets(ill, start, end),
                    'draggable': 'true'
                }
            ]
            symptoms = [{'category': 1,
                         'name': s['_id'],
                         'symbolSize': 10,
                         'value': s['count'],
                         'draggable': 'true'
                         } for s in self.extract_symptoms(ill, start, end)]

            treatments = [{'category': 2,
                           'name': t['_id'],
                           'symbolSize': 10,
                           'value': t['count'],
                           'draggable': 'true'
                           } for t in self.extract_treatments(ill, start, end)]

            nodes.extend(symptoms)
            nodes.extend(treatments)

            relations = self.extract_relations(ill, start, end)
            relations.extend(
                [{'source': s['name'], 'target': ill, 'lineStyle': {'normal': {'width': 1}}} for s in symptoms])
            relations.extend(
                [{'source': t['name'], 'target': ill, 'lineStyle': {'normal': {'width': 1}}} for t in treatments])
        else:
            ills = ['pneumonia', 'diabetes', 'common cold', 'cancer']
            # ills = ['pneumonia']
            nodes = [
                {
                    'category': 0,
                    'name': ill,
                    'symbolSize': 15,
                    'value': self.count_tweets(ill, start, end),
                    'draggable': 'true'
                } for ill in ills
            ]
            symptoms, treatments = {}, {}
            relations = []
            for ill in ills:
                ill_symptoms = list(self.extract_symptoms(ill, start, end))
                ill_treatments = list(self.extract_treatments(ill, start, end))
                for s in ill_symptoms:
                    if s['_id'] not in symptoms:
                        symptoms[s['_id']] = {
                            'category': 1,
                            'name': s['_id'],
                            'symbolSize': 10,
                            'value': s['count'],
                            'draggable': 'true'
                        }
                    else:
                        pass
                for t in ill_treatments:
                    if t['_id'] not in treatments:
                        treatments[t['_id']] = {
                            'category': 2,
                            'name': t['_id'],
                            'symbolSize': 10,
                            'value': t['count'],
                            'draggable': 'true'
                        }
                    else:
                        pass
                relations.extend(self.extract_relations(ill, start, end))
                relations.extend(
                    [{'source': s['_id'], 'target': ill, 'lineStyle': {'normal': {'width': 1}}} for s in ill_symptoms])
                relations.extend(
                    [{'source': t['_id'], 'target': ill, 'lineStyle': {'normal': {'width': 1}}} for t in
                     ill_treatments])

            symptoms = [s for s in symptoms.values()]
            treatments = [t for t in treatments.values()]
            nodes.extend(symptoms)
            nodes.extend(treatments)

        return nodes, relations

    def get_tweets(self, ill, t_type, name, start='2009-01-01', end='2019-12-31'):
        if ill != 'all':
            ill = ill.replace('_', ' ')
            if t_type == 'Symptom':
                print({
                    'illness': ill,
                    'post_date': {'$gte': start, '$lte': end},
                    'symptoms': name
                })
                tweets = self.collection.find(
                    {
                        'illness': ill,
                        'post_date': {'$gte': start, '$lte': end},
                        'symptoms': name
                    },
                    {
                        'post_date': 1,
                        'tweet_info.full_text': 1
                    })
                return [{'text': t['tweet_info']['full_text'], 'time': t['post_date']} for t in tweets]
            else:
                tweets = self.collection.find(
                    {
                        'illness': ill,
                        'post_date': {'$gte': start, '$lte': end},
                        'treatments': name
                    },
                    {
                        'post_date': 1,
                        'tweet_info.full_text': 1
                    })
                return [{'text': t['tweet_info']['full_text'], 'time': t['post_date']} for t in tweets]
        else:
            if t_type == 'Symptom':
                tweets = self.collection.find(
                    {
                        'post_date': {'$gte': start, '$lte': end},
                        'symptoms': name
                    },
                    {
                        'post_date': 1,
                        'tweet_info.full_text': 1
                    })
                return [{'text': t['tweet_info']['full_text'], 'time': t['post_date']} for t in tweets]
            else:
                tweets = self.collection.find(
                    {
                        'post_date': {'$gte': start, '$lte': end},
                        'treatments': name
                    },
                    {
                        'post_date': 1,
                        'tweet_info.full_text': 1
                    })
                return [{'text': t['tweet_info']['full_text'], 'time': t['post_date']} for t in tweets]


def close(self):
    self.client.close()


mongo = MongoHandler()


def index(request):
    return render(request, 'index.html')


def illness(request):
    ill = request.GET.get('i', 'all')
    # data, links = mongo.get_nodes_and_relations(ill)
    # nodes = [{'name': i['name'], 'type_id': i['category'], 'type': CATEGORY_TO_NAME[i['category']]}
    #          for i in data if i['category'] != 0]
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
