import ast
import random
from difflib import SequenceMatcher
from app.Entities.user import User

def type_sort(liste):
    types = {}
    for lst in liste:
        if lst.type not in types:
            types[lst.type] = []
            types[lst.type].append(lst)
        else:
            types[lst.type].append(lst)


    return types

def types_sort(liste):
    types = {}
    for lst in liste:
        if lst['type'] not in types:
            types[lst['type']] = []
            types[lst['type']].append(lst)
        else:
            types[lst['type']].append(lst)


    return types


def Url_convert(url):
    if "drive.google.com/file/d/" in url :
        file_id = url.split("/d/")[1].split("/")[0]
        direct_url = f"https://drive.google.com/thumbnail?id={file_id}"
        return direct_url
    
    else :
        return "L'url fourni n'est pas correcte"
    
def Url_convert_youtube(url):
    if "//youtu." in url :
        file_id = url.split("=")[1]
        direct_url = f"https://img.youtube.com/vi/{file_id}/default.png"
        return direct_url
    
    else :
        return "L'url fourni n'est pas correcte"
    

def convert_instructions(instru):
    return ast.literal_eval(instru)

def dict_recette(liste):
    dico = []
    for r in liste:
        dico.append({'id': r.id,
                      'nom': r.nom,
                      'type': r.type,
                      'instructions': r.instructions,
                      'image_url': r.image_url,
                      'lien_youtube': r.lien_youtube,
                      'temp_de_cuisson': r.temps_de_cuisson
                      })
    return dico


def dict_ingredient(liste):
    dico = []
    for i in liste:
        dico.append({'id': i.id,
                      'nom': i.nom,
                      'poids': i.poids,
                      })
    return dico


def dict_ingredient_poids(liste):
    dico = {}
    for i in liste:
        dico[i.nom] = i.poids
    return dico


def dict_recette_ingre(liste):
    dico = []
    for r_i in liste:
        dico.append({
            'id_recette': r_i.recette_id,
            'id_ingredient': r_i.ingredient_id,
            'quantite': r_i.quantite,
        })
    return dico

def dict_favoris(liste):
    dico = []
    for f in liste:
        dico.append({
            'id_recette': f.recette_id,
            'id_user': f.user_id,
        })
    return dico

def dict_historique(liste):
    dico = []
    for h in liste:
        dico.append({
            'id_recette': h.recette_id,
            'id_user': h.user_id,
            'date': h.date,
            'id': h.id
        })
    return dico

def Search_recette(id,recette):
    try:
        id = int(id)
        for r in recette:
            if r['id'] == id:
                return r
    except:
        for r in recette:
            if r['nom'].lower() == id.lower():
                return r
        
def Search_recette_ingre(id, liste):
    li = []
    for r_i in liste:
        if r_i['id_recette'] == id:
            li.append(r_i['id_ingredient'])

    return li

def Liste_recette(recette):
    l = []
    for r in recette:
        l.append(r['nom'])
    return l


def Search_nom_ingre(id, liste):
    for ingre in liste:
        if ingre['id'] == id:
            return ingre['nom']
        
def closest_string(str, liste):
    return max(liste, key=lambda x: SequenceMatcher(None, str, x).ratio())

def SearchUser(id):
    u = User()
    session = u.Session()
    result = session.query(User).filter(User.id == id).first()
    print(result.nom)
    return result


def clean_text(text):
    return text.encode("utf-8", "replace").decode("utf-8")