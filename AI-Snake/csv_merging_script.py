import glob
import os

#os.chdir("/C:/Users/barjan/Desktop/comp_bsc\3rd\Deep_l\Py_Snake")
for files in glob.glob("*.csv"):
        print(files)

f_out = open("Final_data_set.csv", "a")
for file in glob.glob("*.csv"):
    f = open(file)
    f.__next__()
    # skip the header
    for line in f:
        f_out.write(line)
    f.close()
f_out.close()
