# so the point of this script was to test to see if I can append the DFARS files
#   to the main part file, but apparently there already is a main file
# also, this was eventually going to parse out the html for other text, but
#   not even Jon Skeet can parse html per: https://blog.codinghorror.com/parsing-html-the-cthulhu-way/
# this will only be saved to remind me of the troubles with parsing html...

import os

# main path to current folder
dir_path = os.path.dirname(os.path.abspath(__file__))
dfars_dir = "dfars_dev"
dir_path = dir_path + "\\" + dfars_dir + "\\"

# start the main loop with identifying the DFARS parts, then read file
for i in range(201, 254):
  pnum = str(i)  
  print("################################################################################")
  print("DFARS Part: " + pnum)

  # create file, then read it from directory
  mname = "PART_" + pnum + ".html"
  mpath = dir_path + mname
  mfile = open(mpath, "r")
  mcont = mfile.read()
  mfile.close()

  # first append main file
  apath = "_append_" + mname
  apath = dir_path + apath
  afile = open(apath, "a")
  afile.write(mcont)
  afile.write("<br>")
  
  # now start appending everything else
  for j in os.listdir(dir_path):
    if j[0:3] == pnum:
      jpath = dir_path + j
      jfile = open(jpath, "r", encoding="utf8")
      jcont = jfile.read()
      jfile.close()
      afile.write(jcont)
      afile.write("<br>")

  # operation finished
  afile.close()
  print("Finished with " + pnum)



















