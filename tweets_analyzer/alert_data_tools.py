# -*- coding: utf-8 -*-

"""
Auteur : Anaïs HOAREAU
Date : 07/2019
"""


"""
Les mots du database_alert_word doivent être écrit avec leurs accents, 
dans toutes les formes nécessaires : noms pluriels, féminins, féminins pluriels, 
adjectifs pluriels, féminins, féminins pluriels, verbes conjugués...

"""

class AlertDataTools(object):
    
    def __init__(self, alert_lemma_file_name,
                 alert_lemma_dir_path, 
                 database_alert_words_file_name,
                 database_alert_words_dir_path):
        
        self.alert_lemma_file_name = alert_lemma_file_name
        self.database_alert_words_file_name = database_alert_words_file_name
        self.alert_lemma_dir_path = alert_lemma_dir_path
        self.database_alert_words_dir_path = database_alert_words_dir_path
                 
        # Chargement de database_alert_words
        database_alert_words = open(database_alert_words_dir_path + database_alert_words_file_name,'r')
        self.database_alert_words = dict(eval(database_alert_words.read()))
        
        # Chargement de alert_lemma
        f_alert_lemma = open(alert_lemma_dir_path + alert_lemma_file_name, 'r')
        self.alert_lemma = dict(eval(f_alert_lemma.read()))

    # Méthode qui prend en argument une string 
    # qui renvoie False si le mot n'est pas dans le dictionnaire database_alert_words
    # qui renvoie la valeur associée à la clé correspondante à la string sinon
    def in_database_alert_words(self,word):
         if word in self.database_alert_words.keys():
             return self.database_alert_words[word]
         else:
             return False
         
    # Méthode qui prend en argument une string 
    # qui renvoie False si le mot n'est pas dans la liste
    # qui renvoie la valeur associée à la clé correspondante à la string sinon
    def in_alert_lemma(self,lemma):
        if lemma in self.alert_lemma.keys():
             return self.alert_lemma[lemma]
        else:
             return False
    
    # Méthode qui prend en argument une string, son lemme associé, son tag et la catégorie du lemme
    # qui ajoute ce nouvel élément au dictionnaire (ne fait rien s'il y est déjà)
    # ne renvoie rien
    def add_element(self, word, lemma, tag, category):
        tag_list = ['v', 'nc', 'adj', 'c', 'npp', 'adv', 'det', 'pro', 'prep', 'i', 'ponct', 'cl', 'et']
        
        if tag not in tag_list:
            print("ERROR tag not in the list : 'v', 'nc', 'adj', 'c', 'npp', 'adv', 'det', 'pro', 'prep', 'i', 'ponct', 'cl', 'et'")
            return
        else:
 
            # INSERTION DANS LE DICTIONNAIRE database_alert_words
            
            if word not in self.database_alert_words.keys():
                # Si le mot n'est pas dans database_alert_words on l'ajoute
                self.database_alert_words[word] = {tag:lemma}
            else:
                # Sinon on ajoute le tag ou on met à jour la valeur du lemme si le tag existe déjà
                self.database_alert_words[word][tag]=lemma
                        
            # INSERTION DU LEMME DANS LE DICTIONNAIRE alert_lemma
            
            # On test si le lemme est dans le dictionnaire alert_lemma
            # Si le lemme n'est pas dans le dictionnaire on le rajoute avec sa catégorie
            # Si il y est avec la mauvaise catégorie, on mets à jour la catégorie
            self.alert_lemma[lemma] = category
        
        # REECRITURE DANS LES FICHIERS TXT database_alert_words ET alert_lemma   
        with open(self.database_alert_words_dir_path + self.database_alert_words_file_name,'w') as f:
            f.write(str(self.database_alert_words))
        with open(self.alert_lemma_dir_path + self.alert_lemma_file_name,'w') as f:
            f.write(str(self.alert_lemma))
    
    def remove_lemma_in_alert_lemma(self, lemma):
        del self.alert_lemma[lemma]
        
        with open(self.alert_lemma_dir_path + self.alert_lemma_file_name,'w') as f:
            f.write(str(self.alert_lemma))

    def remove_word_in_database_alert_words(self, word, tag = 'all'):
        if tag == 'all':
            del self.database_alert_words[word]
        else:
            del self.database_alert_words[word][tag]
            
        with open(self.database_alert_words_dir_path + self.database_alert_words_file_name,'w') as f:
            f.write(str(self.database_alert_words))
            