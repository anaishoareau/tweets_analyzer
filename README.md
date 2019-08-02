# TWEETS ANALYZER

Analyze tweets to extract those that deal with a particular theme

## Installation

Vérifier que la commande pip et que le package python git (commande : pip install git) sont installés.

#### Pour installer le package french_preprocessing, executer la commande (dans anaconda prompt par exemple) :
#### pip install git+https://github.com/anaishoareau/tweets_analyzer.git

#### ATTENTION : Cette commande installe aussi les dépendances (les packages python tweepy, pandas, unidecode). Si vous rencontrez des problèmes, il faut les installer à part.

Les versions utilisées sont :

tweepy : 3.8.0

pandas : 0.24.2

unidecode : 1.1.1

#### IL FAUT INSTALLER LE PACKAGE FRENCH_PREPROCESSING POUR QUE TWEETS_ANALYZER FONCTIONNE.

Les informations relatives à l'installation de french_preprocessing sont explicitées dans 
README du repository GitHub du package : https://github.com/anaishoareau/french_preprocessing

## Objectif du package

Réaliser une analyse de tweets pour extraire ceux abordant un thème particulier.

####  Exemple de cas d'usage :

Si on veut voir quels sont les problèmes informatiques que rencontrent 
les utilisateurs Twitter avec la plateforme, on peut imaginer deux catégories 
de mots à tracker dans les textes des tweets : 

- Mots appartenant au champ lexical du problème
- Mots appartenant au champ lexical de l'informatique en relation avec Twitter

Et faire une étude sur les tweets dont les textes contiennent 
au moins un mot de chaque catégorie.


## Phases pour la réalisation de l'analyse

#### Phase préparatoire (Facultatif) :

Extraction de tweets en rapport avec un mot-clé. (Mot-clé du cas d'usage d'exemple : 'twitter')

Le package twitter_extraction permet de réaliser l'opération : https://github.com/anaishoareau/twitter_extraction

#### Première phase de l'analyse : 

Extraction des informations intéressantes des tweets (voir le détail des colonnes du csv) 
et preprocessing à l'aide du module french_preprocessing à installer préalablement : 
https://github.com/anaishoareau/french_preprocessing

Le preprocessing à l'aide du package french_preprocessing regroupe les étapes suivantes :
- Tokenisation et simplification (suppression des stopwords, des symboles inutiles...)
- Tagging (Avec le StanfordPOSTagger et réduction des tags)
- Lemmatisation

#### Deuxième phase de l'analyse : 

Comparaison des mots du texte de chaque tweet (ayant subis le preprocessing) au 
dictionnaire de lemme(*) d'alerte, et stockage des informations utiles dans le csv d'analyse.

(*)Lemme : Mot dans sa forme réduite, tel qu'on le trouve dans un dictionnaire.

Exemple mot -> lemme : 

- "alimentera" -> "alimenter"
- "chanteuse" -> "chanteur"
- "pimentées" -> "pimenté"
- "consonne" -> "consonne"

## Création des dictionnaires relatifs aux mots d'alerte (Propre au cas d'usage choisi)

### Format des fichiers à créer : 

- database_alert_words.txt

Ce ficher texte doit être construit comme un dictionnaire de dictionnaire. 
Pour en remplir un, il est possible d'utiliser les méthodes de la classe AlertDataTools du module alert_data_tools.

Les mots du fichier database_alert_word.txt doivent être écrits avec leurs accents, 
dans toutes les formes nécessaires : noms pluriels, féminins, féminins pluriels, 
adjectifs pluriels, féminins, féminins pluriels, verbes conjugués...

Les tags autorisés sont : 'v', 'nc', 'adj', 'c', 'npp', 'adv', 'det', 'pro', 'prep', 'i', 'ponct', 'cl', 'et'

