import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import colorchooser
from PIL import Image, ImageTk
import random
import json # Besser für Übersetzungsdaten als ein reines Python-Dict im Code

# --- Workaround für Tcl/Tk Pfadproblem ---
# (Code von vorher)
try:
    # ... (Tcl/Tk Pfad-Workaround Code hier einfügen) ...
    python_install_dir = sys.executable.split('python.exe')[0]
    tcl_library_path = os.path.join(python_install_dir, 'tcl', 'tcl8.6')
    tk_library_path = os.path.join(python_install_dir, 'tcl', 'tk8.6')
    if os.path.isdir(tcl_library_path) and os.path.isdir(tk_library_path):
        os.environ['TCL_LIBRARY'] = tcl_library_path
        os.environ['TK_LIBRARY'] = tk_library_path
    else:
        fallback_tcl = r'C:\Program Files\Python313\tcl\tcl8.6' # Anpassen falls nötig
        fallback_tk = r'C:\Program Files\Python313\tcl\tk8.6' # Anpassen falls nötig
        if os.path.isdir(fallback_tcl) and os.path.isdir(fallback_tk):
             os.environ['TCL_LIBRARY'] = fallback_tcl
             os.environ['TK_LIBRARY'] = fallback_tk
except Exception as e:
    print(f"Fehler beim Setzen der Tcl/Tk-Pfade: {e}")
# --- Ende Workaround ---

# --- Konstanten ---
DEFAULT_SIZE = 16
MAX_COLORS = 10
COLOR_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
DEFAULT_COLORS = ["#A0522D", "#8B4513", "#CD853F", "#F4A460", "#DEB887",
                  "#D2B48C", "#BC8F8F", "#FFE4C4", "#FFDEAD", "#FAEBD7"]
LANG_DEFAULT = 'de' # Standardsprache
LANG_FALLBACK = 'en' # Fallback-Sprache

