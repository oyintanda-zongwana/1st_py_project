import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import requests
from io import BytesIO

# Define single color scheme
COLORS = {
    'bg': '#FFFFFF',           # Pure white background
    'secondary_bg': '#F8FAFC', # Light gray for panels
    'accent': '#3B82F6',       # Bright blue accent
    'text': '#1E293B',         # Dark blue-gray text
    'secondary_text': '#64748B', # Lighter text
    'button_bg': '#3B82F6',    # Blue buttons
    'button_hover': '#2563EB', # Darker blue for hover
    'button_fg': '#FFFFFF',    # White text on buttons
    'border': '#E2E8F0',       # Light gray borders
}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
# print(voices[1].id)
engine.setProperty("voice", "voices[0].id")

def speak(audio):
    """Function to convert text to speech"""
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

def wishMe():
    """Function to greet the user based on time of day"""
    try:
        hour = datetime.datetime.now().hour
        greeting = "Good morning!" if hour < 12 else "Good Afternoon!" if hour < 18 else "Good Evening!"
        speak(greeting)
        speak("I am Project number 1 Sir and or Ma'am. Please tell me how I may help you?")
    except Exception as e:
        print(f"Error in wishMe function: {e}")

def takeCommand():
    """Function to take microphone input and return string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.RequestError:
            print("Could not request results; check your internet connection")
            return "None"
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "None"
        except Exception as e:
            print(f"Error: {e}")
            return "None"

def sendEmail(to, content):
    """Function to send email"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Replace with your email credentials
        server.login('your-email@gmail.com', 'your-password')
        server.sendmail('your-email@gmail.com', to, content)
        server.close()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Onz Dev Studios - Voice Assistant")
        self.root.geometry("800x700")
        self.is_listening = False
        self.recording_time = 0
        self.timer_running = False
        
        # Make the window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Configure root window
        self.root.configure(bg=COLORS['bg'])
        
        # Load logo
        self.load_logo()
        
        # Setup GUI
        self.setup_styles()
        self.create_gui()

    def load_logo(self):
        """Load and prepare logo image"""
        try:
            response = requests.get('https://oyintanda-zongwana.github.io/hosted-pics/pics%20folder/brand.png')
            self.logo_image = Image.open(BytesIO(response.content))
            self.logo_image = self.logo_image.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo_photo = None

    def setup_styles(self):
        """Configure all styles for the application"""
        self.style = ttk.Style()
        
        # Configure frame styles
        self.style.configure('Main.TFrame',
                           background=COLORS['bg'])
        
        self.style.configure('Card.TFrame',
                           background=COLORS['bg'],
                           relief='solid',
                           borderwidth=1)
        
        # Configure label styles
        self.style.configure('Title.TLabel',
                           background=COLORS['bg'],
                           foreground=COLORS['text'],
                           font=('Segoe UI', 24, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=COLORS['bg'],
                           foreground=COLORS['text'],
                           font=('Segoe UI', 14))
        
        # Configure button styles
        self.style.configure('Record.TButton',
                           background=COLORS['accent'],
                           foreground='#FFFFFF',
                           font=('Segoe UI', 12, 'bold'),
                           padding=15)
        
        self.style.configure('Toolbar.TButton',
                           background=COLORS['bg'],
                           foreground=COLORS['text'],
                           font=('Segoe UI', 12),
                           padding=10)
        
        # Configure entry style
        self.style.configure('Search.TEntry',
                           background=COLORS['bg'],
                           foreground=COLORS['text'],
                           fieldbackground=COLORS['bg'],
                           insertcolor=COLORS['text'],
                           font=('Segoe UI', 11))

    def create_gui(self):
        """Create the main GUI elements"""
        # Main container
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        
        # Configure grid weights for responsiveness
        self.main_container.grid_columnconfigure(0, weight=2)  # Left panel
        self.main_container.grid_columnconfigure(1, weight=3)  # Right panel
        self.main_container.grid_rowconfigure(1, weight=1)     # Content area
        
        # Create panels
        self.left_panel = ttk.Frame(self.main_container, style='Main.TFrame')
        self.left_panel.grid(row=1, column=0, sticky='nsew', padx=(0, 10))
        
        self.right_panel = ttk.Frame(self.main_container, style='Main.TFrame')
        self.right_panel.grid(row=1, column=1, sticky='nsew', padx=(10, 0))
        
        # Configure panel weights
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        
        # Create header
        self.create_header(self.main_container)
        
        # Create panel contents
        self.create_left_panel()
        self.create_right_panel()

    def create_header(self, container):
        """Create a modern header"""
        self.header = ttk.Frame(container, style='Main.TFrame')
        self.header.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Add logo
        if self.logo_photo:
            self.logo_label = ttk.Label(
                self.header,
                image=self.logo_photo,
                style='Logo.TLabel'
            )
            self.logo_label.grid(row=0, column=0, padx=(20, 10))
        
        # Add title next to logo
        title_frame = ttk.Frame(self.header, style='Main.TFrame')
        title_frame.grid(row=0, column=1, sticky='w')
        
        self.title = ttk.Label(
            title_frame,
            text="Onz Dev Studios",
            style='Title.TLabel'
        )
        self.title.grid(row=0, column=0, sticky='w')
        
        self.subtitle = ttk.Label(
            title_frame,
            text="Voice Assistant",
            style='Subtitle.TLabel'
        )
        self.subtitle.grid(row=1, column=0, sticky='w')

    def create_left_panel(self):
        """Create the left panel with voice assistant UI"""
        self.create_wave_display(self.left_panel)
        self.create_timer(self.left_panel)
        self.create_record_button(self.left_panel)
        self.create_toolbar(self.left_panel)

    def create_right_panel(self):
        """Create the right panel with transcript"""
        # Search bar with modern styling
        self.search_frame = ttk.Frame(self.right_panel, style='Card.TFrame', padding=10)
        self.search_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        self.search_frame.grid_columnconfigure(1, weight=1)
        
        search_icon = ttk.Label(
            self.search_frame,
            text="🔍",
            style='Subtitle.TLabel'
        )
        search_icon.grid(row=0, column=0, padx=(5, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        self.search_entry = ttk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            style='Search.TEntry'
        )
        self.search_entry.grid(row=0, column=1, sticky='ew')
        
        # Transcript area
        self.transcript_frame = ttk.Frame(self.right_panel, style='Card.TFrame', padding=20)
        self.transcript_frame.grid(row=1, column=0, sticky='nsew')
        self.transcript_frame.grid_columnconfigure(0, weight=1)
        self.transcript_frame.grid_rowconfigure(1, weight=1)
        
        self.transcript_area = tk.Text(
            self.transcript_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=COLORS['bg'],
            fg=COLORS['text'],
            relief='flat',
            padx=10,
            pady=10
        )
        self.transcript_area.grid(row=1, column=0, sticky='nsew')
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.transcript_frame,
            orient='vertical',
            command=self.transcript_area.yview
        )
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.transcript_area['yscrollcommand'] = self.scrollbar.set

    def create_wave_display(self, container):
        """Create a waveform display"""
        self.wave_label = ttk.Label(
            container,
            text="Voice Activity",
            style='Subtitle.TLabel'
        )
        self.wave_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.wave_frame = ttk.Frame(container, style='Card.TFrame', padding=20)
        self.wave_frame.grid(row=1, column=0, sticky='ew', pady=(0, 20))
        
        self.wave_canvas = tk.Canvas(
            self.wave_frame,
            height=150,
            width=300,  # Set a default width
            bg=COLORS['secondary_bg'],
            highlightthickness=1,
            highlightbackground=COLORS['border']
        )
        self.wave_canvas.grid(row=0, column=0, sticky='ew')
        
        # Initialize wave bars immediately
        self.setup_wave_bars()
        
        # Make the canvas responsive
        self.wave_frame.grid_columnconfigure(0, weight=1)
        self.wave_canvas.bind('<Configure>', self.on_canvas_resize)

    def setup_wave_bars(self):
        """Initialize the wave bars"""
        self.wave_canvas.delete("all")
        width = self.wave_canvas.winfo_width()
        height = self.wave_canvas.winfo_height()
        center_y = height // 2
        
        # Create bars
        bar_width = 4
        gap = 3
        num_bars = width // (bar_width + gap)
        
        self.wave_bars = []
        for i in range(num_bars):
            x = i * (bar_width + gap)
            bar = self.wave_canvas.create_rectangle(
                x, center_y - 2,
                x + bar_width, center_y + 2,
                fill=COLORS['accent'],
                width=0
            )
            self.wave_bars.append(bar)

    def on_canvas_resize(self, event):
        """Handle canvas resize"""
        self.setup_wave_bars()

    def animate_wave(self):
        """Animate the wave visualization"""
        if not self.is_listening or not hasattr(self, 'wave_bars'):
            return
        
        height = self.wave_canvas.winfo_height()
        center_y = height // 2
        
        # Animate each bar
        import random
        for bar in self.wave_bars:
            # Dynamic height variation
            bar_height = random.randint(15, 45)
            
            # Update bar height
            self.wave_canvas.coords(
                bar,
                self.wave_canvas.coords(bar)[0],  # x1
                center_y - bar_height,            # y1
                self.wave_canvas.coords(bar)[2],  # x2
                center_y + bar_height             # y2
            )
        
        # Schedule next animation frame
        self.animation_id = self.root.after(30, self.animate_wave)

    def create_timer(self, container):
        """Create the timer display"""
        self.timer_label = ttk.Label(
            container,
            text="00:00",
            style='Timer.TLabel'
        )
        self.timer_label.grid(row=2, column=0, pady=10)

    def create_record_button(self, container):
        """Create a modern record button"""
        self.record_btn = ttk.Button(
            container,
            text="▶️ Start",  # Changed to play icon
            style='Record.TButton',
            command=self.toggle_recording
        )
        self.record_btn.grid(row=3, column=0, pady=30)

    def create_toolbar(self, container):
        """Create the toolbar with action buttons"""
        self.toolbar = ttk.Frame(container, style='Toolbar.TFrame')
        self.toolbar.grid(row=4, column=0, sticky='ew', pady=(20, 0))
        
        toolbar_buttons = [
            ("📋", self.copy_text, "Copy transcript"),
            ("📁", self.open_file, "Open file"),
            ("📤", self.share, "Share"),
            ("⚙️", self.settings, "Settings")
        ]
        
        for i, (icon, command, tooltip) in enumerate(toolbar_buttons):
            btn = ttk.Button(
                self.toolbar,
                text=icon,
                style='Toolbar.TButton',
                command=command
            )
            btn.grid(row=0, column=i, padx=10)

    def update_timer(self):
        """Update the timer display"""
        if self.timer_running:
            self.recording_time += 1
            minutes = self.recording_time // 60
            seconds = self.recording_time % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def toggle_recording(self):
        """Toggle recording state and animation"""
        self.is_listening = not self.is_listening
        
        if self.is_listening:
            # Start recording
            self.record_btn.configure(text="⏸️ Pause")
            self.timer_running = True
            self.update_timer()
            
            # Ensure bars are set up
            if not hasattr(self, 'wave_bars') or not self.wave_bars:
                self.setup_wave_bars()
            
            # Start animation
            self.animate_wave()
            
            # Start voice recognition
            self.recognition_thread = threading.Thread(target=self.run_assistant)
            self.recognition_thread.daemon = True
            self.recognition_thread.start()
        else:
            # Stop recording
            self.record_btn.configure(text="▶️ Start")
            self.timer_running = False
            
            # Stop animation
            if hasattr(self, 'animation_id') and self.animation_id:
                self.root.after_cancel(self.animation_id)
                self.animation_id = None

    def start_assistant(self):
        """Start the voice assistant"""
        if not self.is_listening:
            self.is_listening = True
            self.assistant_thread = threading.Thread(target=self.run_assistant)
            self.assistant_thread.daemon = True
            self.assistant_thread.start()

    def stop_assistant(self):
        """Stop the voice assistant"""
        self.is_listening = False
        self.timer_running = False

    def run_assistant(self):
        """Main assistant loop"""
        while self.is_listening:
            query = takeCommand().lower()
            if query == "None":
                continue

            # Update transcript with user's query
            self.update_transcript(f"You: {query}")

            # Process commands
            if 'wikipedia' in query:
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                self.update_transcript(f"Assistant: According to Wikipedia\n{results}")
                speak("According to Wikipedia")
                speak(results)
            elif 'open google' in query:
                self.update_transcript("Assistant: Opening Google")
                webbrowser.open("google.com")
            elif 'open stackoverflow' in query:
                self.update_transcript("Assistant: Opening Stack Overflow")
                webbrowser.open("stackoverflow.com")
            elif 'play music' in query:
                music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
                songs = os.listdir(music_dir)
                self.update_transcript(f"Assistant: Playing: {songs[0]}")
                speak(f"Playing: {songs[0]}")
                os.startfile(os.path.join(music_dir, songs[0]))
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                self.update_transcript(f"Assistant: The time is {strTime}")
                speak(f"Sir and or Ma'am, The time is {strTime}")
            elif 'open code' in query:
                self.update_transcript("Assistant: Opening VS Code")
                codePath = "C:\\Users\\Ot\\AppData\\Local\\Programs\\Microsoft VS Code\\bin\\code"
                os.startfile(codePath)
            elif 'email to ot' in query:
                self.update_transcript("Assistant: Sending email")
                try:
                    speak("What should I say?")
                    content = takeCommand()
                    to = "OTyourEmail@gmail.com"
                    sendEmail(to, content)
                    self.update_transcript("Assistant: Email has been sent!")
                    speak("Email has been sent!")
                except Exception as e:
                    self.update_transcript("Assistant: Sorry my friend OT shame. I am not able to send this email")
                    speak("Sorry my friend OT shame. I am not able to send this email")

    # Toolbar button functions
    def copy_text(self):
        """Copy transcript text to clipboard"""
        text = self.transcript_area.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.update_transcript("Assistant: Transcript copied to clipboard")
        speak("Transcript copied to clipboard")

    def open_file(self):
        """Open a saved transcript file"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Open Transcript File"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.transcript_area.delete(1.0, tk.END)
                    self.transcript_area.insert(1.0, content)
                self.update_transcript(f"Assistant: Opened file: {file_path}")
                speak("File opened successfully")
            except Exception as e:
                self.update_transcript(f"Assistant: Error opening file: {str(e)}")
                speak("Error opening file")

    def share(self):
        """Save transcript to file"""
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Transcript As"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    text = self.transcript_area.get(1.0, tk.END)
                    file.write(text)
                self.update_transcript(f"Assistant: Transcript saved to: {file_path}")
                speak("Transcript saved successfully")
            except Exception as e:
                self.update_transcript(f"Assistant: Error saving transcript: {str(e)}")
                speak("Error saving transcript")

    def settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=COLORS['bg'])
        
        # Voice settings
        voice_frame = ttk.LabelFrame(settings_window, text="Voice Settings", padding=10)
        voice_frame.pack(fill='x', padx=10, pady=5)
        
        # Voice selection
        ttk.Label(voice_frame, text="Select Voice:").pack(anchor='w')
        voice_var = tk.StringVar(value="Voice 1")
        voice_combo = ttk.Combobox(voice_frame, textvariable=voice_var)
        voice_combo['values'] = [f"Voice {i+1}" for i in range(len(voices))]
        voice_combo.pack(fill='x', pady=5)
        
        # Speed settings
        speed_frame = ttk.LabelFrame(settings_window, text="Speech Speed", padding=10)
        speed_frame.pack(fill='x', padx=10, pady=5)
        
        speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(
            speed_frame,
            from_=0.5,
            to=2.0,
            variable=speed_var,
            orient='horizontal'
        )
        speed_scale.pack(fill='x')
        
        # Save settings button
        def save_settings():
            try:
                engine.setProperty("voice", voices[voice_combo.current()].id)
                engine.setProperty("rate", int(engine.getProperty('rate') * speed_var.get()))
                self.update_transcript("Assistant: Settings saved")
                speak("Settings saved")
                settings_window.destroy()
            except Exception as e:
                self.update_transcript(f"Assistant: Error saving settings: {str(e)}")
                speak("Error saving settings")
        
        ttk.Button(
            settings_window,
            text="Save Settings",
            command=save_settings
        ).pack(pady=20)

    def clear_transcript(self):
        """Clear the transcript area"""
        self.transcript_area.delete(1.0, tk.END)
        self.search_var.set("")  # Clear search
        self.current_search_index.set("0/0")

    def on_search_change(self, *args):
        """Handle search text changes"""
        search_text = self.search_var.get()
        if search_text:
            self.highlight_search(search_text)
        else:
            self.clear_highlights()

    def highlight_search(self, search_text):
        """Highlight all instances of search text"""
        # Clear previous highlights
        self.clear_highlights()
        
        # Configure highlight tag
        self.transcript_area.tag_configure('highlight', background='yellow', foreground='black')
        
        # Find and highlight matches
        start_pos = '1.0'
        self.search_matches = []
        
        while True:
            start_pos = self.transcript_area.search(
                search_text, start_pos, tk.END, nocase=True
            )
            if not start_pos:
                break
            
            end_pos = f"{start_pos}+{len(search_text)}c"
            self.transcript_area.tag_add('highlight', start_pos, end_pos)
            self.search_matches.append(start_pos)
            start_pos = end_pos
        
        # Update match counter
        total_matches = len(self.search_matches)
        self.current_match = 0 if total_matches > 0 else -1
        self.current_search_index.set(f"{self.current_match + 1}/{total_matches}" if total_matches > 0 else "0/0")

    def clear_highlights(self):
        """Clear all search highlights"""
        self.transcript_area.tag_remove('highlight', '1.0', tk.END)
        self.search_matches = []
        self.current_match = -1
        self.current_search_index.set("0/0")

    def search_text(self, direction):
        """Navigate through search results"""
        if not self.search_matches:
            return
        
        if direction == 'forward':
            self.current_match = (self.current_match + 1) % len(self.search_matches)
        else:
            self.current_match = (self.current_match - 1) % len(self.search_matches)
        
        # Highlight current match differently
        self.transcript_area.tag_remove('current_match', '1.0', tk.END)
        self.transcript_area.tag_configure('current_match', background='orange', foreground='black')
        
        # Get position of current match
        match_pos = self.search_matches[self.current_match]
        end_pos = f"{match_pos}+{len(self.search_var.get())}c"
        
        # Apply current match highlight
        self.transcript_area.tag_add('current_match', match_pos, end_pos)
        
        # Ensure current match is visible
        self.transcript_area.see(match_pos)
        
        # Update counter
        self.current_search_index.set(f"{self.current_match + 1}/{len(self.search_matches)}")

    def update_transcript(self, text):
        """Add text to transcript with modern styling"""
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.transcript_area.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
        self.transcript_area.insert(tk.END, f"{text}\n", "message")
        self.transcript_area.see(tk.END)
        
        # Configure tags for styling
        self.transcript_area.tag_configure(
            "timestamp",
            foreground=COLORS['secondary_text'],
            font=('Segoe UI', 9)
        )
        self.transcript_area.tag_configure(
            "message",
            foreground=COLORS['text'],
            font=('Segoe UI', 11)
        )

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = VoiceAssistantGUI(root)
        wishMe()
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")