import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import webbrowser
import difflib
import folium

# 1. إضافة كلاس المسجد (Mosque Class)
class Mosque:
    """كلاس لتمثيل كائن المسجد، يفي بمتطلب B."""
    def __init__(self, id, name, type, address, coordinates, imam_name):
        # للتأكد من أن ID هو رقم قبل الإنشاء
        self.id = int(id)
        self.name = name
        self.type = type
        self.address = address
        self.coordinates = coordinates
        self.imam_name = imam_name

    def to_tuple(self):
        """لتحويل كائن المسجد إلى صف (Tuple) جاهز للإدخال في قاعدة البيانات."""
        return (self.id, self.name, self.type, self.address, self.coordinates, self.imam_name)
    
    def __str__(self):
        """لتسهيل عرض الكائن في ListBox."""
        return f"ID: {self.id}, Name: {self.name}, Type: {self.type}, Imam: {self.imam_name}, Coords: {self.coordinates}"

class MosqueDB:
    def __init__(self):
        self.conn = sqlite3.connect('mosques.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Mosq (
                ID INTEGER PRIMARY KEY,
                Name TEXT,
                Type TEXT,
                Address TEXT,
                Coordinates TEXT,
                Imam_name TEXT
            )
        ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def Display(self):
        self.cursor.execute("SELECT * FROM Mosq")
        records = self.cursor.fetchall()
        return records

    def Search(self, name):
        self.cursor.execute("SELECT * FROM Mosq WHERE Name=?", (name,))
        record = self.cursor.fetchone()
        return record

    # 2. تعديل دالة Insert لتقبل كائن Mosque
    def Insert(self, mosque_obj):
        if not isinstance(mosque_obj, Mosque):
            raise TypeError("Expected a Mosque object.")
        
        self.cursor.execute("INSERT INTO Mosq VALUES (?, ?, ?, ?, ?, ?)",
                            mosque_obj.to_tuple())
        self.conn.commit()

    def Delete(self, id):
        self.cursor.execute("DELETE FROM Mosq WHERE ID=?", (id,))
        self.conn.commit()

    def Update(self, name, new_imam_name):
        self.cursor.execute("UPDATE Mosq SET Imam_name=? WHERE Name=?", (new_imam_name, name))
        self.conn.commit()