# --- Übersetzungsdaten ---
# Ideal: Aus einer JSON-Datei laden, hier als Dictionary für Einfachheit
translations = {
    "en": {
        "window_title": "Pixel Pattern Generator v4",
        "file_menu": "File",
        "file_menu_save": "Save Image",
        "file_menu_exit": "Exit",
        "lang_menu": "Language",
        "lang_menu_german": "German",
        "lang_menu_english": "English",
        "help_menu": "Help",
        "help_menu_about": "About",
        "about_title": "About Pixel Pattern Generator",
        "about_text": "Pixel Pattern Generator v4\n\nA tool to create and visualize pixel patterns.\nCreated with Python and Tkinter.",
        "label_size": "Image Size (Pixels)",
        "radio_16": "16x16",
        "radio_32": "32x32",
        "label_num_colors": "Number of Colors",
        "label_max_colors": "(1 - {max})", # Platzhalter für Formatierung
        "label_color_settings": "Color Settings",
        "label_percentage_sum_base": "Sum",
        "label_percentage_sum_ok": "OK",
        "label_percentage_sum_needed": "needed",
        "label_percentage_sum_too_much": "too much",
        "label_percentage_sum_invalid": "Invalid Input",
        "label_pattern": "Pattern",
        "label_pattern_size": "Size:",
        "button_random": "Random Pattern",
        "button_preview": "Preview",
        "label_preview": "Preview",
        "label_filename": "File:",
        "button_save": "Save",
        "color_picker_title": "Choose color for '{char}'",
        "error_title": "Error",
        "warning_title": "Warning",
        "info_title": "Info",
        "error_invalid_hex": "Invalid Hex code '{hex}' for color '{char}'.",
        "error_invalid_percent": "Invalid percentage for color '{char}'.",
        "error_invalid_num_colors": "Number of colors must be between 1 and {max}.",
        "error_no_image_generated": "No image has been generated yet.",
        "error_save_failed": "Could not save image:\n{error}",
        "error_save_no_filename": "Please enter a filename.",
        "error_pattern_size_mismatch": "Pattern size ({width}x{height}) does not match selected size ({size}x{size}).",
        "error_pattern_invalid_char": "Invalid character '{char}' in pattern at line {line}, column {col}. Allowed: '{allowed}'",
        "error_pattern_empty": "Pattern is empty.",
        "error_pattern_line_length": "Line {line} has wrong length. Expected: {expected}, found: {found}.",
        "warning_percent_sum": "The sum of percentages is {sum:.1f}%.",
        "question_normalize_percent": "The sum of percentages is {sum:.1f}%.\nNormalize values to continue?",
        "error_percent_sum_zero": "Sum of percentages is zero or negative.",
        "info_save_success": "Image successfully saved as '{filename}'.",
        "color_settings_label_char": "'{char}':",
        "color_settings_label_percent": "%:",
        "color_settings_button_pick": "?",
    },
    "de": {
        "window_title": "Pixel Muster Generator v4",
        "file_menu": "Datei",
        "file_menu_save": "Bild speichern",
        "file_menu_exit": "Beenden",
        "lang_menu": "Sprache",
        "lang_menu_german": "Deutsch",
        "lang_menu_english": "Englisch",
        "help_menu": "Hilfe",
        "help_menu_about": "Über",
        "about_title": "Über Pixel Muster Generator",
        "about_text": "Pixel Muster Generator v4\n\nEin Werkzeug zum Erstellen und Visualisieren von Pixel-Mustern.\nErstellt mit Python und Tkinter.",
        "label_size": "Bildgröße (Pixel)",
        "radio_16": "16x16",
        "radio_32": "32x32",
        "label_num_colors": "Anzahl Farben",
        "label_max_colors": "(1 - {max})",
        "label_color_settings": "Farbeinstellungen",
        "label_percentage_sum_base": "Summe",
        "label_percentage_sum_ok": "OK",
        "label_percentage_sum_needed": "benötigt",
        "label_percentage_sum_too_much": "zu viel",
        "label_percentage_sum_invalid": "Ungültige Eingabe",
        "label_pattern": "Muster",
        "label_pattern_size": "Größe:",
        "button_random": "Zufalls-Muster",
        "button_preview": "Vorschau",
        "label_preview": "Vorschau",
        "label_filename": "Datei:",
        "button_save": "Speichern",
        "color_picker_title": "Farbe wählen für '{char}'",
        "error_title": "Fehler",
        "warning_title": "Warnung",
        "info_title": "Info",
        "error_invalid_hex": "Ungültiger Hex-Code '{hex}' für Farbe '{char}'.",
        "error_invalid_percent": "Ungültige Prozentzahl für Farbe '{char}'.",
        "error_invalid_num_colors": "Anzahl der Farben muss zwischen 1 und {max} liegen.",
        "error_no_image_generated": "Es wurde noch kein Bild generiert.",
        "error_save_failed": "Konnte Bild nicht speichern:\n{error}",
        "error_save_no_filename": "Bitte Dateinamen eingeben.",
        "error_pattern_size_mismatch": "Mustergröße ({width}x{height}) passt nicht zur Auswahl ({size}x{size}).",
        "error_pattern_invalid_char": "Ungültiges Zeichen '{char}' in Muster Zeile {line}, Spalte {col}. Erlaubt: '{allowed}'",
        "error_pattern_empty": "Muster ist leer.",
        "error_pattern_line_length": "Zeile {line} hat falsche Länge. Erwartet: {expected}, gefunden: {found}.",
        "warning_percent_sum": "Die Summe der Prozente ist {sum:.1f}%.",
        "question_normalize_percent": "Die Summe der Prozente ist {sum:.1f}%.\nSollen die Werte zum Fortfahren normalisiert werden?",
        "error_percent_sum_zero": "Summe der Prozente ist 0 oder negativ.",
        "info_save_success": "Bild erfolgreich gespeichert als '{filename}'.",
        "color_settings_label_char": "'{char}':",
        "color_settings_label_percent": "%:",
        "color_settings_button_pick": "?",
    }
}


# --- Kernlogik (angepasst für Fehler-Keys) ---
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    if len(hex_code) != 6: raise ValueError("hex_length") # Schlüssel für Übersetzung
    try: return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    except ValueError: raise ValueError("hex_conversion") # Schlüssel

