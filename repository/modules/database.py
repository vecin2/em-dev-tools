import pymssql
import sys

def update_rev_number():
    host = 'windows'
    username = 'sa'
    password = 'admin'
    database = 'ootb_15_1_fp2'
    
    conn = pymssql.connect(host, username, password, database)
    cursor = conn.cursor()
    
    SQLCommand1 ='''SELECT * FROM CCADMIN_VERSION WHERE RELEASE_NAME = %s
                ''' 
    SQLCommand ='''UPDATE CCADMIN_VERSION SET UPGRADE_VERSION=%s  WHERE RELEASE_NAME = %s
                '''
    releaseName= 'Project_R1_0_0'
    updateToValue=sys.argv[1]
    
    cursor.execute(SQLCommand1,(releaseName)) 
    results = cursor.fetchone() 
    while results:
        print ("Updating UPGRADE_VERSION in CCADMIN_VERSION table for project " +  results[2] + " from value " + str(results[1]) +
                " to value "+ str(updateToValue))
        results = cursor.fetchone() 
    
    cursor.execute(SQLCommand,(updateToValue,releaseName)) 
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_rev_number()