class MosquesManagementSystem:
    def __init__(self, master):
        self.master = master
        master.title("CS492 Project 3: Mosques Management System")
        self.master.config(bg="#F0F8FF")

        self.db = MosqueDB()

        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.LabelFrame(self.master, text="Part 1: Input Fields", bg="#E0EEE0", fg="#2F4F4F", font=("Arial", 10, "bold"))
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        labels_data = [
            ("ID", "Number", "Entry"),
            ("Name", "Text", "Entry"),
            ("Type", "Text", "OptionMenue"),
            ("Address", "Text", "Entry"),
            ("Coordinates", "Text", "Entry"),
            ("Imam Name", "Text", "Entry")
        ]

        self.entries = {}
        for row, (text, data_type, widget_type) in enumerate(labels_data):
            tk.Label(input_frame, text=f"{text}:", bg="#E0EEE0", fg="#1E90FF").grid(row=row, column=0, padx=5, pady=2, sticky="w")
            if widget_type == "OptionMenue":
                self.entries[text] = tk.StringVar(input_frame)
                self.entries[text].set("Jummah")
                option_menu = tk.OptionMenu(input_frame, self.entries[text], "Jummah", "Normal")
                option_menu.config(bg="#FFFFFF")
                option_menu.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
            elif widget_type == "Entry":
                entry = tk.Entry(input_frame, width=40, bg="#FFFFFF")
                entry.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
                self.entries[text] = entry

        list_frame = tk.LabelFrame(self.master, text="Part 2: Data Records Display", bg="#ADD8E6", fg="#2F4F4F", font=("Arial", 10, "bold"))
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.listbox = tk.Listbox(list_frame, height=10, width=80, bg="#F5FFFA", fg="#000000")
        self.listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        button_frame = tk.LabelFrame(self.master, text="Part 3 & 4: Operations", bg="#B0E0E6", fg="#2F4F4F", font=("Arial", 10, "bold"))
        button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        buttons_data = [
            ("Display All", self.display_all, "#98FB98"),
            ("Add Entry", self.add_entry, "#98FB98"),
            ("Search By Name", self.search_by_name, "#ADD8E6"),
            ("Delete Entry (by ID)", self.delete_entry, "#F08080"),
            ("Update Entry", self.update_entry, "#FFD700"),
            ("Display on Map", self.display_on_map, "#DDA0DD")
        ]

        for text, command, color in buttons_data:
            button = tk.Button(button_frame, text=text, command=command, width=20, bg=color, fg="#333333", activebackground="#DCDCDC")
            button.pack(side="left", padx=5, pady=5)

    def clear_listbox(self):
        self.listbox.delete(0, tk.END)

    def display_all(self):
        self.clear_listbox()
        records = self.db.Display()
        # عرض البيانات
        for record in records:
            # يمكن تحويل الصف إلى كائن مسجد للعرض إذا أردت استخدام دالة __str__ في كلاس Mosque
            self.listbox.insert(tk.END, record) 
            # أو استخدام الكلاس الجديد: self.listbox.insert(tk.END, str(Mosque(*record)))

    # 3. تعديل دالة add_entry لإنشاء كائن Mosque
    def add_entry(self):
        try:
            id_str = self.entries["ID"].get()
            if not id_str.isdigit():
                 messagebox.showerror("Error", "ID must be a number.")
                 return
            
            # جمع البيانات من حقول الإدخال
            id = id_str
            name = self.entries["Name"].get()
            type = self.entries["Type"].get()
            address = self.entries["Address"].get()
            coordinates = self.entries["Coordinates"].get()
            imam_name = self.entries["Imam Name"].get()

            if not all([name, type, address, coordinates, imam_name]):
                messagebox.showerror("Error", "All fields must be filled.")
                return
            
            # إنشاء كائن المسجد (يُنفذ متطلب B)
            new_mosque = Mosque(id, name, type, address, coordinates, imam_name)

            # إدراج الكائن في قاعدة البيانات
            self.db.Insert(new_mosque)
            messagebox.showinfo("Success", f"Mosque '{name}' added successfully.")
            self.display_all()

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # باقي الدوال لم تتغير
    def search_by_name(self):
        self.clear_listbox()
        search_name = self.entries["Name"].get()

        if not search_name:
            messagebox.showerror("Error", "Enter a name to search.")
            return

        record = self.db.Search(search_name)
        if record:
            self.listbox.insert(tk.END, record)
        else:
            self.listbox.insert(tk.END, f"No exact match found for '{search_name}'.")

            all_records = self.db.Display()
            all_names = [r[1] for r in all_records]
            close_matches = difflib.get_close_matches(search_name, all_names, n=5, cutoff=0.6)

            if close_matches:
                self.listbox.insert(tk.END, "--- Closest Matches Found (Enhancement): ---")
                for match in close_matches:
                    self.listbox.insert(tk.END, f"Did you mean: {match}?")

    def delete_entry(self):
        try:
            id_to_delete_str = self.entries["ID"].get()
            if not id_to_delete_str or not id_to_delete_str.isdigit():
                messagebox.showerror("Error", "Enter the ID (number) to delete.")
                return

            self.db.Delete(int(id_to_delete_str))
            messagebox.showinfo("Success", f"Record with ID {id_to_delete_str} deleted.")
            self.display_all()

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def update_entry(self):
        mosque_name = self.entries["Name"].get()
        new_imam_name = self.entries["Imam Name"].get()

        if not mosque_name or not new_imam_name:
            messagebox.showerror("Error", "Enter the Mosque Name and the new Imam Name to update.")
            return

        record = self.db.Search(mosque_name)
        if record:
            self.db.Update(mosque_name, new_imam_name)
            messagebox.showinfo("Success", f"Imam Name for '{mosque_name}' updated to '{new_imam_name}'.")
            self.display_all()
        else:
            messagebox.showerror("Error", f"Mosque '{mosque_name}' not found for update.")

    def display_on_map(self):
        mosque_name = self.entries["Name"].get()

        if not mosque_name:
            messagebox.showerror("Error", "Enter the Mosque Name to display on map.")
            return

        record = self.db.Search(mosque_name)
        if record:
            try:
                coordinates_str = record[4]
                lat, lon = map(float, coordinates_str.split(','))

                m = folium.Map(location=[lat, lon], zoom_start=15)
                folium.Marker([lat, lon], popup=f"Mosque: {mosque_name}", tooltip="Location").add_to(m)

                map_filename = f"{mosque_name}_map.html"
                m.save(map_filename)
                webbrowser.open_new_tab(map_filename)

            except ValueError:
                messagebox.showerror("Error", "Invalid Coordinates format. Please use 'latitude,longitude' (e.g., 24.58,46.73).")
            except Exception as e:
                messagebox.showerror("Error", f"Map display error (Folium/Webbrowser): {e}")
        else:
            messagebox.showerror("Error", f"Mosque '{mosque_name}' not found. Cannot display map.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MosquesManagementSystem(root)
    root.mainloop()