def generate_pil_image_from_pattern(size, num_colors, color_hex_list, pattern_string, trans_func):
    if len(color_hex_list) != num_colors: raise ValueError("color_count_mismatch")

    valid_chars = COLOR_CHARS[:num_colors]
    char_to_hex_map = {}
    char_to_rgb_map = {}
    try:
        for i, char in enumerate(valid_chars):
            hex_color = color_hex_list[i].strip()
            if not hex_color.startswith('#'): hex_color = '#' + hex_color
            try:
                rgb_color = hex_to_rgb(hex_color)
            except ValueError as e_inner:
                 # Wirf Fehler mit Kontext für Übersetzung
                 raise ValueError(f"invalid_hex:{e_inner.args[0]}:{widgets['hex_entry'].get()}:{char}")
            char_to_hex_map[char] = hex_color
            char_to_rgb_map[char] = rgb_color
    except IndexError: raise ValueError("color_list_too_short")

    pattern_lines = pattern_string.strip().split('\n')
    if not pattern_lines or not pattern_lines[0]: raise ValueError("pattern_empty")
    expected_height, expected_width = size, size
    if len(pattern_lines) != expected_height: raise ValueError(f"pattern_height_mismatch:{len(pattern_lines)}:{expected_height}")

    pixel_data = []
    for y, line in enumerate(pattern_lines):
        cleaned_line = line.rstrip()
        if len(cleaned_line) != expected_width: raise ValueError(f"pattern_line_length:{y+1}:{expected_width}:{len(cleaned_line)}")
        for x, char in enumerate(cleaned_line):
            if char not in valid_chars: raise ValueError(f"pattern_invalid_char:{char}:{y+1}:{x+1}:{valid_chars}")
            pixel_data.append(char_to_rgb_map[char])

    if len(pixel_data) != size * size: raise ValueError("internal_pixel_count")
    img = Image.new('RGB', (size, size))
    img.putdata(pixel_data)
    return img, char_to_hex_map


