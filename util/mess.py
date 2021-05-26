file=open("C:\\Users\m\\Desktop\\game of life patteren\\glider.txt","r")
file1=open("C:\\Users\m\\Desktop\\game of life patteren\\glider1.txt","w+")
for line in file:
    line = list(map(int,line.split(",")))
    file1.write(str(line[0])+","+str(int(line[1])-2)+","+str(int(line[2]))+"\n")

file1.close()