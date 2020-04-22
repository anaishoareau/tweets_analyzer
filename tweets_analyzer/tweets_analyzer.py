# -*- coding: utf-8 -*-

"""
Auteurs : Nicolas CALABRESE, Anaïs HOAREAU
Date : 04/2020
"""

""" IMPORTS """

import pandas as pd
import re

from french_preprocessing.french_preprocessing import FrenchPreprocessing
from tweets_analyzer.general_tools import remove_emoji
from french_preprocessing.lexique_tools import LexiqueTools


class TweetsAnalyzer(object):

    def __init__(self, alert_lemma_file_name,
                 alert_lemma_dir_path,
                 database_alert_words_file_name,
                 database_alert_words_dir_path,
                 lexique_update = False):

        """ INITIALISATIONS DES DICTIONNAIRES """

        # Chargement du dicitonnaire alert_lemma
        f_alert_lemma = open(alert_lemma_dir_path + alert_lemma_file_name, 'r')
        self.alert_lemma = dict(eval(f_alert_lemma.read()))

        # Chargement du dictionnaire database_alert_words
        f_database_alert_words = open(database_alert_words_dir_path + database_alert_words_file_name, 'r')
        self.database_alert_words = dict(eval(f_database_alert_words.read()))

        """ MISE A JOUR DU LEXIQUE AVANT ANAYSE """
        if lexique_update:
            lt = LexiqueTools()
            lt.lexique_update(self.database_alert_words)

        """ INITIALISATION DU FRENCH PROCESSING """

        self.fp = FrenchPreprocessing()


    """ DEFINITION DE LA METHODE D'ANALYSE D'UN FICHIER JSON DE TWEETS """

    # La fonction prend en argument un fichier json au format 'nomfichier.json'
    #et le path du dossier dans lequel il se trouve
    # Ne retourne rien, mais crée un fichier csv dans le dossier indiqué par le chemin : csv_analyzed_dir_path
    # avec les informations décrites dans le README
    def analyze(self, json_file_name_to_analyze,
                json_file_to_analyze_dir_path,
                csv_analyzed_name,
                csv_analyzed_dir_path):

        # Noms des colonnes du csv
        fieldnames_analyzed_data = ["id","date","tweet_url","user-id:user_name",
                                "rt","text", "lemmatized_text","hashtags",
                                "names_in_tweet_id:names_in_tweet","emoji",
                                "urls_in_tweet","nb_rt","nb_like",
                                "list_alert_lemma_1","list_alert_lemma_2",
                                "nb_alert_lemma_1","nb_alert_lemma_2"]

        # Ouverture du json
        json = pd.read_json(path_or_buf= json_file_to_analyze_dir_path + json_file_name_to_analyze, orient='records', encoding='utf-8', lines = True)

        # Pour chaque tweet on va récupérer les données qui nous interessent
        # Vectorization 
        df = pd.DataFrame(columns = fieldnames_analyzed_data)

        # Récupération des infos générales sur le tweet
        df['id'] = json['id']
        df['date'] = json['created_at']
        df['tweet_url'] = (json['user'].map(lambda x: "https://twitter.com/" + x['screen_name']+"/status/")) + json['id'].map(str)
        df['user-id:user_name'] = json['id'].map(str) + ':' + json['user'].map(lambda x: x['screen_name'])

        # Récupération du texte du tweet, du booléen indiquant si c'est un retweet
        # et séparation des emojis du text pour enregistrer leurs noms dans une autre colonne du csv
        df['rt'] = json['retweeted']

        df['text_1'] = json['full_text']
        df['text_1'] = df['text_1'].map(lambda x: {"full_text": x})
        if "retweeted_status" not in json:
            df['text'] = df['text_1']
        else:
            df['text'] = json['retweeted_status']
            df['text'] = df['text'].fillna(df["text_1"])

        df['text'] = df['text'].map(lambda x: x["full_text"])
        df.drop(columns=['text_1'], inplace = True)
        df['text'] = df['text'].map(lambda x: remove_emoji(x)[0])
        df['emoji'] = df['text'].map(lambda x: remove_emoji(x)[1])

        # Récupération des urls présentes dans le tweet
        df['urls_in_tweet'] = json['entities'].map(lambda x: [dic['url'] for dic in x['urls']])

        # Suppression des urls dans le texte du tweet
        supr_url = re.compile(r'http[s]*://.+ ')
        df['text'] = df['text'].map(lambda x: re.sub(supr_url, " ", x))

        # Récupération des hashtags du tweet
        df['hashtags'] = json['entities'].map(lambda x: "|".join([dic['text'] for dic in x['hashtags']]))

        # Récupération des pseudos cités et id
        df['names_in_tweet_id:names_in_tweet'] = json['entities'].map(lambda x: "|".join([ str(dic['id'])+':'+dic['screen_name'] for dic in x['user_mentions'] ]))

        # Récupération du nombre de retweets du nombre de like
        df['nb_rt'] = json['retweet_count']
        df['nb_like'] = json['favorite_count']

        """ PREPROCESSING """
        # Passage de tous les hashtags, et nom des emojis en minuscules
        df['hashtags'] = df['hashtags'].str.lower()
        df['emoji'] = df['emoji'].str.lower()

        # Pré-traitement du text
        supr = re.compile(r'[~§¨^°¤\*\+\s=#\@\(\)\[\]|_<>\{\} ]+')
        df['text'] = df['text'].map(lambda x: re.sub(supr, " ", x))

        # On applique l'algorithme de préprocessing pour obtenir : text_lemmatized
        df['lemmatized_text'] = df['text'].map(lambda x: self.fp.preprocessing(x))

        """ RECHERCHE DES MOTS D'ALERTE DANS lemmatized_text """
        # mots d alerte de categorie 1
        alert_lemma_1 = [alert_1 for alert_1 in self.alert_lemma.keys() if (self.alert_lemma[alert_1]==1) ]
        # mots d alerte de categorie 2
        alert_lemma_2 = [alert_2 for alert_2 in self.alert_lemma.keys() if (self.alert_lemma[alert_2]==2) ]
        df["list_alert_lemma_1"] = df["lemmatized_text"].map(lambda x: "|".join([mots for mots in x.split(" ") if (mots in alert_lemma_1)]) )
        df["list_alert_lemma_2"] = df["lemmatized_text"].map(lambda x: "|".join([mots for mots in x.split(" ") if (mots in alert_lemma_2)]) )
        df["nb_alert_lemma_1"] = df["lemmatized_text"].map(lambda x: len([mots for mots in x.split(" ") if (mots in alert_lemma_1)]) )
        df["nb_alert_lemma_2"] = df["lemmatized_text"].map(lambda x: len([mots for mots in x.split(" ") if (mots in alert_lemma_2)]) )


        """ CSV """
        df.to_csv(path_or_buf= csv_analyzed_dir_path + csv_analyzed_name, index=False)