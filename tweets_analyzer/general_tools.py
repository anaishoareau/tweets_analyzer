# -*- coding: utf-8 -*-

"""
Auteur : Anaïs HOAREAU
Date : 07/2019
"""

# Fonction qui prend un texte (string) en argument
# retourne le texte sans emoji (string) et une string 
#composée des noms des émojis présents dans le texte d'entrée en minuscule séparés par "|"

def remove_emoji(text_string):
    # IMPORTS
    import unicodedata
    from unidecode import unidecode

    new_text_string = ""
    emoji_string = ""
    for character in text_string:
        try:
            chart = character.encode('latin-1')
            new_text_string += character
            
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            
            if replaced != '':
                new_text_string += replaced
            else:
                
                try:
                    if emoji_string == "": 
                        emoji_string += unicodedata.name(character)
                    else: 
                        emoji_string += "|" + unicodedata.name(character)
                        
                except ValueError:
                    emoji_string += ""

    return (new_text_string, emoji_string.lower())

# Fonction qui permet de générer les formes conjuguées des verbes du 1er groupe  
def conjug_1(first_group_verb):  
    ending = ['er', 'e', 'es', 'ons', 'ez', 'ent', 'é', 'ais', 'ait', 'ions', 'iez', 'aient', 'ai', 'as', 'a', 'âmes',
                   'âtes', 'èrent', 'erai', 'eras', 'era', 'erons', 'erez', 'eront', 'erais', 'erait', 'erions', 'eriez',
                   'eraient', 'asse', 'asses', 'ât', 'assions', 'assiez', 'assent', 'ant']
    conjug = []
    for en in ending:
        conjug.append(first_group_verb[:-2]+en)
    return conjug

# Fonction qui permet de générer les formes conjuguées des verbes du 2eme groupe 
def conjug_2(second_group_verb):
    ending = ['ir', 'is', 'it', 'issons', 'issez', 'issent', 'issais', 'issait', 'issions', 
                     'issiez', 'issaient', 'îmes', 'îtes', 'irent', 'irai', 'iras', 'ira', 'irons', 
                     'irez', 'iront', 'irais', 'irait', 'irions', 'iriez', 'iraient', 'isse', 'isses', 
                     'issions', 'issiez', 'issent', 'i', 'issant']
    conjug = []
    for en in ending:
        conjug.append(second_group_verb[:-2]+en)
    return conjug
                