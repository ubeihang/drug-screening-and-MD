import os
import linecache
from shutil import copyfile

f = open("F:\dataset\experimentaldata\pdbqt\\hb.txt", 'w')  # Create an empty text first

path = "F:\dataset\experimentaldata\pdbqt\pdbqt"  # Specify the directory to read the file from

files = os.listdir(path)  # Use 'listdir' to read all file names

files.sort()  # filename sorting

for file_ in files:  # Loop through each filename
   
    if os.path.isdir(path + '/'+ file_):  # Determine if it is a folder
        f_name = file_
      
        the_line = linecache.getline('F:\dataset\experimentaldata\pdbqt\pdbqt\\' + file_ + '\\log.txt', 25)
      
        
        if the_line.strip()== '':
            f.write(f_name + '       1         -0.1      0.000      0.000' + '\n' )   # append text
            copyfile(path + '/'+ file_ + '.pdbqt' , 'F:\dataset\experimentaldata\pdbqt-3\error'+ '/'+ file_ + '.pdbqt')

        else:
            f.write(f_name + '    ' + the_line )  # append text
        
        linecache.clearcache()

print("Program completed successfully!")
