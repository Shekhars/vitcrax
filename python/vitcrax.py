import mechanize   #browser in python
import cookielib   #mantain session
from mechanize import Browser   
from BeautifulSoup import BeautifulSoup # BeautifulSoup is for text processing html pages
import MySQLdb  # Mysql wrapper Note: u need mysql installed
db=MySQLdb.connect(user="root",passwd="",db="<dbname>",unix_socket="/opt/lampp/var/mysql/mysql.sock") # unix_socket is to use xampp socket
if db:
    print 'succes'
cursor = db.cursor() 
br=mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
n=0
while(n<=550):
    m=str(n).zfill(4) # filling zeros for roll no like 001,002 etc. 
    n=n+1
    print '10BCE'+m   # This is where roll no goes, for 09BCE just replace by 09BCE.
    u='10BCE'+m
    r=br.open('https://academics.vit.ac.in/parent/parent_login.asp')
    html=r.read()
    soup=BeautifulSoup(html) 
    e=soup('font', face="verdana",size="3")
    c=e[0].contents[0]  # this is the captcha in unicode
    a=c.encode('ascii','ignore')
    b=a.split(' ')
    captcha=b[0][8:9]+b[1]+b[2]+b[3]+b[4]+b[5][0:1] # final captcha
    print captcha
    br.select_form('parent_login')
    br.form['wdregno']=u
    br.form['vrfcd']=captcha
    response=br.submit()
    resp = br.open('https://academics.vit.ac.in/parent/marks.asp')
    page=resp.read()
    soup=BeautifulSoup(page)
    tr=soup('tr', bgcolor="#EDEADE", height="40") # taking all the tr tags
    if tr==[]:
        continue
    else:
        x=0 
        for i in tr:
            x=x+1  
            l=[[0 for j in range(20)] for i in range(x)]
            l1=[[0 for j in range(20)] for i in range(x)]
            td=[i.findAll('td') for i in tr]
            for i in range(x):
                for j in range(20):
                    if(td[i][4].contents[0]=="Lab Only" or td[i][4].contents[0]=="Embedded Lab" or td[i][4].contents[0]=="Project" ):
                        l[i][j]='null'
                        continue  
                    else:
                        if td[i][j].contents==[]:
                            l[i][j]='null'
                        else:
                            l[i][j]=td[i][j].contents[0].encode('ascii','ignore')

        l=[x for x in l if x !=['null' for j in range(20)]]   
       # print l[0],l[1]
        for i in range(len(l)):
            cursor.execute("INSERT INTO std VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[u,l[i][0],l[i][1],l[i][2],l[i][3],l[i][4],l[i][5],l[i][6],l[i][7],l[i][8],l[i][9],l[i][10],l[i][11],l[i][12],l[i][13],l[i][14],l[i][15],l[i][16],l[i][17],l[i][18],l[i][19]])
            print 'succes'
            db.commit()
db.close()



              
                
   
    









