import os
import pygame 
import ctypes
import os

def is_hidden(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    return name.startswith('.') or has_hidden_attribute(filepath)

def has_hidden_attribute(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result

def count_files_in_folder(folder):
	# folder path
	dir_path = folder
	count = 0
	# Iterate directory
	for path in os.listdir(dir_path):
		# check if current path is a file
		if os.path.isfile(os.path.join(dir_path, path)) and not is_hidden(path):
			count += 1
	print('File count:', count)
	return count

class AnimatedObject():
	img_path = "../graphics/spirit/"
	
	def change_status(self,status):
		self.status=status
		self.frame_index=0

	def get_picture(self):
		self.frame_index+=1
		if(self.frame_index==self.pictures[self.status]["n_frames"]):
			self.frame_index=0
		return self.pictures[self.status]["images"][self.frame_index]
	
	def load_pictures(img_path,statuses):
		pictures={}
		for j in statuses:
			folder_path = img_path+j+"/"
			print(folder_path)
			n_files = count_files_in_folder(folder_path)
			pictures_array=[]
			pictures[j]={}
			for i in range(0,n_files):
				pictures_array.append(pygame.image.load(folder_path+"{}.png".format(i)))
			pictures[j]["images"]=pictures_array
			pictures[j]["n_frames"]=n_files
		return pictures