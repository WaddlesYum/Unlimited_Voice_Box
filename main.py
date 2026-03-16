import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import edge_tts
import threading
import pygame # Used to play the sound once generated

# Initialize pygame mixer for audio playback
pygame.mixer.init()

async def generate_and_play(text, voice_name):
    output_file = "speech_output.mp3"
    try:
        # This part talks to Microsoft's servers to get the high-quality voice
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_file)
        
        # Play the resulting file
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

def on_button_click():
    text = text_entry.get("1.0", tk.END).strip()
    voice = voice_box.get()
    
    if not text:
        messagebox.showwarning("Warning", "Type something first!")
        return

    # Run the AI voice generation in a background thread so the app doesn't freeze
    def run_async():
        asyncio.run(generate_and_play(text, voice))
    
    threading.Thread(target=run_async, daemon=True).start()

# --- GUI SETUP ---
root = tk.Tk()
root.title("Unlimited AI Voice Box")
root.geometry("400x300")

tk.Label(root, text="Type your message:", font=("Arial", 10)).pack(pady=5)
text_entry = tk.Text(root, height=5, width=40)
text_entry.pack(pady=5)

tk.Label(root, text="Select Voice:", font=("Arial", 10)).pack(pady=5)
# These are the "Bella" style high-quality voices
voices = ["en-US-AvaNeural", "en-US-EmmaNeural", "en-US-AndrewNeural", "en-GB-SoniaNeural"]
voice_box = ttk.Combobox(root, values=voices, state="readonly")
voice_box.current(0)
voice_box.pack(pady=5)

speak_button = tk.Button(root, text="Speak Message", command=on_button_click, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
speak_button.pack(pady=20)

root.mainloop()