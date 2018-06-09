import pymssql
import pysvn
import os
import glob
print(os.environ['HOME'])
emCoreHome= os.environ['EM_CORE_HOME']
#jfrom os.path import expanduser
#home = expanduser("~")

#source home/.em.bash

host = 'windows'
username = 'sa'
password = 'admin'
database = 'ootb_15_1_fp2'

conn = pymssql.connect(host, username, password, database)
cursor = conn.cursor()

SQLCommand1 ='''SELECT * FROM CCADMIN_VERSION WHERE RELEASE_NAME = %s
            ''' 
SQLCommand ='''UPDATE CCADMIN_VERSION SET UPGRADE_VERSION= 4821 WHERE RELEASE_NAME = %s
            '''
releaseName= 'Project_R1_0_0'

#cursor.execute(SQLCommand,query_params) 
#cursor.execute(SQLCommand,(releaseName)) 
#svn up
cursor.execute(SQLCommand1,(releaseName)) 
results = cursor.fetchone() 
while results:
     print ("Your customer " +  results[0] + " " + str(results[1]))
     results = cursor.fetchone() 

conn.commit()
conn.close()
client = pysvn.Client()

def login(*args):
        return True, 'dgarcia', 'Drec0mmo3', False

client.callback_get_login = login

rev= client.update(emCoreHome)
print "Revision: ", str(rev[0]).split(" ")[-1][:-1]



os.chdir(emCoreHome+"/modules")
for file in glob.glob("update.sequence"):
        print(file)

