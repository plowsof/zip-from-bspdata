
#create zips using dendeds bspdata output
import os
import glob
import zipfile

bspDataDir = "E:\\WIS\\dump_tex_bsp-main (1)\\dump_tex_bsp-main\\bspdata\\bspdata" 
resource_dir = "E:\\WIS\\user\\user"
maps_dir = "E:\\WIS\\user\\user\\maps"
zip_dir = "E:\\WIS\\dump_tex_bsp-main\\GithubZips"
sounds_dir = os.path.join(resource_dir,"sounds")
textures_dir = os.path.join(resource_dir,"textures")


for subdir, dirs, files in os.walk(maps_dir):
	for filename in files:
		subdir = subdir.split("\\")[-1]
		#i dont have to do the dm/ folder 
		if subdir != "dm":
			#only bsp
			if filename[-3:] == "bsp":
				#print(f"subdir:{subdir}\nfname:{filename}\n*************")
				collect_required = os.path.join(bspDataDir, subdir)
				sounds = os.path.join(collect_required,"sound")
				textures = os.path.join(collect_required,"textures")
				selfSound = os.path.join(sounds,filename[:-3]+"txt")
				selfTexture =os.path.join(textures,filename[:-3]+"txt")
				req_files=[]
				print(filename)
				if os.path.isfile(selfSound):
					with open(selfSound, "r") as f:
						lines = f.readlines()
						for line in lines:
							#print(line[:-1])
							line = os.path.join("sound",line)
							req_files.append(line[:-1])
				if os.path.isfile(selfTexture):
					with open(selfTexture,"r") as f:
						lines = f.readlines()
						for line in lines:
							#print(line[:-1])
							line = os.path.join("textures",line)
							req_files.append(line[:-1])

				#time to build the zip
				zfile = os.path.join(zip_dir,subdir,filename[:-3]+"zip")
				if not os.path.exists(os.path.dirname(zfile)):
					try:
						print("create the dir")
						os.makedirs(os.path.dirname(zfile))
						pass
					except Exception as e:
						print(e)
			    		
				missing_stuff = os.path.join(zip_dir,subdir,"missing_stuff.txt")
				with zipfile.ZipFile(zfile,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as zipObj:
					#write the bsp first
					mapfile = os.path.join(maps_dir,subdir,filename)
					zip_mapdir = os.path.join("maps",filename)
					zipObj.write(mapfile, zip_mapdir)
					for x in req_files:
						pathToFile = os.path.join(resource_dir,x)
						if os.path.isfile(pathToFile):
							zipObj.write(pathToFile, x)
						else:
							print(f"{pathToFile} : not exist")
							if os.path.isfile(missing_stuff):
								with open(missing_stuff,"a") as f:
									f.write(f"{filename} ~ {x} : not exist\n")
							else:
								with open(missing_stuff,"w") as f:
									f.write(f"{filename} ~ {x} : not exist\n")