(Il est possible d'utilser les fonctions conjug_1 et conjug_2 du module general_tools pour obtenir
la liste de toutes les formes conjuguées d'un verbe régulier du 1er ou du 2ème groupe)

##### Exemple de la forme du fichier database_alert_words.txt :

{'problèmes' : {'nc' : 'problème'}, 'problème' : {'nc' : 'problème'},
'ordinateurs' : {'nc' : 'ordinateur'}, 'problème' : {'nc' : 'ordinateur'},
'connecté' : {'v' : 'connecter', 'adj' : 'connecté'}}

- alert_lemma.txt

Ce fichier texte doit être construit comme un dictionnaire.
Pour en remplir un, il est possible d'utiliser les méthodes de la classe AlertDataTools du module alert_data_tools.

Ce fichier permet de connaître la catégorie du lemme que l'on va tracker. 

##### Exemple de la forme du fichier alert_lemma.txt : 

{'problème' : 1, 'ordinateur' : 2, 'connecter' : 2, 'connecté' : 2}

### Outils pour la création de database_alert_word.txt et alert_lemma.txt :

#### Import et instanciation

from tweets_analyzer.alert_data_tools import AlertDataTools

adt=AlertDataTools(alert_lemma_file_name,alert_lemma_dir_path,database_alert_words_file_name,database_alert_words_dir_path)

#### Détail des méthodes 

- adt.in_database_alert_words(word)

Renvoie False, si le mot "word" ne se trouve pas dans database_alert_words

Renvoie le dictionnaire associé à "word" : {tag1 : lemma1, tag2 : lemma2}, si le mot "word" se trouve dans database_alert_words

- adt.in_alert_lemma(word)

Renvoie False, si le lemme "lemma" ne se trouve pas dans alert_lemma

Renvoie la catégorie associée à lemma : 1 ou 2, si le lemme "lemma" se trouve dans alert_lemma

- adt.add_element(word, lemma, tag, category)

Ne renvoie rien

Ajoute l'élément dans dans database_alert_word ( {word : {tag:lemma}} ) et dans alert lemma ( {lemma : category} )

- adt.remove_lemma_in_alert_lemma(lemma)

Supprime le lemme "lemma" de alert_lemma

- adt.remove_word_in_database_alert_words(word, tag = 'all')

Si tag = tag1 : Supprime le tag "tag1" de database_alert_word ({word : {tag1 : lemma1, tag2 : lemma2}} -> {word : {tag2 : lemma2}})

Si tag = 'all' : Supprime le mot "word" de database_alert_word ({word : {tag1 : lemma1, tag2 : lemma2}} -> {})

## Détail des colonnes du fichier CSV d'analyse

- "id" : Identifiant Twitter du tweet
- "date" : Date et heure de création du tweet (UTC+0)
- "tweet_url" : Lien url du tweet
- "user-id:user_name" : Identifiant et pseudo (@) de la personne qui a tweeté, id et pseudo séparés par ":"
- "rt" : Booléen indiquant si le tweet est un retweet ou non (True or False)
- "text" : Texte du tweet
- "lemmatized_text" : Texte auquel on a appliqué le pré-processing complet
- "hashtags" : Hashtags dans le texte du tweet, hashtags séparés par '|'
- "names_in_tweet_id:names_in_tweet" : Identifiants et pseudos (@) des personnes citées dans le texte du tweet,
id et pseudo d'une personne séparés par ":", les différentes personnes séparés par '|'
- "emoji" : Noms des emojis présents dans le texte du tweet, emojis séparés par '|'
- "urls_in_tweet" : Liens url présents dans le texte du tweet, urls séparés '|'
- "nb_rt" : Nombre de fois que le tweet a été retweeté (au moment de l'extraction)
- "nb_like" : Nombre de fois que le tweet a été liké (au moment de l'extraction)
- "list_alert_lemma_1" : Mots d'alerte de catégorie 1 présents dans le texte du tweet, mots séparés par '|'
- "list_alert_lemma_2" : Mots d'alerte de catégorie 2 présents dans le texte du tweet, mots séparés par '|'
- "nb_alert_lemma_1" : Nombre de mots d'alerte de catégorie 1 dans le texte du tweet
- "nb_alert_lemma_2" : Nombre de mots d'alerte de catégorie 2 dans le texte du tweet


## Exemple d'utilisation de la méthode d'analyse

#### IMPORTS

import pandas as pd

from tweets_analyzer.tweets_analyzer import TweetsAnalyzer

#### DEFINITION DES CONSTANTES (Informations à modifier)

alert_lemma_file_name, alert_lemma_dir_path = 'alert_lemma.txt', 'C:\chemin\exemple\alert_data'

database_alert_words_file_name, database_alert_words_dir_path = 'database_alert_words.txt', 'C:\chemin\exemple\alert_data'

json_file_name_to_analyze, json_file_to_analyze_dir_path = '2019-07-26_tweets.json', 'C:\chemin\exemple\data_to_analyze'

csv_analyzed_name, csv_analyzed_dir_path = 'analyzed_2019-07-26_tweets.csv', 'C:\chemin\exemple\analyzed_data'

lexique_update = False

(lexique_update = True signifie que l'on met à jour les mots du lexique avec database_alert_words, 
on ajoute les élements manquants pour que la lemmatisation soit plus performante pour notre cas)

#### LANCEMENT DE L'ANALYSE

tweets_analyzer = TweetsAnalyzer(alert_lemma_file_name,
                                 alert_lemma_dir_path,
                                 database_alert_words_file_name,
                                 database_alert_words_dir_path, 
                                 lexique_update)

tweets_analyzer.analyze(json_file_name_to_analyze, 
                        json_file_to_analyze_dir_path,
                        csv_analyzed_name,
                        csv_analyzed_dir_path)

#### OUVERTURE ET LECTURE DU FICHIER CSV D'ANALYSE 

dataset = pd.read_csv(csv_analyzed_dir_path + csv_analyzed_name, encoding = 'latin-1')

print(dataset.head())
