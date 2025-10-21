import hashlib
import time

def crack_md5_dictionnaire(hash_a_cracker, fichier_dictionnaire):
    """
    Tente de cracker un hash MD5 en utilisant une attaque par dictionnaire.
    """
    try:
        # Ouvre le fichier dictionnaire en mode lecture
        with open(fichier_dictionnaire, 'r') as f:
            for ligne in f:
                mot = ligne.strip() # Enlève les espaces et sauts de ligne
                
                # Calcule le hash MD5 du mot
                hash_calcule = hashlib.md5(mot.encode()).hexdigest()
                
                # Compare le hash calculé au hash cible
                if hash_calcule == hash_a_cracker:
                    return mot # Trouvé !
                    
    except FileNotFoundError:
        print(f"[ERREUR ] Le fichier dictionnaire '{fichier_dictionnaire}' n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"[ERREUR] Une erreur est survenue : {e}")
        return None
        
    return None # Non trouvé

# --- Point d'entrée principal du script ---
if __name__ == "__main__":
    
    # Hash MD5 pour "123456"
    HASH_CIBLE = "e10adc3949ba59abbe56e057f20f883e" 
    NOM_DU_DICTIONNAIRE = "dico.txt" 
    
    print(f"--- Service de Crack MD5 (v1.0 Console) ---")
    print(f"Hash cible : {HASH_CIBLE}")
    print(f"Dictionnaire : {NOM_DU_DICTIONNAIRE}")
    print("---------------------------------------------")
    print("Démarrage du crack...")

    start_time = time.time() # Démarre le chronomètre
    resultat = crack_md5_dictionnaire(HASH_CIBLE, NOM_DU_DICTIONNAIRE)
    end_time = time.time() # Arrête le chronomètre
    duree = end_time - start_time

    print("---------------------------------------------")
    if resultat:
        print(f"✅ TROUVÉ ! \nMot de passe : {resultat}")
    else:
        print(f"❌ NON TROUVÉ.")
    
    print(f"Durée de l'opération : {duree:.4f} secondes.")