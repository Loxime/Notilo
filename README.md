# Analyseur de Texte 📝

## Description
L'Analyseur de Texte est un programme Python avec interface graphique qui permet d'analyser et de modifier facilement des fichiers texte, PDF et ODS. Il offre des fonctionnalités d'analyse statistique, de recherche et de modification de texte.

## 🚀 Fonctionnalités

### Lecture de fichiers
- Support des formats : `.txt`, `.pdf`, `.ods`
- Détection automatique de l'encodage des fichiers texte
- Interface de sélection de fichiers intuitive

### Analyse de texte
- Comptage de mots
- Comptage de phrases
- Comptage de lettres
- Recherche d'occurrences de mots
- Recherche d'occurrences de lettres

### Modification de texte
- Fonction rechercher/remplacer
- Sauvegarde des modifications
- Export en nouveau fichier texte

## 📋 Prérequis

### Python
- Python 3.6 ou supérieur

### Bibliothèques requises
```bash
pip install PyPDF2 odf chardet
```

## 🛠️ Installation

1. Clonez ou téléchargez le code source
2. Installez les dépendances :
```bash
pip install PyPDF2 odf chardet
```
3. Lancez le programme :
```bash
python analyseur_texte.py
```

## 📖 Guide d'utilisation

### Ouvrir un fichier
1. Cliquez sur "Parcourir..." pour sélectionner un fichier
2. Ou entrez directement le chemin dans le champ
3. Cliquez sur "Ouvrir"

### Analyser le texte
- Cliquez sur "Analyser statistiques" pour voir :
  - Le nombre de mots
  - Le nombre de phrases
  - Le nombre total de lettres

### Rechercher du texte
1. **Rechercher un mot**
   - Entrez le mot dans le champ "Rechercher un mot"
   - Cliquez sur "Chercher"
   - Le nombre d'occurrences s'affiche dans la zone de résultats

2. **Rechercher une lettre**
   - Entrez une lettre dans le champ "Rechercher une lettre"
   - Cliquez sur "Chercher"
   - Le nombre d'occurrences s'affiche dans la zone de résultats

### Modifier le texte
1. **Remplacer du texte**
   - Entrez le texte à remplacer dans le premier champ
   - Entrez le nouveau texte dans le second champ
   - Cliquez sur "Remplacer"

2. **Sauvegarder les modifications**
   - Cliquez sur "Sauvegarder" pour mettre à jour le fichier actuel
   - Ou "Sauvegarder sous..." pour créer un nouveau fichier
   
   ⚠️ Note : La sauvegarde n'est possible que pour les fichiers .txt

## 🔍 Fonctionnalités détaillées

### Gestion des fichiers
- **Fichiers texte (.txt)**
  - Lecture et écriture complètes
  - Détection automatique de l'encodage
  - Support des caractères spéciaux et accents

- **Fichiers PDF (.pdf)**
  - Lecture seule
  - Extraction du texte de toutes les pages
  - Conservation de la structure du texte

- **Fichiers ODS (.ods)**
  - Lecture seule
  - Extraction du texte des cellules
  - Support du formatage basique

### Interface utilisateur
- Zone de texte principale pour visualiser et modifier le contenu
- Zone de résultats pour afficher les statistiques et recherches
- Boutons et contrôles clairement organisés et étiquetés

## ⚠️ Limitations connues
- La sauvegarde n'est possible que pour les fichiers .txt
- Les fichiers PDF et ODS sont en lecture seule
- Les mises en forme complexes des PDF et ODS ne sont pas conservées

## 🐛 Résolution des problèmes courants

### Le fichier ne s'ouvre pas
- Vérifiez que le fichier existe et n'est pas corrompu
- Vérifiez vos permissions d'accès au fichier
- Pour les fichiers texte, essayez de les rouvrir avec un autre encodage

### Erreurs d'encodage
- Le programme essaie automatiquement plusieurs encodages courants
- Si l'erreur persiste, essayez de convertir votre fichier en UTF-8

### Problèmes de sauvegarde
- Vérifiez que vous avez les droits d'écriture dans le dossier
- Assurez-vous que le fichier n'est pas ouvert dans un autre programme
- Utilisez "Sauvegarder sous..." pour créer une nouvelle copie

## 💡 Conseils d'utilisation
- Sauvegardez régulièrement vos modifications
- Pour les gros fichiers, attendez que le chargement soit complet
- Utilisez la recherche de mots pour les termes exacts
- Faites une copie de sauvegarde avant de modifier des fichiers importants

## 🤝 Contribution
N'hésitez pas à contribuer à ce projet en :
- Signalant des bugs
- Proposant des améliorations
- Ajoutant de nouvelles fonctionnalités
- Améliorant la documentation

## 📝 Remarques
Le programme est conçu pour être simple et intuitif. Si vous rencontrez des difficultés ou avez des suggestions d'amélioration, n'hésitez pas à les partager.