# --- GUI Klasse ---
class PatternApp:
    def __init__(self, master):
        self.master = master
        # self.master.title("Pixel Pattern Generator") # Wird jetzt durch Übersetzung gesetzt

        # --- Icon setzen ---
        try:
            # Versuche, ein Icon zu laden (optional)
            icon_file = "smaragt_erz.png" # Stelle sicher, dass diese Datei existiert
            if os.path.exists(icon_file):
                pil_icon = Image.open(icon_file)
                tk_icon = ImageTk.PhotoImage(pil_icon)
                master.iconphoto(True, tk_icon)
        except Exception as e:
            print(f"WARNUNG: Icon konnte nicht geladen werden: {e}")

        # Spracheinstellung
        self.current_language = tk.StringVar(value=LANG_DEFAULT)
        self.current_language.trace_add("write", self.switch_language)

        self.pil_image = None
        self.tk_image = None
        self.char_color_map = {}
        self.color_settings_widgets = []

        self.size_var = tk.IntVar(value=DEFAULT_SIZE)
        self.num_colors_var = tk.IntVar(value=3)
        self.num_colors_var.trace_add("write", self.update_color_settings_ui)

        self.percentage_sum_info_var = tk.StringVar() # Initialwert wird in update_percentage_sum gesetzt

        style = ttk.Style()
        # Style-Konfigurationen...

        # --- Menüleiste ---
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # Datei-Menü
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.translate('file_menu'), menu=self.file_menu)
        self.file_menu.add_command(label=self.translate('file_menu_save'), command=self.save_image, accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.translate('file_menu_exit'), command=master.quit)
        master.bind_all("<Control-s>", lambda e: self.save_image()) # Shortcut

        # Sprach-Menü
        self.lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.translate('lang_menu'), menu=self.lang_menu)
        self.lang_menu.add_radiobutton(label=self.translate('lang_menu_german'), variable=self.current_language, value='de')
        self.lang_menu.add_radiobutton(label=self.translate('lang_menu_english'), variable=self.current_language, value='en')

        # Hilfe-Menü
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.translate('help_menu'), menu=self.help_menu)
        self.help_menu.add_command(label=self.translate('help_menu_about'), command=self.show_about_dialog)


        # --- Hauptlayout ---
        master.geometry("900x800")
        master.columnconfigure(0, weight=1, minsize=350)
        master.columnconfigure(1, weight=2, minsize=400)
        master.rowconfigure(0, weight=1)

        # Linke Spalte
        self.left_frame = ttk.Frame(master, padding="10")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.rowconfigure(2, weight=1) # Color settings expand

        self.size_frame = ttk.LabelFrame(self.left_frame, text=self.translate('label_size'), padding="5")
        self.size_frame.grid(row=0, column=0, sticky="ew", pady=(0,5))
        self.radio_16 = ttk.Radiobutton(self.size_frame, text=self.translate('radio_16'), variable=self.size_var, value=16)
        self.radio_16.pack(side=tk.LEFT, padx=5)
        self.radio_32 = ttk.Radiobutton(self.size_frame, text=self.translate('radio_32'), variable=self.size_var, value=32)
        self.radio_32.pack(side=tk.LEFT, padx=5)

        self.num_colors_frame = ttk.LabelFrame(self.left_frame, text=self.translate('label_num_colors'), padding="5")
        self.num_colors_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.num_colors_spinbox = ttk.Spinbox(self.num_colors_frame, from_=1, to=MAX_COLORS, width=5, textvariable=self.num_colors_var, command=self.update_color_settings_ui)
        self.num_colors_spinbox.pack(side=tk.LEFT, padx=5)
        self.max_colors_label = ttk.Label(self.num_colors_frame, text=self.translate('label_max_colors', max=MAX_COLORS))
        self.max_colors_label.pack(side=tk.LEFT)

        self.color_outer_frame = ttk.LabelFrame(self.left_frame, text=self.translate('label_color_settings'), padding="5")
        self.color_outer_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        self.color_canvas = tk.Canvas(self.color_outer_frame, borderwidth=0)
        self.color_settings_frame = ttk.Frame(self.color_canvas, padding="5") # Frame im Canvas
        self.color_scrollbar = ttk.Scrollbar(self.color_outer_frame, orient="vertical", command=self.color_canvas.yview)
        self.color_canvas.configure(yscrollcommand=self.color_scrollbar.set)
        self.color_scrollbar.pack(side="right", fill="y")
        self.color_canvas.pack(side="left", fill="both", expand=True)
        self.color_canvas_window = self.color_canvas.create_window((0, 0), window=self.color_settings_frame, anchor="nw")
        self.color_settings_frame.bind("<Configure>", lambda e: self.color_canvas.configure(scrollregion=self.color_canvas.bbox("all")))
        self.color_canvas.bind('<Enter>', lambda e: self._bind_mousewheel(e, self.color_canvas))
        self.color_canvas.bind('<Leave>', lambda e: self._unbind_mousewheel(e, self.color_canvas))

        self.percentage_sum_label = ttk.Label(self.left_frame, textvariable=self.percentage_sum_info_var, relief="sunken", padding=3)
        self.percentage_sum_label.grid(row=3, column=0, sticky="ew", pady=(5,0))

        # Rechte Spalte
        self.right_frame = ttk.Frame(master, padding="10")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.rowconfigure(0, weight=2) # Pattern
        self.right_frame.rowconfigure(2, weight=1) # Preview

        self.pattern_frame = ttk.LabelFrame(self.right_frame, text=self.translate('label_pattern'), padding="5")
        self.pattern_frame.grid(row=0, column=0, sticky="nsew", pady=(0,5))
        self.pattern_text = scrolledtext.ScrolledText(self.pattern_frame, width=45, height=18, wrap=tk.NONE)
        self.pattern_text.pack(fill="both", expand=True)
        self.pattern_text.bind("<KeyRelease>", self.update_pattern_size_info)
        self.pattern_size_label = ttk.Label(self.pattern_frame, text=f"{self.translate('label_pattern_size')} 0x0")
        self.pattern_size_label.pack(anchor="w", pady=(3,0))

        self.pattern_button_frame = ttk.Frame(self.right_frame)
        self.pattern_button_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.random_button = ttk.Button(self.pattern_button_frame, text=self.translate('button_random'), command=self.generate_random_pattern)
        self.random_button.pack(side=tk.LEFT, padx=(0,5), expand=True, fill="x")
        self.preview_button = ttk.Button(self.pattern_button_frame, text=self.translate('button_preview'), command=self.update_preview)
        self.preview_button.pack(side=tk.LEFT, padx=(5,0), expand=True, fill="x")

        self.preview_display_frame = ttk.LabelFrame(self.right_frame, text=self.translate('label_preview'), padding="5")
        self.preview_display_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        self.preview_canvas = tk.Canvas(self.preview_display_frame, bg="lightgrey", width=256, height=256)
        self.preview_canvas.pack(pady=5, expand=True)

        self.save_frame = ttk.Frame(self.right_frame)
        self.save_frame.grid(row=3, column=0, sticky="ew", pady=(10,0))
        self.filename_label = ttk.Label(self.save_frame, text=self.translate('label_filename'))
        self.filename_label.pack(side=tk.LEFT, padx=5)
        self.filename_entry = ttk.Entry(self.save_frame, width=25)
        self.filename_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        self.filename_entry.insert(0, "tile.png")
        self.save_button = ttk.Button(self.save_frame, text=self.translate('button_save'), command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Initiale UI-Sprache setzen und Widgets erstellen
        self.update_ui_language()
        self.update_color_settings_ui()
        self.update_pattern_size_info()

    # --- Übersetzungsfunktion ---
    def translate(self, key, **kwargs):
        """ Holt den übersetzten Text für einen Schlüssel. """
        lang = self.current_language.get()
        try:
            text = translations[lang][key]
            return text.format(**kwargs) # Ermöglicht Platzhalter wie {max}
        except KeyError:
            # Fallback auf Englisch
            try:
                text = translations[LANG_FALLBACK][key]
                print(f"WARNUNG: Schlüssel '{key}' fehlt in '{lang}', verwende Fallback '{LANG_FALLBACK}'.")
                return text.format(**kwargs)
            except KeyError:
                print(f"FEHLER: Schlüssel '{key}' fehlt auch im Fallback '{LANG_FALLBACK}'.")
                return key # Gib Schlüssel als Indikator zurück
        except Exception as e:
             print(f"FEHLER bei Übersetzung von '{key}': {e}")
             return key

    # --- Sprachwechsel ---
    def switch_language(self, *args):
        """ Wird aufgerufen, wenn die Sprache geändert wird. """
        print(f"Sprache geändert auf: {self.current_language.get()}")
        self.update_ui_language()
        # Neuaufbau der dynamischen Teile der UI (Farbeinstellungen)
        self.update_color_settings_ui()

    def update_ui_language(self):
        """ Aktualisiert alle Texte in der UI zur aktuellen Sprache. """
        # Fenstertitel
        self.master.title(self.translate('window_title'))

        # Menüs
        self.menu_bar.entryconfig(1, label=self.translate('file_menu'))
        self.file_menu.entryconfig(0, label=self.translate('file_menu_save'))
        self.file_menu.entryconfig(2, label=self.translate('file_menu_exit'))
        self.menu_bar.entryconfig(2, label=self.translate('lang_menu'))
        self.lang_menu.entryconfig(0, label=self.translate('lang_menu_german'))
        self.lang_menu.entryconfig(1, label=self.translate('lang_menu_english'))
        self.menu_bar.entryconfig(3, label=self.translate('help_menu'))
        self.help_menu.entryconfig(0, label=self.translate('help_menu_about'))


        # Linke Spalte Widgets
        self.size_frame.config(text=self.translate('label_size'))
        self.radio_16.config(text=self.translate('radio_16'))
        self.radio_32.config(text=self.translate('radio_32'))
        self.num_colors_frame.config(text=self.translate('label_num_colors'))
        self.max_colors_label.config(text=self.translate('label_max_colors', max=MAX_COLORS))
        self.color_outer_frame.config(text=self.translate('label_color_settings'))
        # Prozent-Summen-Label wird von update_percentage_sum_info aktualisiert

        # Rechte Spalte Widgets
        self.pattern_frame.config(text=self.translate('label_pattern'))
        # Pattern-Größe-Label wird von update_pattern_size_info aktualisiert
        self.random_button.config(text=self.translate('button_random'))
        self.preview_button.config(text=self.translate('button_preview'))
        self.preview_display_frame.config(text=self.translate('label_preview'))
        self.filename_label.config(text=self.translate('label_filename'))
        self.save_button.config(text=self.translate('button_save'))

        # Aktualisiere dynamische Labels
        self.update_pattern_size_info()
        self.update_percentage_sum_info()


    def show_about_dialog(self):
        """Zeigt den 'Über'-Dialog an."""
        messagebox.showinfo(
            self.translate('about_title'),
            self.translate('about_text')
        )

    # --- Mausrad-Binding ---
    def _bind_mousewheel(self, event, widget):
        widget.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, widget))

    def _unbind_mousewheel(self, event, widget):
        widget.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # --- UI Update Funktionen ---
    def update_pattern_size_info(self, event=None):
        content = self.pattern_text.get("1.0", tk.END).strip()
        if not content: width, height = 0, 0
        else:
            lines = content.split('\n')
            height = len(lines)
            width = len(lines[0].rstrip()) if height > 0 else 0
        self.pattern_size_label.config(text=f"{self.translate('label_pattern_size')} {width}x{height}")

    def update_color_settings_ui(self, *args):
        for widget_dict in self.color_settings_widgets: widget_dict['frame'].destroy()
        self.color_settings_widgets.clear()
        try:
            num_colors = self.num_colors_var.get()
            if not 1 <= num_colors <= MAX_COLORS:
                num_colors = max(1, min(MAX_COLORS, num_colors)); self.num_colors_var.set(num_colors)
        except tk.TclError: return

        default_perc = 100.0 / num_colors if num_colors > 0 else 0

        for i in range(num_colors):
            char = COLOR_CHARS[i]
            # Nimm vorherige Farbe, wenn vorhanden, sonst Default
            previous_hex = DEFAULT_COLORS[i % len(DEFAULT_COLORS)] # Default
            if hasattr(self, '_previous_colors') and i < len(self._previous_colors):
                 previous_hex = self._previous_colors[i]

            frame = ttk.Frame(self.color_settings_frame)
            frame.pack(fill="x", pady=3)

            ttk.Label(frame, text=self.translate('color_settings_label_char', char=char), width=4).pack(side=tk.LEFT, padx=(0, 5))
            color_box = tk.Label(frame, text="", bg=previous_hex, width=2, height=1, relief="sunken", borderwidth=1)
            color_box.pack(side=tk.LEFT, padx=5)
            hex_entry = ttk.Entry(frame, width=8)
            hex_entry.insert(0, previous_hex)
            hex_entry.pack(side=tk.LEFT, padx=5)
            hex_entry.bind("<FocusOut>", lambda e, idx=i: self.update_hex_entry_change(idx))
            hex_entry.bind("<Return>", lambda e, idx=i: self.update_hex_entry_change(idx))
            pick_button = ttk.Button(frame, text=self.translate('color_settings_button_pick'), width=2, command=lambda idx=i: self.pick_color(idx))
            pick_button.pack(side=tk.LEFT, padx=5)

            ttk.Label(frame, text=self.translate('color_settings_label_percent')).pack(side=tk.LEFT, padx=(10, 2))
            # Nimm vorherigen Prozentwert, wenn vorhanden, sonst Default
            previous_perc = f"{default_perc:.1f}"
            if hasattr(self, '_previous_percentages') and i < len(self._previous_percentages):
                 previous_perc = self._previous_percentages[i]
            perc_var = tk.StringVar(value=previous_perc)

            perc_entry = ttk.Entry(frame, width=6, textvariable=perc_var)
            perc_entry.pack(side=tk.LEFT, padx=2)
            perc_var.trace_add("write", self.update_percentage_sum_info)
            perc_entry.bind("<KeyRelease>", self.update_percentage_sum_info)

            widget_refs = {'frame': frame, 'char': char, 'hex_entry': hex_entry, 'color_box': color_box, 'perc_entry': perc_entry, 'perc_var': perc_var}
            self.color_settings_widgets.append(widget_refs)
            # Korrigiere die Farbe der Box initial, falls der Hex-Code ungültig war
            self.update_hex_entry_change(i, update_main_entry=False) # Nicht das Hauptfeld updaten

        self.update_percentage_sum_info()
        # Speichere aktuelle Farben/Prozente für den nächsten Neuaufbau
        self._save_current_color_settings_state()


    def _save_current_color_settings_state(self):
        """ Speichert die aktuellen Hex- und Prozentwerte intern. """
        self._previous_colors = [w['hex_entry'].get() for w in self.color_settings_widgets]
        self._previous_percentages = [w['perc_var'].get() for w in self.color_settings_widgets]


    def update_hex_entry_change(self, index, update_main_entry=True):
        if not (0 <= index < len(self.color_settings_widgets)): return
        widgets = self.color_settings_widgets[index]
        hex_entry = widgets['hex_entry']
        color_box = widgets['color_box']
        new_hex = hex_entry.get().strip()
        if not new_hex.startswith('#'): new_hex = '#' + new_hex
        try:
             hex_to_rgb(new_hex)
             color_box.config(bg=new_hex)
             hex_entry.delete(0, tk.END); hex_entry.insert(0, new_hex) # Format korrigieren
             # if update_main_entry: self.update_main_color_entry_from_widgets() # Nicht mehr benötigt
        except ValueError:
             color_box.config(bg="SystemButtonFace")


    def pick_color(self, index):
        if not (0 <= index < len(self.color_settings_widgets)): return
        widgets = self.color_settings_widgets[index]
        result = colorchooser.askcolor(initialcolor=widgets['hex_entry'].get(),
                                       title=self.translate('color_picker_title', char=widgets['char']))
        if result and result[1]:
            widgets['hex_entry'].delete(0, tk.END); widgets['hex_entry'].insert(0, result[1])
            widgets['color_box'].config(bg=result[1])
            # self.update_main_color_entry_from_widgets() # Nicht mehr benötigt


    def update_percentage_sum_info(self, *args):
        total_perc = 0.0
        valid = True
        for widgets in self.color_settings_widgets:
            try:
                perc = float(widgets['perc_var'].get()); total_perc += perc
                if perc < 0: valid = False; break
            except (ValueError, tk.TclError): valid = False; break

        base = self.translate('label_percentage_sum_base')
        if not valid: info = self.translate('label_percentage_sum_invalid')
        else:
            diff = total_perc - 100.0
            if abs(diff) <= 0.1: status = self.translate('label_percentage_sum_ok')
            elif diff > 0: status = f"(+{diff:.1f}% {self.translate('label_percentage_sum_too_much')})"
            else: status = f"({diff:.1f}% {self.translate('label_percentage_sum_needed')})"
            info = f"{total_perc:.1f}% {status}"
        self.percentage_sum_info_var.set(f"{base}: {info}")


    def get_current_color_settings(self):
        color_list, percentages = [], []
        valid = True
        for i, widgets in enumerate(self.color_settings_widgets):
            hex_color = widgets['hex_entry'].get().strip();
            if not hex_color.startswith('#'): hex_color = '#' + hex_color
            try: hex_to_rgb(hex_color); color_list.append(hex_color)
            except ValueError:
                self.show_translated_error("error_invalid_hex", hex=widgets['hex_entry'].get(), char=widgets['char'])
                valid = False; break
            try:
                perc = float(widgets['perc_var'].get()); percentages.append(perc)
                if perc < 0: raise ValueError()
            except ValueError:
                self.show_translated_error("error_invalid_percent", char=widgets['char'])
                valid = False; break
        return (color_list, percentages) if valid else (None, None)

    # --- Logikfunktionen (angepasst für Fehlerübersetzung) ---
    def generate_random_pattern(self):
        try:
            size = self.size_var.get(); num_colors = self.num_colors_var.get()
            color_list, percentages = self.get_current_color_settings()
            if color_list is None: return
            if num_colors != len(color_list): raise ValueError("internal_color_widget_mismatch") # Interner Fehler

            total_perc = sum(percentages)
            if not (99.9 < total_perc < 100.1):
                 resp = messagebox.askyesno(self.translate('warning_title'),
                                self.translate('question_normalize_percent', sum=total_perc), icon='warning')
                 if not resp: return
                 if total_perc <= 0: self.show_translated_error("error_percent_sum_zero"); return
                 percentages = [(p / total_perc) * 100 for p in percentages]
                 for i, p_val in enumerate(percentages): self.color_settings_widgets[i]['perc_var'].set(f"{p_val:.1f}")

            population = list(COLOR_CHARS[:num_colors]); weights = percentages
            total_pixels = size * size
            random_chars = random.choices(population, weights=weights, k=total_pixels)
            pattern_lines = ["".join(random_chars[i:i+size]) for i in range(0, total_pixels, size)]
            self.pattern_text.delete("1.0", tk.END); self.pattern_text.insert("1.0", "\n".join(pattern_lines))
            self.update_pattern_size_info()
        except (tk.TclError, ValueError) as e: self.show_translated_error(str(e)) # Schlüssel oder Standardfehler
        except Exception as e: self.show_translated_error(str(e), title='Unerwarteter Fehler')


    def update_preview(self):
        try:
            size = self.size_var.get(); num_colors = self.num_colors_var.get()
            pattern = self.pattern_text.get("1.0", tk.END).strip()
            color_list, _ = self.get_current_color_settings()
            if color_list is None: self.clear_preview_and_disable_save(); return
            if not pattern: self.clear_preview_and_disable_save(); return

            self.pil_image, self.char_color_map = generate_pil_image_from_pattern(size, num_colors, color_list, pattern, self.translate)

            preview_size = 256; w, h = self.pil_image.size
            if w > 0 and h > 0:
                scale = min(preview_size / w, preview_size / h)
                new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
                resized_pil_image = self.pil_image.resize((new_w, new_h), Image.NEAREST)
            else: resized_pil_image = self.pil_image
            self.tk_image = ImageTk.PhotoImage(resized_pil_image)

            self.preview_canvas.delete("all"); canvas_w = self.preview_canvas.winfo_width(); canvas_h = self.preview_canvas.winfo_height()
            if canvas_w <= 1: canvas_w = preview_size;
            if canvas_h <= 1: canvas_h = preview_size;
            x_pos, y_pos = (canvas_w - new_w) // 2, (canvas_h - new_h) // 2
            self.preview_canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.tk_image)
            self.save_button.config(state=tk.NORMAL)
        except (ValueError, tk.TclError, IndexError) as e:
            # Versuche, den Fehler zu übersetzen, wenn der key im Fehlerstring enthalten ist
            error_key = str(e)
            error_parts = error_key.split(':')
            params = {}
            # Zerlege Fehlerstring in Schlüssel und Parameter
            if len(error_parts) > 1 and error_parts[0] in translations[self.current_language.get()]:
                 key = error_parts[0]
                 if key == "pattern_invalid_char": params = {'char': error_parts[1], 'line': error_parts[2], 'col': error_parts[3], 'allowed': error_parts[4]}
                 elif key == "pattern_line_length": params = {'line': error_parts[1], 'expected': error_parts[2], 'found': error_parts[3]}
                 elif key == "pattern_height_mismatch": params = {'found': error_parts[1], 'expected': error_parts[2]}
                 elif key == "invalid_hex": params = {'type': error_parts[1], 'hex': error_parts[2], 'char': error_parts[3]}
                 # ... füge hier weitere spezifische Fehler-Key-Parsings hinzu
                 self.show_translated_error(key, **params)
            else:
                 self.show_translated_error(error_key) # Zeige Originalfehler oder generischen Key
            self.clear_preview_and_disable_save()
        except Exception as e:
             self.show_translated_error(str(e), title='Unerwarteter Fehler')
             self.clear_preview_and_disable_save()


    def show_translated_error(self, error_key, title_key='error_title', **kwargs):
         """ Zeigt eine übersetzte Fehlermeldung an. """
         title = self.translate(title_key)
         message = self.translate(error_key, **kwargs)
         messagebox.showerror(title, message)


    def clear_preview_and_disable_save(self):
        self.pil_image = None; self.tk_image = None
        self.preview_canvas.delete("all"); self.save_button.config(state=tk.DISABLED)


    def save_image(self):
        if self.pil_image:
            filename = self.filename_entry.get()
            if not filename: self.show_translated_error("error_save_no_filename"); return
            if not any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']): filename += ".png"
            try:
                self.pil_image.save(filename, "PNG")
                messagebox.showinfo(self.translate('info_title'), self.translate('info_save_success', filename=filename))
            except Exception as e: self.show_translated_error("error_save_failed", error=e)
        else: self.show_translated_error("error_no_image_generated")


# --- Hauptprogramm ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PatternApp(root)
    root.mainloop()