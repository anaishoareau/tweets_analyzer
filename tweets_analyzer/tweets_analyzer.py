# -*- coding: utf-8 -*-

"""
Auteur : Anaïs HOAREAU
Date : 07/2019
GitHub : https://github.com/anaishoareau
Linkedin : https://www.linkedin.com/in/ana%C3%AFs-hoareau-a2a042183/
"""

""" IMPORTS """

import pandas as pd
import math
import csv

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
        json = pd.read_json(open(json_file_to_analyze_dir_path + json_file_name_to_analyze, "r", encoding="utf8"),lines=True)
            
        # On crée le fichier csv d'analyse
        with open(csv_analyzed_dir_path + csv_analyzed_name, 'w', encoding = 'utf-8') as csvfile:
            
            # On écrit le nom des colonnes dans le csv
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_analyzed_data)
            writer.writeheader()
            
            # Pour chaque tweet on va récupérer les données qui nous interesse
            for i in range(0, len(json['id'])):
                dico = {}
                
                """ ENREGISTREMENT DES DONNEES INTERESSANTES """
                
                # Récupération des infos générales sur le tweet
                dico['id'] = json['id'][i]
                dico['date'] = json['created_at'][i]
                dico['tweet_url'] = "https://twitter.com/"+json['user'][i]['screen_name']+"/status/"+str(json['id'][i])
                dico['user-id:user_name'] = str(json['id'][i])+':'+json['user'][i]['screen_name']
                
                # Récupération du texte du tweet, du booléen indiquant si c'est un retweet
                # et séparation des emojis du text pour enregistrer leurs noms dans une autre colonne du csv
                try :
                    math.isnan(json['retweeted_status'][i])
                    dico['rt'] = False
                    dico['text'] = str(remove_emoji(json['full_text'][i])[0])
                    dico['emoji'] = str(remove_emoji(json['full_text'][i])[1])
                except :
                    dico['rt'] = True
                    dico['text'] = str(remove_emoji(json['retweeted_status'][i]['full_text'])[0])
                    dico['emoji'] = str(remove_emoji(json['retweeted_status'][i]['full_text'])[1])
                
                # Récupération des urls présentes dans le tweet
                urls = json['entities'][i]['urls']
                list_urls_in_tweet = []
                for k in range(len(urls)):
                    list_urls_in_tweet.append(urls[k]['url'])
                dico['urls_in_tweet'] = '|'.join(list_urls_in_tweet)
    
                # Suppression des urls dans le texte du tweet
                if 'http' in dico['text']:
                    text = dico['text']
                    text_list = text.split(' ')
                    for m in range(len(text_list)):
                        if 'http' in text_list[m] : 
                            text_list[m] = ""
                    dico['text'] = ' '.join(text_list)
    
                # Récupération des hashtags du tweet
                hashtags = json['entities'][i]['hashtags']
                list_hashtags = []
                for k in range(len(hashtags)):
                        list_hashtags.append(hashtags[k]['text'])
                dico['hashtags'] = "|".join(list_hashtags)
    
                # Récupération des pseudos cités et id
                user_mentions = json['entities'][i]['user_mentions']
                list_user_mentions = []
                for j in range(len(user_mentions)):
                    list_user_mentions.append(str(user_mentions[j]['id'])+':'+str(user_mentions[j]['screen_name']))
                dico['names_in_tweet_id:names_in_tweet'] = "|".join(list_user_mentions)
                
                # Récupération du nombre de retweets du nombre de like
                dico['nb_rt'] = json['retweet_count'][i]
                dico['nb_like'] = json['favorite_count'][i]
                
                """ PREPROCESSING """
                
                # Passage de tous les textes, hashtags, et nom des emojis en minuscules
                dico['text'] = dico['text'].lower()
                dico['hashtags'] = dico['hashtags'].lower()
                dico['emoji'] = dico['emoji'].lower()
                
                # Pré-traitement du text
                dico['text'] = dico['text'].replace('\n',' ')
                dico['text'] = dico['text'].replace('#',' ')
                dico['text'] = dico['text'].replace('@',' ')
                dico['text'] = dico['text'].replace('-',' ')
                dico['text'] = dico['text'].replace('(',' ')
                dico['text'] = dico['text'].replace(')',' ')
                dico['text'] = dico['text'].replace('[',' ')
                dico['text'] = dico['text'].replace(']',' ')
                dico['text'] = dico['text'].replace('&',' ')
                dico['text'] = dico['text'].replace('|',' ')
                dico['text'] = dico['text'].replace('_',' ')
                dico['text'] = dico['text'].replace('<',' ')
                dico['text'] = dico['text'].replace('>',' ')
                dico['text'] = dico['text'].replace('{',' ')
                dico['text'] = dico['text'].replace('}',' ')
                dico['text'] = dico['text'].replace('    ',' ')
                dico['text'] = dico['text'].replace('   ',' ')
                dico['text'] = dico['text'].replace('  ',' ')
                
                # On applique l'algorithme de préprocessing pour obtenir : text_lemmatized
                dico['lemmatized_text'] = self.fp.preprocessing(dico['text'])
                
                """ RECHERCHE DES MOTS D'ALERTE DANS lemmatized_text """
                
                # Détermination des valeurs des colonnes : 
                #"nb_alert_lemma_1","nb_alert_lemma_2","list_alert_lemma_1","list_alert_lemma_2"
                
                list_alert_lemma_1 = []
                list_alert_lemma_2 = []
                
                compt_1 = 0
                compt_2 = 0
                
                for word in dico['lemmatized_text'].split():
                    for lemma in self.alert_lemma.keys():
                        if word == lemma:
                            if self.alert_lemma[lemma] == 1:
                                compt_1 += 1
                                list_alert_lemma_1.append(word)
                            else:
                                compt_2 += 1
                                list_alert_lemma_2.append(word)
                                
                dico["list_alert_lemma_1"] = "|".join(list_alert_lemma_1)
                dico["list_alert_lemma_2"] = "|".join(list_alert_lemma_2)
                
                dico["nb_alert_lemma_1"] = compt_1
                dico["nb_alert_lemma_2"] = compt_2
                
                writer.writerow(dico)