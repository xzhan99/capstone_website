import pymongo
import urllib

from capstone_website.settings import MONGODB


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
