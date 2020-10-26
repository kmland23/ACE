import random
import xml.dom.minidom
import lxml.etree as etree
from bs4 import BeautifulSoup

filename="Rascal.xml"

#get random values 
minFT2=random.choice([8, 9, 10, 11, 12,13, 14])
maxFT2=random.choice([8, 9, 10, 11, 12,13, 14])
distributionFT2='uniform'
minFT=random.choice([8, 9, 10, 11, 12,13, 14])
maxFT=random.choice([8, 9, 10, 11, 12,13, 14])
distributionFT='normal'
stdFT2=random.choice([1, 2, 3, 4, 5, 6, 7])
stdFT=random.choice([1, 2, 3, 4, 5, 6, 7])

#get smaller value for minimum than maximum
while int(minFT)>int(maxFT):
    minFT=random.choice([8, 9, 10, 11, 12,13, 14])

while int(minFT2)>int(maxFT2):
    minFT2=random.choice([8, 9, 10, 11, 12, 13, 14])
    
#open original xml file
my_file = open(filename, "r+")
lines_of_file = my_file.readlines()

variation=random.choice([1, 2, 3, 4])

my_file = open(filename, "r+")
lines_of_file = my_file.readlines()

#chooses randomly between uniform or normal distributions
if variation==1:
    
    string1="<wingarea unit= 'FT2' min={} max={} distribution='uniform' > 10.57 </wingarea>".format(minFT2,       
                    maxFT2)
    string2="<wingspan unit= 'FT' min={} max={} distribution='normal'> std={}> 9.17 </wingspan>".format(minFT, 
                    maxFT, stdFT)
 
elif variation ==2:
        
    string1="<wingarea unit= 'FT2' min= {} max= {} distribution= 'normal' > std={}>10.57 </wingarea>".format(minFT2, maxFT2, stdFT2)
    string2="<wingspan unit= 'FT' min={} max={} distribution= 'normal'> std={}> 9.17 </wingspan>".format(minFT, maxFT, stdFT)

elif variation ==3:
        
    string1="<wingarea unit= 'FT2' min= {} max= {} distribution= 'uniform' > 10.57 </wingarea>".format(minFT2, 
                                                                                maxFT2)
    string2="<wingspan unit= 'FT' min={} max={} distribution='uniform'> 9.17 </wingspan>".format(minFT, maxFT)

else:
            
    string1="<wingarea unit= 'FT2' min= {} max= {} distribution= 'normal' > std={}>10.57 </wingarea>".format(minFT2, maxFT2, distributionFT2, stdFT2)
    string2="<wingspan unit= 'FT' min={} max={} distribution='uniform'> 9.17 </wingspan>".format(minFT, maxFT, distributionFT)

lines_of_file.insert(15, string1)
lines_of_file.insert(16, string2)

'''
#this makes it pretty, but changes the order and puts "" around the inputs
bs = BeautifulSoup(str(lines_of_file))
prettyXML= (bs.prettify())
#prettyXML=prettyXML.get_text()
print (str(prettyXML))
'''

#creates file in the correct order without '' but is not pretty
with open("Rascal_11.xml", "w+") as f: 
    f.write(str(lines_of_file)) 

my_file.close()

