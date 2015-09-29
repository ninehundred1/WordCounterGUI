__author__ = 'Meyer'
"""
Simple Word counter that counts how often each word is appearing in a txt 
document and displays counts in GUI and also saves them as text file.
Intended to find the most common words used in a text to focus the learning
of vocabulary on the most common words in a language.
"""
from collections import defaultdict
import os
import Tkinter
from tkFileDialog import askopenfilename

class WordCounterGUI():
	
     	def __init__(self, parent_gui):
		self.root = parent_gui
		self.create_GUI()
		self.total_words = 0
		self.words = defaultdict(int)
		self.file_list = []
		
	def create_GUI(self):
		self.root.wm_title("WordCount")
		instruction_field = Tkinter.Label(self.root, text="Choose .txt file to upload for word count. Counts are saved in same directory")
		instruction_field.pack(ipadx=50)
		instruction_field.pack(ipadx=50)
		self.choose_file_button = Tkinter.Button(self.root, text="choose txt files",bg="green", fg="black", command=self.on_load_data_button)
		self.choose_file_button.pack()
		self.file_text = Tkinter.Label(self.root,  font=("Helvetica", 9), text=" - ")
        	self.file_text.pack()
        	self.status_text = Tkinter.Label(self.root,  font=("Helvetica", 11), text=" Please load .txt file ")
        	self.status_text.pack()
        	self.count_output_field = Tkinter.Text(self.root, width = 80, height = 40, takefocus=0)
        	self.scrollbar = Tkinter.Scrollbar(self.root)
        	self.scrollbar.pack(side = Tkinter.RIGHT, fill=Tkinter.Y )
        	self.scrollbar.config(command=self.count_output_field.yview)
        	self.count_output_field.config(yscrollcommand=self.scrollbar.set)
        	self.count_output_field.pack()
        	
	def on_load_data_button(self):
		file = askopenfilename(filetypes=[("txt files","*.txt")], parent=root,title='Choose .txt file to count')
		if file:
			self.status_text.configure(text="Loaded Text")
			self.file_name = os.path.splitext(file)[0]
			name_ext=os.path.basename(file)
			name_only = os.path.splitext(name_ext)[0]
			self.file_text.configure(text=name_only)
			if name_only in self.file_list:
				self.status_text.configure(text="File already included")
				return
			self.file_list.append(name_only)
			words_last_file = 0
			with open(file,'r') as file_stream:
				for line in file_stream:
					words_in_line = line.split()
					self.total_words += len(words_in_line)
					for word in words_in_line:
						self.words[word] += 1
						words_last_file += 1
			self.status_text.configure(text="Last file total words: "+str(words_last_file))
			self.show_all()
			self.choose_file_button.config(text="add another file") 
		else:
			self.status_text.configure(text="File path invalid")

	def show_all(self):
		sorted_dict = sorted(self.words.iteritems(),key=lambda (k,v): v,reverse=True)
		file_export = open(self.file_name+'_WORDS.txt', 'w')
		file_export.write('Total Words Counted: ' +str(self.total_words) + '\n')
		file_export.write('Unique words founds: '+str(len(self.words))+'\n')
		file_export.write('Unique words %: '+str("{0:.2f}".format(len(self.words)/float(self.total_words)))+'\n')
		file_export.write('\nFILES INCLUDED:\n')
		#self.status_text.configure(text="Total Words counted: "+str(self.total_words))
		self.count_output_field.delete(1.0,Tkinter.END)
		self.count_output_field.insert(Tkinter.INSERT, 'Total Words counted: '+str(self.total_words)+'\n')
		self.count_output_field.insert(Tkinter.INSERT, 'Unique words founds: '+str(len(self.words))+'\n')
		self.count_output_field.insert(Tkinter.INSERT, 'Unique words %: '+str("{0:.2f}".format(len(self.words)/float(self.total_words)))+'\n')
		self.count_output_field.insert(Tkinter.INSERT, '\nFILES INCLUDED:\n')
		for names in self.file_list:
			file_export.write(names+'\n')
			self.count_output_field.insert(Tkinter.INSERT, names+'\n')
		list_display = []
		file_export.write('\n')
		for i, tuples in enumerate(sorted_dict):
			line = '\t\t'.join(str(x) for x in tuples)
			file_export.write(str(i+1)+'\t'+line + '\n')
			list_display.append(str(i+1)+'\t'+line)
		file_export.close()
		list_display_format = "\n".join(list_display)
		self.count_output_field.insert(Tkinter.INSERT, '\n'+list_display_format)

root = Tkinter.Tk()
my_gui = WordCounterGUI(root)
root.mainloop()