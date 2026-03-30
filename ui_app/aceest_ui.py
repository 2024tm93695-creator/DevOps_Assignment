import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Flask API base URL
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5000')

class ACEestUIApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ACEest Fitness & Performance - UI Client")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a1a")

        self.current_client = None
        self.current_user = None

        # Programs for AI-style generation
        self.program_templates = {
            "Fat Loss": ["Full Body HIIT", "Circuit Training", "Cardio + Weights"],
            "Muscle Gain": ["Push/Pull/Legs", "Upper/Lower Split", "Full Body Strength"],
            "Beginner": ["Full Body 3x/week", "Light Strength + Mobility"]
        }

        self.programs = {
            "Fat Loss (FL) – 3 day": {"factor": 22, "desc": "3-day full-body fat loss"},
            "Fat Loss (FL) – 5 day": {"factor": 24, "desc": "5-day split, higher volume fat loss"},
            "Muscle Gain (MG) – PPL": {"factor": 35, "desc": "Push/Pull/Legs hypertrophy"},
            "Beginner (BG)": {"factor": 26, "desc": "3-day simple beginner full-body"},
        }

        self.login_screen()

    # ---------- LOGIN SCREEN ----------
    def login_screen(self):
        self.clear_root()
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(expand=True)

        tk.Label(frame, text="ACEest Login", font=("Arial", 24), fg="#d4af37", bg="#1a1a1a").pack(pady=20)

        tk.Label(frame, text="Username", fg="white", bg="#1a1a1a").pack(pady=5)
        self.username_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.username_var, bg="#333", fg="white").pack()

        tk.Label(frame, text="Password", fg="white", bg="#1a1a1a").pack(pady=5)
        self.password_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.password_var, show="*", bg="#333", fg="white").pack()

        ttk.Button(frame, text="Login", command=self.login).pack(pady=20)
        ttk.Button(frame, text="Skip Login (Demo)", command=self.skip_login).pack(pady=5)

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        # For demo purposes, accept any login
        if username and password:
            self.current_user = username
            self.current_role = "Admin"
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Please enter username and password")

    def skip_login(self):
        self.current_user = "Demo User"
        self.current_role = "Admin"
        self.dashboard()

    # ---------- DASHBOARD ----------
    def dashboard(self):
        self.clear_root()

        # Header
        header = tk.Label(self.root, text=f"ACEest Dashboard ({self.current_role})", font=("Arial", 24, "bold"), bg="#d4af37", fg="black", height=2)
        header.pack(fill="x")

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bg="#111111", fg="#d4af37", anchor="w")
        status_bar.pack(side="bottom", fill="x")

        # Left panel: Clients & program generator
        left = tk.Frame(self.root, bg="#1a1a1a", width=350)
        left.pack(side="left", fill="y", padx=10, pady=10)

        # Client selection
        tk.Label(left, text="Select Client", bg="#1a1a1a", fg="white").pack(pady=(5,0))
        self.client_list = ttk.Combobox(left, state="readonly")
        self.client_list.pack()
        self.client_list.bind("<<ComboboxSelected>>", self.load_client)
        self.refresh_client_list()

        # Client form fields
        tk.Label(left, text="Name", bg="#1a1a1a", fg="white").pack(pady=(10,0))
        self.name = tk.StringVar()
        tk.Entry(left, textvariable=self.name, bg="#333", fg="white").pack()

        tk.Label(left, text="Age", bg="#1a1a1a", fg="white").pack(pady=(5,0))
        self.age = tk.IntVar()
        tk.Entry(left, textvariable=self.age, bg="#333", fg="white").pack()

        tk.Label(left, text="Height (cm)", bg="#1a1a1a", fg="white").pack(pady=(5,0))
        self.height = tk.DoubleVar()
        tk.Entry(left, textvariable=self.height, bg="#333", fg="white").pack()

        tk.Label(left, text="Weight (kg)", bg="#1a1a1a", fg="white").pack(pady=(5,0))
        self.weight = tk.DoubleVar()
        tk.Entry(left, textvariable=self.weight, bg="#333", fg="white").pack()

        tk.Label(left, text="Program", bg="#1a1a1a", fg="white").pack(pady=(5,0))
        self.program = tk.StringVar()
        ttk.Combobox(left, textvariable=self.program, values=list(self.programs.keys()), state="readonly").pack()

        tk.Label(left, text="Target Weight (kg)", bg="#1a1a1a", fg="white").pack(pady=(10,0))
        self.target_weight = tk.DoubleVar()
        tk.Entry(left, textvariable=self.target_weight, bg="#333", fg="white").pack()

        tk.Label(left, text="Target Adherence %", bg="#1a1a1a", fg="white").pack(pady=(5,0))
        self.target_adherence = tk.IntVar()
        tk.Entry(left, textvariable=self.target_adherence, bg="#333", fg="white").pack()

        # Buttons
        ttk.Button(left, text="Save Client", command=self.save_client).pack(pady=5)
        ttk.Button(left, text="Load Client", command=self.load_client_data).pack(pady=5)
        ttk.Button(left, text="Generate AI Program", command=self.generate_program).pack(pady=5)
        ttk.Button(left, text="Log Workout", command=self.open_log_workout_window).pack(pady=5)
        ttk.Button(left, text="Log Body Metrics", command=self.open_log_metrics_window).pack(pady=5)
        ttk.Button(left, text="View Workout History", command=self.open_workout_history_window).pack(pady=5)

        # Trainer management
        ttk.Button(left, text="Manage Trainers", command=self.open_trainer_management).pack(pady=5)
        ttk.Button(left, text="Manage Subscriptions", command=self.open_subscription_management).pack(pady=5)

        # Right panel: Notebook with charts and workouts
        right = tk.Frame(self.root, bg="#1a1a1a")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill="both", expand=True)

        # Tab1: Summary & charts
        self.tab_summary = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(self.tab_summary, text="Client Summary")

        self.summary_text = tk.Text(self.tab_summary, bg="#111", fg="white", font=("Consolas", 11))
        self.summary_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Chart placeholder
        self.chart_frame = tk.Frame(self.tab_summary, bg="#1a1a1a")
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab2: Workouts & exercises
        self.tab_workouts = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(self.tab_workouts, text="Workouts & Exercises")
        self.setup_workout_tab()

        # Tab3: Analytics
        self.tab_analytics = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(self.tab_analytics, text="Progress & Analytics")
        self.setup_analytics_tab()

    # ---------- CLIENT MANAGEMENT ----------
    def refresh_client_list(self):
        try:
            response = requests.get(f"{API_BASE_URL}/api/members")
            if response.status_code == 200:
                members = response.json()
                names = [member['name'] for member in members]
                self.client_list["values"] = names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load clients: {str(e)}")

    def save_client(self):
        data = {
            "name": self.name.get(),
            "age": self.age.get(),
            "height": self.height.get(),
            "weight": self.weight.get(),
            "program": self.program.get(),
            "target_weight": self.target_weight.get(),
            "target_adherence": self.target_adherence.get()
        }

        try:
            response = requests.post(f"{API_BASE_URL}/api/members", json=data)
            if response.status_code == 201:
                messagebox.showinfo("Success", "Client saved successfully")
                self.refresh_client_list()
                self.set_status("Client saved")
            else:
                error = response.json().get('error', 'Unknown error')
                messagebox.showerror("Error", f"Failed to save client: {error}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save client: {str(e)}")

    def load_client_data(self):
        name = self.name.get()
        if not name:
            messagebox.showwarning("Warning", "Please enter a client name")
            return

        try:
            # First try to get by name from API (this might need a custom endpoint)
            response = requests.get(f"{API_BASE_URL}/api/members")
            if response.status_code == 200:
                members = response.json()
                member = next((m for m in members if m['name'] == name), None)
                if member:
                    self.populate_client_form(member)
                    self.current_client = name
                    self.refresh_summary()
                    self.refresh_workouts()
                    self.plot_charts()
                    self.set_status(f"Loaded client: {name}")
                else:
                    messagebox.showwarning("Not Found", f"Client {name} not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load client: {str(e)}")

    def load_client(self, event=None):
        name = self.client_list.get()
        if not name:
            return
        self.current_client = name
        self.name.set(name)
        self.load_client_data()

    def populate_client_form(self, member):
        self.name.set(member.get('name', ''))
        self.age.set(member.get('age', 0))
        self.height.set(member.get('height', 0.0))
        self.weight.set(member.get('weight', 0.0))
        self.program.set(member.get('program', ''))
        self.target_weight.set(member.get('target_weight', 0.0))
        self.target_adherence.set(member.get('target_adherence', 0))

    # ---------- AI-STYLE PROGRAM GENERATOR ----------
    def generate_program(self):
        if not self.current_client:
            messagebox.showwarning("No Client", "Select a client first")
            return

        import random
        program_type = random.choice(list(self.program_templates.keys()))
        program_detail = random.choice(self.program_templates[program_type])

        # Update the program field
        self.program.set(program_detail)
        messagebox.showinfo("Program Generated", f"Program for {self.current_client}: {program_detail}")
        self.set_status("Program generated")

    # ---------- SUMMARY & CHARTS ----------
    def refresh_summary(self):
        if not self.current_client:
            return

        try:
            response = requests.get(f"{API_BASE_URL}/api/members/{self.current_client}/summary")
            if response.status_code == 200:
                summary = response.json()
                text = f"""Name: {summary['member']['name']}
Age: {summary['member']['age']}
Height: {summary['member']['height']} cm
Weight: {summary['member']['weight']} kg
Program: {summary['member']['program']}
Calories: {summary['member']['calories']}
Target Weight: {summary['member']['target_weight']} kg
Target Adherence: {summary['member']['target_adherence']}%

BMI: {summary['bmi']}
Membership: {summary['member']['membership_status']}

Recent Progress: {len(summary['recent_progress'])} entries
Recent Workouts: {len(summary['recent_workouts'])} sessions"""

                self.summary_text.configure(state="normal")
                self.summary_text.delete("1.0", "end")
                self.summary_text.insert("end", text)
                self.summary_text.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load summary: {str(e)}")

    def plot_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        if not self.current_client:
            return

        # For demo, create a simple chart
        fig, ax = plt.subplots(figsize=(6, 3))
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        adherence = [85, 90, 88, 92]
        ax.plot(weeks, adherence, marker="o")
        ax.set_title("Weekly Adherence Trend")
        ax.set_ylabel("Adherence %")
        ax.set_ylim(0, 100)
        ax.grid(True)
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- WORKOUT MANAGEMENT ----------
    def setup_workout_tab(self):
        # Treeview for workouts
        columns = ("date", "type", "duration", "notes")
        self.tree_workouts = ttk.Treeview(self.tab_workouts, columns=columns, show="headings")
        for c in columns:
            self.tree_workouts.heading(c, c.title())
            self.tree_workouts.column(c, width=150)
        self.tree_workouts.pack(fill="both", expand=True)
        ttk.Button(self.tab_workouts, text="Add Workout", command=self.add_workout).pack(pady=5)
        ttk.Button(self.tab_workouts, text="Refresh", command=self.refresh_workouts).pack(pady=5)

    def refresh_workouts(self):
        for row in self.tree_workouts.get_children():
            self.tree_workouts.delete(row)
        if not self.current_client:
            return

        try:
            response = requests.get(f"{API_BASE_URL}/api/workouts?member={self.current_client}")
            if response.status_code == 200:
                workouts = response.json()
                for workout in workouts:
                    self.tree_workouts.insert("", "end", values=(
                        workout['date'],
                        workout['workout_type'],
                        workout['duration_min'],
                        workout['notes']
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load workouts: {str(e)}")

    def add_workout(self):
        if not self.current_client:
            messagebox.showwarning("No Client", "Select a client first")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Add Workout - {self.current_client}")
        win.geometry("500x600")
        win.configure(bg="#1a1a1a")

        # Workout details
        tk.Label(win, text="Date (YYYY-MM-DD)", fg="white", bg="#1a1a1a").pack(pady=5)
        date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(win, textvariable=date_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Workout Type", fg="white", bg="#1a1a1a").pack(pady=5)
        type_var = tk.StringVar()
        ttk.Combobox(win, textvariable=type_var,
                    values=["Strength", "Hypertrophy", "Cardio", "Mobility", "HIIT", "Yoga"],
                    state="readonly").pack()

        tk.Label(win, text="Duration (minutes)", fg="white", bg="#1a1a1a").pack(pady=5)
        dur_var = tk.IntVar(value=60)
        tk.Entry(win, textvariable=dur_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Notes", fg="white", bg="#1a1a1a").pack(pady=5)
        notes_var = tk.StringVar()
        tk.Entry(win, textvariable=notes_var, bg="#333", fg="white").pack()

        # Exercises section
        tk.Label(win, text="Exercises", fg="#d4af37", bg="#1a1a1a", font=("Arial", 12, "bold")).pack(pady=10)

        exercises_frame = tk.Frame(win, bg="#1a1a1a")
        exercises_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.exercises_data = []

        def add_exercise():
            exercise_win = tk.Toplevel(win)
            exercise_win.title("Add Exercise")
            exercise_win.geometry("300x250")
            exercise_win.configure(bg="#1a1a1a")

            tk.Label(exercise_win, text="Exercise Name", fg="white", bg="#1a1a1a").pack(pady=5)
            name_var = tk.StringVar()
            tk.Entry(exercise_win, textvariable=name_var, bg="#333", fg="white").pack()

            tk.Label(exercise_win, text="Sets", fg="white", bg="#1a1a1a").pack(pady=5)
            sets_var = tk.IntVar(value=3)
            tk.Entry(exercise_win, textvariable=sets_var, bg="#333", fg="white").pack()

            tk.Label(exercise_win, text="Reps", fg="white", bg="#1a1a1a").pack(pady=5)
            reps_var = tk.IntVar(value=10)
            tk.Entry(exercise_win, textvariable=reps_var, bg="#333", fg="white").pack()

            tk.Label(exercise_win, text="Weight (kg)", fg="white", bg="#1a1a1a").pack(pady=5)
            weight_var = tk.DoubleVar(value=0.0)
            tk.Entry(exercise_win, textvariable=weight_var, bg="#333", fg="white").pack()

            def save_exercise():
                self.exercises_data.append({
                    "name": name_var.get(),
                    "sets": sets_var.get(),
                    "reps": reps_var.get(),
                    "weight": weight_var.get()
                })
                exercise_win.destroy()
                update_exercises_list()

            ttk.Button(exercise_win, text="Save Exercise", command=save_exercise).pack(pady=10)

        ttk.Button(exercises_frame, text="Add Exercise", command=add_exercise).pack(pady=5)

        exercises_list = tk.Text(exercises_frame, bg="#111", fg="white", height=8, font=("Consolas", 9))
        exercises_list.pack(fill="both", expand=True)

        def update_exercises_list():
            exercises_list.delete("1.0", "end")
            for i, ex in enumerate(self.exercises_data, 1):
                exercises_list.insert("end", f"{i}. {ex['name']} - {ex['sets']}x{ex['reps']} @ {ex['weight']}kg\n")

        def save_workout():
            data = {
                "client_name": self.current_client,
                "date": date_var.get(),
                "workout_type": type_var.get(),
                "duration_min": dur_var.get(),
                "notes": notes_var.get(),
                "exercises": self.exercises_data
            }

            try:
                response = requests.post(f"{API_BASE_URL}/api/workouts", json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Workout saved successfully")
                    self.refresh_workouts()
                    win.destroy()
                    self.set_status("Workout logged")
                else:
                    error = response.json().get('error', 'Unknown error')
                    messagebox.showerror("Error", f"Failed to save workout: {error}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save workout: {str(e)}")

        ttk.Button(win, text="Save Workout", command=save_workout).pack(pady=10)

    # ---------- ANALYTICS TAB ----------
    def setup_analytics_tab(self):
        ttk.Button(self.tab_analytics, text="Adherence Chart", command=self.show_adherence_chart).pack(pady=10)
        ttk.Button(self.tab_analytics, text="Weight Trend Chart", command=self.show_weight_chart).pack(pady=10)
        ttk.Button(self.tab_analytics, text="BMI & Risk Info", command=self.show_bmi_info).pack(pady=10)

        self.analytics_frame = tk.Frame(self.tab_analytics, bg="#1a1a1a")
        self.analytics_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def show_adherence_chart(self):
        self.plot_charts()  # Reuse the summary chart

    def show_weight_chart(self):
        for widget in self.analytics_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 4))
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
        weights = [80.5, 79.8, 79.2, 78.5, 78.0]
        ax.plot(weeks, weights, marker="o", color="blue")
        ax.set_title("Weight Trend")
        ax.set_ylabel("Weight (kg)")
        ax.grid(True)
        canvas = FigureCanvasTkAgg(fig, self.analytics_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_bmi_info(self):
        if not self.current_client:
            messagebox.showwarning("No Client", "Select a client first")
            return

        try:
            response = requests.get(f"{API_BASE_URL}/api/members/{self.current_client}/summary")
            if response.status_code == 200:
                summary = response.json()
                bmi = summary['bmi']
                weight = summary['member']['weight']
                height = summary['member']['height']

                category = "Normal weight"
                if bmi < 18.5:
                    category = "Underweight"
                elif bmi >= 25:
                    category = "Overweight"
                elif bmi >= 30:
                    category = "Obese"

                info = f"""BMI Information for {self.current_client}

Current BMI: {bmi}
Category: {category}
Weight: {weight} kg
Height: {height} cm

BMI Categories:
- Underweight: < 18.5
- Normal weight: 18.5 - 24.9
- Overweight: 25 - 29.9
- Obese: ≥ 30"""

                messagebox.showinfo("BMI Information", info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get BMI info: {str(e)}")

    # ---------- ADDITIONAL WINDOWS ----------
    def open_log_workout_window(self):
        self.add_workout()

    def open_log_metrics_window(self):
        if not self.current_client:
            messagebox.showwarning("No Client", "Select a client first")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Log Body Metrics - {self.current_client}")
        win.geometry("300x300")
        win.configure(bg="#1a1a1a")

        tk.Label(win, text="Date (YYYY-MM-DD)", fg="white", bg="#1a1a1a").pack(pady=5)
        date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(win, textvariable=date_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Weight (kg)", fg="white", bg="#1a1a1a").pack(pady=5)
        weight_var = tk.DoubleVar()
        tk.Entry(win, textvariable=weight_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Waist (cm)", fg="white", bg="#1a1a1a").pack(pady=5)
        waist_var = tk.DoubleVar()
        tk.Entry(win, textvariable=waist_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Body Fat %", fg="white", bg="#1a1a1a").pack(pady=5)
        bodyfat_var = tk.DoubleVar()
        tk.Entry(win, textvariable=bodyfat_var, bg="#333", fg="white").pack()

        def save_metrics():
            # Note: This would need a metrics endpoint in the API
            messagebox.showinfo("Info", "Metrics logging would be implemented with API endpoint")
            win.destroy()

        ttk.Button(win, text="Save Metrics", command=save_metrics).pack(pady=10)

    def open_workout_history_window(self):
        if not self.current_client:
            messagebox.showwarning("No Client", "Select a client first")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Workout History - {self.current_client}")
        win.geometry("600x400")
        win.configure(bg="#1a1a1a")

        # Treeview for workout history
        columns = ("date", "type", "duration", "notes")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, c.title())
            tree.column(c, width=120)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Load workout history
        try:
            response = requests.get(f"{API_BASE_URL}/api/workouts?member={self.current_client}")
            if response.status_code == 200:
                workouts = response.json()
                for workout in workouts:
                    tree.insert("", "end", values=(
                        workout['date'],
                        workout['workout_type'],
                        workout['duration_min'],
                        workout['notes']
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load workout history: {str(e)}")

    def open_trainer_management(self):
        win = tk.Toplevel(self.root)
        win.title("Trainer Management")
        win.geometry("600x500")
        win.configure(bg="#1a1a1a")

        # Trainer list
        columns = ("name", "specialization", "experience", "email")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, c.title())
            tree.column(c, width=120)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Load trainers
        try:
            response = requests.get(f"{API_BASE_URL}/api/members/trainers")
            if response.status_code == 200:
                trainers = response.json()
                for trainer in trainers:
                    tree.insert("", "end", values=(
                        trainer['name'],
                        trainer['specialization'] or '',
                        trainer['experience_years'] or '',
                        trainer['email'] or ''
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load trainers: {str(e)}")

        # Buttons
        button_frame = tk.Frame(win, bg="#1a1a1a")
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Add Trainer", command=lambda: self.add_trainer(win, tree)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=lambda: self.refresh_trainers(tree)).pack(side="left", padx=5)

    def add_trainer(self, parent_win, tree):
        win = tk.Toplevel(parent_win)
        win.title("Add Trainer")
        win.geometry("400x300")
        win.configure(bg="#1a1a1a")

        tk.Label(win, text="Name", fg="white", bg="#1a1a1a").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(win, textvariable=name_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Specialization", fg="white", bg="#1a1a1a").pack(pady=5)
        spec_var = tk.StringVar()
        tk.Entry(win, textvariable=spec_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Experience (years)", fg="white", bg="#1a1a1a").pack(pady=5)
        exp_var = tk.IntVar()
        tk.Entry(win, textvariable=exp_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Email", fg="white", bg="#1a1a1a").pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(win, textvariable=email_var, bg="#333", fg="white").pack()

        def save_trainer():
            data = {
                "name": name_var.get(),
                "specialization": spec_var.get(),
                "experience_years": exp_var.get(),
                "email": email_var.get()
            }

            try:
                response = requests.post(f"{API_BASE_URL}/api/members/trainers", json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Trainer added successfully")
                    self.refresh_trainers(tree)
                    win.destroy()
                else:
                    error = response.json().get('error', 'Unknown error')
                    messagebox.showerror("Error", f"Failed to add trainer: {error}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add trainer: {str(e)}")

        ttk.Button(win, text="Save Trainer", command=save_trainer).pack(pady=10)

    def refresh_trainers(self, tree):
        for row in tree.get_children():
            tree.delete(row)

        try:
            response = requests.get(f"{API_BASE_URL}/api/members/trainers")
            if response.status_code == 200:
                trainers = response.json()
                for trainer in trainers:
                    tree.insert("", "end", values=(
                        trainer['name'],
                        trainer['specialization'] or '',
                        trainer['experience_years'] or '',
                        trainer['email'] or ''
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh trainers: {str(e)}")

    def open_subscription_management(self):
        win = tk.Toplevel(self.root)
        win.title("Subscription Management")
        win.geometry("700x500")
        win.configure(bg="#1a1a1a")

        # Subscription list
        columns = ("client", "plan", "start_date", "end_date", "fee", "status")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, c.title())
            tree.column(c, width=100)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Load subscriptions
        try:
            response = requests.get(f"{API_BASE_URL}/api/subscriptions")
            if response.status_code == 200:
                subscriptions = response.json()
                for sub in subscriptions:
                    tree.insert("", "end", values=(
                        sub['client_name'],
                        sub['plan_name'],
                        sub['start_date'],
                        sub['end_date'],
                        f"${sub['fee']}",
                        sub['status']
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subscriptions: {str(e)}")

        # Buttons
        button_frame = tk.Frame(win, bg="#1a1a1a")
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Add Subscription", command=lambda: self.add_subscription(win, tree)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=lambda: self.refresh_subscriptions(tree)).pack(side="left", padx=5)

    def add_subscription(self, parent_win, tree):
        win = tk.Toplevel(parent_win)
        win.title("Add Subscription")
        win.geometry("400x350")
        win.configure(bg="#1a1a1a")

        tk.Label(win, text="Client Name", fg="white", bg="#1a1a1a").pack(pady=5)
        client_var = tk.StringVar()
        tk.Entry(win, textvariable=client_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Plan Name", fg="white", bg="#1a1a1a").pack(pady=5)
        plan_var = tk.StringVar()
        ttk.Combobox(win, textvariable=plan_var,
                    values=["Basic", "Premium", "VIP", "Student", "Senior"],
                    state="readonly").pack()

        tk.Label(win, text="Start Date (YYYY-MM-DD)", fg="white", bg="#1a1a1a").pack(pady=5)
        start_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(win, textvariable=start_var, bg="#333", fg="white").pack()

        tk.Label(win, text="End Date (YYYY-MM-DD)", fg="white", bg="#1a1a1a").pack(pady=5)
        end_var = tk.StringVar(value=(date.today().replace(year=date.today().year + 1)).isoformat())
        tk.Entry(win, textvariable=end_var, bg="#333", fg="white").pack()

        def save_subscription():
            data = {
                "client_name": client_var.get(),
                "plan_name": plan_var.get(),
                "start_date": start_var.get(),
                "end_date": end_var.get()
            }

            try:
                response = requests.post(f"{API_BASE_URL}/api/subscriptions", json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Subscription added successfully")
                    self.refresh_subscriptions(tree)
                    win.destroy()
                else:
                    error = response.json().get('error', 'Unknown error')
                    messagebox.showerror("Error", f"Failed to add subscription: {error}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add subscription: {str(e)}")

        ttk.Button(win, text="Save Subscription", command=save_subscription).pack(pady=10)

    def refresh_subscriptions(self, tree):
        for row in tree.get_children():
            tree.delete(row)

        try:
            response = requests.get(f"{API_BASE_URL}/api/subscriptions")
            if response.status_code == 200:
                subscriptions = response.json()
                for sub in subscriptions:
                    tree.insert("", "end", values=(
                        sub['client_name'],
                        sub['plan_name'],
                        sub['start_date'],
                        sub['end_date'],
                        f"${sub['fee']}",
                        sub['status']
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh subscriptions: {str(e)}")

    # ---------- UTILITY METHODS ----------
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def set_status(self, text: str):
        self.status_var.set(text)

# ---------- RUN APPLICATION ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = ACEestUIApp(root)
    root.mainloop()