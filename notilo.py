import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import re
import PyPDF2
import odf.opendocument
import odf.text
import chardet
import os

class TextAnalyzer:
    def __init__(self):
        self.text = ""
        self.current_file = None
        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Analyseur de Texte")
        self.root.geometry("800x600")

        # Zone de saisie du chemin du fichier
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=10, padx=10, fill='x')
        ttk.Label(file_frame, text="Chemin du fichier:").pack(side='left')
        self.file_path = ttk.Entry(file_frame, width=50)
        self.file_path.pack(side='left', padx=5)
        ttk.Button(file_frame, text="Parcourir...", command=self.browse_file).pack(side='left')
        ttk.Button(file_frame, text="Ouvrir", command=self.load_file).pack(side='left', padx=5)
        ttk.Button(file_frame, text="Sauvegarder", command=self.save_file).pack(side='left', padx=5)
        ttk.Button(file_frame, text="Sauvegarder sous...", command=self.save_file_as).pack(side='left')

        # Zone d'affichage du texte
        text_frame = ttk.Frame(self.root)
        text_frame.pack(pady=10, padx=10, fill='both', expand=True)
        self.text_display = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, height=15)
        self.text_display.pack(fill='both', expand=True)

        # Zone des contrôles
        control_frame = ttk.LabelFrame(self.root, text="Contrôles")
        control_frame.pack(pady=10, padx=10, fill='x')

        # Boutons pour les différentes analyses
        ttk.Button(control_frame, text="Analyser statistiques", command=self.show_stats).pack(side='left', padx=5)
        
        # Frame pour la recherche de mots
        search_frame = ttk.LabelFrame(control_frame, text="Rechercher un mot")
        search_frame.pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=20).pack(side='left')
        ttk.Button(search_frame, text="Chercher", command=self.search_text).pack(side='left')

        # Frame pour la recherche de lettres
        letter_frame = ttk.LabelFrame(control_frame, text="Rechercher une lettre")
        letter_frame.pack(side='left', padx=5)
        self.letter_var = tk.StringVar()
        ttk.Entry(letter_frame, textvariable=self.letter_var, width=5).pack(side='left')
        ttk.Button(letter_frame, text="Chercher", command=self.search_letter).pack(side='left')

        # Frame pour le remplacement
        replace_frame = ttk.LabelFrame(control_frame, text="Remplacer")
        replace_frame.pack(side='left', padx=5)
        self.replace_from = tk.StringVar()
        self.replace_to = tk.StringVar()
        ttk.Entry(replace_frame, textvariable=self.replace_from, width=10).pack(side='left')
        ttk.Label(replace_frame, text="→").pack(side='left')
        ttk.Entry(replace_frame, textvariable=self.replace_to, width=10).pack(side='left')
        ttk.Button(replace_frame, text="Remplacer", command=self.replace_text).pack(side='left')

        # Zone de résultats
        result_frame = ttk.LabelFrame(self.root, text="Résultats")
        result_frame.pack(pady=10, padx=10, fill='x')
        self.result_display = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=6)
        self.result_display.pack(fill='x', expand=True, padx=5, pady=5)

    def browse_file(self):
        filetypes = (
            ('Tous les fichiers supportés', '*.txt;*.pdf;*.ods'),
            ('Fichiers texte', '*.txt'),
            ('Fichiers PDF', '*.pdf'),
            ('Fichiers ODS', '*.ods')
        )
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path.delete(0, tk.END)
            self.file_path.insert(0, filename)

    def detect_encoding(self, filepath):
        """Détecte l'encodage du fichier"""
        with open(filepath, 'rb') as file:
            raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

    def load_file(self):
        filepath = self.file_path.get()
        try:
            if not filepath:
                messagebox.showerror("Erreur", "Veuillez sélectionner un fichier")
                return

            if filepath.endswith('.txt'):
                try:
                    encoding = self.detect_encoding(filepath)
                    with open(filepath, 'r', encoding=encoding) as file:
                        self.text = file.read()
                except UnicodeDecodeError:
                    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                    for enc in encodings:
                        try:
                            with open(filepath, 'r', encoding=enc) as file:
                                self.text = file.read()
                                break
                        except UnicodeDecodeError:
                            continue
                    else:
                        raise UnicodeDecodeError("Impossible de détecter l'encodage du fichier")

            elif filepath.endswith('.pdf'):
                self.text = self.read_pdf(filepath)
            elif filepath.endswith('.ods'):
                self.text = self.read_ods(filepath)
            else:
                messagebox.showerror("Erreur", "Format de fichier non supporté")
                return
            
            self.current_file = filepath
            self.text_display.delete('1.0', tk.END)
            self.text_display.insert('1.0', self.text)
            self.show_result("Fichier chargé avec succès!")
            self.root.title(f"Analyseur de Texte - {os.path.basename(filepath)}")

        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier non trouvé")
        except PermissionError:
            messagebox.showerror("Erreur", "Permission refusée pour accéder au fichier")
        except UnicodeDecodeError as e:
            messagebox.showerror("Erreur", f"Erreur de décodage du fichier: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")

    def save_file(self):
        if not self.current_file:
            self.save_file_as()
            return
        
        try:
            # Mise à jour du texte depuis l'affichage
            self.text = self.text_display.get('1.0', tk.END).strip()
            
            # Sauvegarde uniquement pour les fichiers texte
            if self.current_file.endswith('.txt'):
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.text)
                self.show_result("Fichier sauvegardé avec succès!")
            else:
                messagebox.showwarning("Attention", 
                    "La sauvegarde n'est possible que pour les fichiers texte. "
                    "Utilisez 'Sauvegarder sous...' pour créer un nouveau fichier texte.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def save_file_as(self):
        try:
            # Mise à jour du texte depuis l'affichage
            self.text = self.text_display.get('1.0', tk.END).strip()
            
            # Demande où sauvegarder le fichier
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Fichier texte", "*.txt")],
                initialfile=os.path.basename(self.current_file) if self.current_file else None
            )
            
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(self.text)
                self.current_file = filepath
                self.file_path.delete(0, tk.END)
                self.file_path.insert(0, filepath)
                self.root.title(f"Analyseur de Texte - {os.path.basename(filepath)}")
                self.show_result("Fichier sauvegardé avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def read_pdf(self, filepath):
        try:
            text = ""
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")

    def read_ods(self, filepath):
        try:
            text = ""
            doc = odf.opendocument.load(filepath)
            for element in doc.getElementsByType(odf.text.P):
                if element.firstChild:
                    text += element.firstChild.data + "\n"
            return text
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier ODS: {str(e)}")

    def count_words(self):
        return len(re.findall(r'\b\w+\b', self.text))

    def count_sentences(self):
        return len(re.findall(r'[.!?]+', self.text))

    def count_letters(self):
        return len(re.findall(r'[a-zA-zÀ-ÿ]', self.text))

    def count_word_occurrences(self, word):
        return len(re.findall(rf'\b{re.escape(word)}\b', self.text, re.IGNORECASE))

    def count_letter_occurrences(self, letter):
        if len(letter) != 1:
            raise ValueError("Veuillez entrer une seule lettre")
        return sum(1 for c in self.text.lower() if c == letter.lower())

    def search_text(self):
        word = self.search_var.get()
        if not word:
            messagebox.showwarning("Attention", "Veuillez entrer un mot à rechercher")
            return
        count = self.count_word_occurrences(word)
        self.show_result(f"Le mot '{word}' apparaît {count} fois dans le texte.")

    def search_letter(self):
        letter = self.letter_var.get()
        if not letter:
            messagebox.showwarning("Attention", "Veuillez entrer une lettre à rechercher")
            return
        try:
            count = self.count_letter_occurrences(letter)
            self.show_result(f"La lettre '{letter}' apparaît {count} fois dans le texte.")
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))

    def replace_text(self):
        old_text = self.replace_from.get()
        new_text = self.replace_to.get()
        if not old_text or not new_text:
            messagebox.showwarning("Attention", "Veuillez remplir les deux champs de remplacement")
            return
        self.text = re.sub(rf'\b{re.escape(old_text)}\b', new_text, self.text)
        self.text_display.delete('1.0', tk.END)
        self.text_display.insert('1.0', self.text)
        self.show_result(f"Remplacement effectué: '{old_text}' → '{new_text}'")

    def show_stats(self):
        stats = f"""Statistiques du texte:
        - Nombre de mots: {self.count_words()}
        - Nombre de phrases: {self.count_sentences()}
        - Nombre de lettres: {self.count_letters()}
        """
        self.show_result(stats)

    def show_result(self, message):
        self.result_display.delete('1.0', tk.END)
        self.result_display.insert('1.0', message)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    analyzer = TextAnalyzer()
    analyzer.run()