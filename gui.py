from tkinter import *
from tkinter.ttk import Combobox
from random import randint
import webbrowser
from PIL import Image, ImageTk
from urllib.request import urlopen
import tkinter.filedialog
from tkinter import messagebox

# Initializes Tkinter
root = Tk()

# Sets the size of the window
root.geometry("600x350")

# Sets the minimum window size
root.minsize(400, 350)

# Titles the window
root.title('Sky Explore v1.2')

root.iconphoto(False, PhotoImage(file = "LogoFull.png"))

def random_coords():
	random_RA = f'{randint(0, 23)} {randint(0, 59)} {randint(0, 5999) / 100}'
	random_DEC = f'{randint(-89, 89)} {randint(0, 59)} {randint(0, 599) / 10}'
	return random_RA, random_DEC

def gen_url(RA, DEC, arc_min_width, arc_min_height, database, file_format):
	# Saves the url in a variable and opens it in the browser
	return f"https://archive.stsci.edu/cgi-bin/dss_search?v={database}&r={RA.replace(' ', '+')}&d={DEC.replace(' ', '+')}%22&e=J2000&h={arc_min_height}&w={arc_min_width}&f={file_format}&c=none&fov=NONE&v3="

# Main window class

class mainWindow:
	def combo_change(self, x):
		curr_format = self.file_format_combo.get()
		if curr_format == 'FITS (URL Only)':
			self.download_rand_button["state"] = "disabled"
			self.download_spec_button["state"] = "disabled"
			self.open_url_rand_button.configure(text="Open URL (Direct Download)")
			self.open_url_spec_button.configure(text="Open URL (Direct Download)")

		elif curr_format == 'GIF':
			self.download_rand_button["state"] = "normal"
			self.download_spec_button["state"] = "normal"
			self.open_url_rand_button.configure(text="Open URL")
			self.open_url_spec_button.configure(text="Open URL")

	def open_rand_url(self):
		if self.check_validity() == False:
			return None
		rand_coords = random_coords()
		webbrowser.open(gen_url(rand_coords[0], rand_coords[1], float(self.image_arc_width_entry.get()), float(self.image_arc_height_entry.get()), self.database_dict[self.database_combo.get()], self.file_formats_dict[self.file_format_combo.get()]), new=2)

	def open_spec_url(self):
		if self.check_validity(extra=True) == False:
			return None
		webbrowser.open(gen_url(self.ra_entry.get(), self.dec_entry.get(), float(self.image_arc_width_entry.get()),
								float(self.image_arc_height_entry.get()), self.database_dict[self.database_combo.get()],
								self.file_formats_dict[self.file_format_combo.get()]), new=2)

	def download_rand(self):
		if self.check_validity() == False:
			return None
		rand_coords = random_coords()
		url = gen_url(rand_coords[0], rand_coords[1], float(self.image_arc_width_entry.get()), float(self.image_arc_height_entry.get()), self.database_dict[self.database_combo.get()], self.file_formats_dict[self.file_format_combo.get()])
		self.download(url)

	def download_spec(self):
		if self.check_validity(extra=True) == False:
			return None
		url = gen_url(self.ra_entry.get(), self.dec_entry.get(), float(self.image_arc_width_entry.get()), float(self.image_arc_height_entry.get()), self.database_dict[self.database_combo.get()], self.file_formats_dict[self.file_format_combo.get()])
		self.download(url)


	def download(self, url):
		path = tkinter.filedialog.asksaveasfilename(filetypes=(("Gif", "*.gif"), ("All files", "*.*")))
		if len(path) == 0:
			return
		img = Image.open(urlopen(url))
		img.save(path)

	def check_validity(self, extra=False):
		if self.image_arc_width_entry.get() == '' or self.image_arc_height_entry.get() == '':
			messagebox.showerror("Sky Explore v1.2 | Error", "Missing one or more of the image dimensions.")
			return False

		if float(self.image_arc_width_entry.get()) > 120:
			messagebox.showerror("Sky Explore v1.2 | Error", "Dimensions must be a maximum of 120 arc minutes.")
			return False

		if float(self.image_arc_width_entry.get()) <= 0:
			messagebox.showerror("Sky Explore v1.2 | Error", "Dimensions must be a greater than 0.")
			return False

		if extra:
			if len(self.ra_entry.get().split(' ')) != 3 or len(self.dec_entry.get().split(' ')) != 3:
				messagebox.showerror("Sky Explore v1.2 | Error", "Right Accention and/or Declication is invalid.")
				return False

		return True

	def __init__(self):

		# Class for tips when hovering over certain widgets
		# self.tip = Balloon(root)
		# self.tip.bind_widget(widget, balloonmsg="My MSG")

		# --------------------------

		root.columnconfigure(0, weight=1) # Make window resize properly
		root.columnconfigure(1, weight=1)  # Make window resize properly
		root.rowconfigure(0, weight=1)  # Make window resize properly
		root.rowconfigure(1, weight=1)  # Make window resize properly

		# --------------------------

		self.settings_frame = LabelFrame(root, text='Settings')  # The frame for random generation
		self.settings_frame.grid(row=0, column=0, padx=10, pady=5, ipadx=10, ipady=10, columnspan=2, sticky=E+W+N+S)  # Places the frame in grid

		for col in range(3): # Configures all the columns
			self.settings_frame.columnconfigure(col, weight=1)

		for row in range(4):  # Configures all the rows
			self.settings_frame.rowconfigure(row, weight=1)

		self.image_arc_width_label = Label(self.settings_frame, text="Image width (Arc minutes): ")
		self.image_arc_width_label.grid(column=0, row=0, padx=10, pady=5, ipadx=10, ipady=5, sticky=E+W)

		self.image_arc_width_entry = Entry(self.settings_frame)
		self.image_arc_width_entry.grid(column=1, row=0, padx=10, pady=5, ipadx=10, ipady=5, sticky=E+W)

		self.image_arc_height_label = Label(self.settings_frame, text="Image height (Arc minutes): ")
		self.image_arc_height_label.grid(column=0, row=1, padx=10, pady=5, ipadx=10, ipady=5, sticky=E+W)

		self.image_arc_height_entry = Entry(self.settings_frame)
		self.image_arc_height_entry.grid(column=1, row=1, padx=10, pady=5, ipadx=10, ipady=5, sticky=E+W)

		self.file_format_label = Label(self.settings_frame, text="File format: ")  # Creates the combobox
		self.file_format_label.grid(column=0, row=2, padx=10, pady=5, ipadx=10, ipady=5)

		self.file_formats_dict = {
			'GIF': 'GIF',
			'FITS (URL Only)': 'FITS'
		}
		self.file_format_combo = Combobox(self.settings_frame) # Creates the combobox
		self.file_format_combo['values'] = list(self.file_formats_dict.keys()) # Sets the combobox's values
		self.file_format_combo.grid(column=1, row=2, padx=10, pady=5, ipadx=10, ipady=5, sticky=E+W) # Places the combobox
		self.file_format_combo.bind('<<ComboboxSelected>>', lambda x:self.combo_change(None))
		self.file_format_combo.current(0)

		self.database_label = Label(self.settings_frame, text="Database: ")  # Creates the combobox
		self.database_label.grid(column=0, row=3, padx=10, pady=5, ipadx=10, ipady=5, sticky=E+W)

		self.database_dict = {
			"Automatic": 'all',
			"POSS2/UKSTU Red Band": 'poss2ukstu_red',
			"POSS2/UKSTU Infrared": 'poss2ukstu_ir',
			"POSS2/UKSTU Blue Band": 'poss2ukstu_blue',
			"POSS1 Blue Band": 'poss1_blue',
			"POSS1 Red Band": 'poss1_red',
			"Quick-V": "quickv",
			"Phase II GSC2": 'phase2_gsc2',
			"Phase II GSC1": 'phase2_gsc1'
		}
		self.database_combo = Combobox(self.settings_frame)  # Creates the combobox
		self.database_combo['values'] = list(self.database_dict.keys())  # Sets the combobox's values
		self.database_combo.grid(column=1, row=3, padx=10, pady=5, ipadx=10, ipady=5,
									sticky=E+W)  # Places the combobox
		self.database_combo.current(0)

		# --------------------------

		self.generate_random_frame = LabelFrame(root, text='Generate Random')  # The frame for random generation
		self.generate_random_frame.grid(row=1, column=0, padx=10, pady=5, ipadx=50, ipady=10, sticky=E+W+N+S) # Places the frame in grid

		for col in range(1):
			self.generate_random_frame.columnconfigure(col, weight=1)  # Make frame resize properly
		for row in range(2):
			self.generate_random_frame.rowconfigure(row, weight=1)  # Make frame resize properly

		self.open_url_rand_button = Button(self.generate_random_frame, text='Open URL', command=self.open_rand_url)
		self.open_url_rand_button.grid(row=0, column=0, padx=10, pady=5, ipadx=10, ipady=10, sticky=E+W)  # Places the button in the labeled frame

		self.download_rand_button = Button(self.generate_random_frame, text='Download (SLOW)', command=self.download_rand)
		self.download_rand_button.grid(row=1, column=0, padx=10, pady=5, ipadx=10, ipady=10, sticky=E+W)  # Places the button in the labeled frame

		# --------------------------

		self.generate_spec_frame = LabelFrame(root, text='Generate Specific')  # The frame for random generation
		self.generate_spec_frame.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=10, sticky=E+W+N+S)  # Places the frame in grid

		for col in range(2):
			self.generate_spec_frame.columnconfigure(col, weight=1)  # Make frame resize properly
		for row in range(3):
			self.generate_spec_frame.rowconfigure(row, weight=1)  # Make frame resize properly

		self.ra_label = Label(self.generate_spec_frame, text="Right Ascension (E.X. 18 53 35.08): ")
		self.ra_label.grid(row=0, column=0, padx=10, pady=5, ipadx=10, ipady=10, sticky=E+W)

		self.ra_entry = Entry(self.generate_spec_frame)
		self.ra_entry.grid(row=0, column=1, padx=10, pady=5, ipadx=10, ipady=10, sticky=E+W)

		self.dec_label = Label(self.generate_spec_frame, text="Declination (E.X. +33 01 45.0): ")
		self.dec_label.grid(row=1, column=0, padx=10, pady=5, ipadx=10, ipady=10, sticky=E+W)

		self.dec_entry = Entry(self.generate_spec_frame)
		self.dec_entry.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=10, sticky=E+W)

		self.open_url_spec_button = Button(self.generate_spec_frame, text='Open URL', command=self.open_spec_url)
		self.open_url_spec_button.grid(row=2, column=0, padx=10, pady=5, ipadx=10, ipady=10, columnspan=2, sticky=E+W)  # Places the button in the labeled frame

		self.download_spec_button = Button(self.generate_spec_frame, text='Download (SLOW)', command=self.download_spec)
		self.download_spec_button.grid(row=3, column=0, padx=10, pady=5, ipadx=10, ipady=10, columnspan=2, sticky=E+W)  # Places the button in the labeled frame

e = mainWindow()
root.mainloop()