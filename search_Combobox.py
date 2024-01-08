import tkinter as tk
from tkinter import ttk
import re
class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, master=None, **kw):
        # Initialize the Combobox with the required parameters
        ttk.Combobox.__init__(self, master, **kw)

        self._set_autocomplete()

    def _set_autocomplete(self):
        # Create a popup window to show the search results
        self._popup_win = tk.Toplevel()
        self._popup_win.overrideredirect(True)  # No window decorations
        self._popup_win.withdraw()

        # Create a ListBox to show search results
        self._popup_list = tk.Listbox(self._popup_win)

        self._popup_list.pack(fill="both", expand=True)

        # Bind combobox key press event to search method
        self.bind('<KeyRelease>', self._search)
        self.bind('<Button-1>', self._reset_autocomplete)
        self._popup_list.bind('<ButtonRelease-1>', self._select_item)
        self._popup_list.bind('<Motion>', lambda event: self._popup_list.focus_set())


    def _reset_autocomplete(self, event):
        # Reset autocomplete and hide popup
        self._popup_list.delete(0, tk.END)
        self._popup_win.withdraw()

    def _search(self, event):
        data = self['values']
        if not data:
            return

        # Build search pattern
        pattern = event.widget.get().lower()
        pattern = pattern.replace('(', '\(').replace(')', '\)')  # Escape special characters
        pattern = r"(?i).*" + pattern + r".*"

        # Remove previous search results
        self._popup_list.delete(0, tk.END)

        # Search data and show results
        for item in data:
            if re.match(pattern, item):
                self._popup_list.insert(tk.END, item)

    # Show popup and reposition it
        if self._popup_list.size() > 0:
            x = self.winfo_x()
            y = self.winfo_y() + self.winfo_height()
            w = self.winfo_width()
            self._popup_win.geometry('{}x{}+{}+{}'.format(w, 150, x, y))
            self._popup_win.deiconify()
        else:
            self._popup_win.withdraw()


    def _select_item(self, event):
        # Set the value of the combobox to the selected item
        if self._popup_list.curselection():
            index = self._popup_list.curselection()[0]
            value = self._popup_list.get(index)
            self.set(value)
            self.icursor('end')  # Move cursor to end of text
        self._popup_win.withdraw()
