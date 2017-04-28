import pymysql;
import time;

conn = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = '6236336', db = 'test');
#before the test, please enter correct information and connect your databases.
#that is all information from my databases information, so I did not change them
#to connection mysql
cur  = conn.cursor();
#to set cursor
checking_email = cur.execute("select * from mailing;");
#to get all information from mailing table
info = cur.fetchmany(checking_email);
#info get all information
tmp = list(info);
# change type  tmp is list

#################################################################################################################
def seeTotalEmails(Email):         #calucate how many time to use a smae Domain of Email and sort them in a dict
    d = {};
    for x in set(Email):
        d[x] = Email.count(x);
    return d;
#################################################################################################################
def find_EmailDomain(estr):        #to del the user name before and include @ in the email address 
    jj = 0;                        #eg: hotmail.com, yahoo.com.cn
    while( jj < len(estr)):          
        if (estr[jj] == '@'):
            estr = estr[jj + 1:len(estr)-3];
            return estr;
        jj = jj + 1;
#################################################################################################################
def setAllDomain(tmp):
    i = 0;
    while ( i < len(tmp)):
        tmp[i] = find_EmailDomain(str(tmp[i]));
        i = i + 1;
    return tmp;
##################################################################################################################
def inserttable(information):
    setEmail = setAllDomain(tmp);      #sort every row domain of Email in the list
                                       #eg: hotmail.com, gmail.com, yahoo.con.cn in the list
    for i in information:
        cur.execute("insert into email values('%s','%d','%s');" %(i, information[i],todayDate));
##################################################################################################################
def selectDate():                      #to display the information form last 30 days compared to the total
    dateinformation = cur.execute("SELECT  * FROM email WHERE   ordertime BETWEEN now() - INTERVAL 30 DAY AND now()");
    info2 = cur.fetchmany(dateinformation);
    for x in info2:
        print(x);
##################################################################################################################
def topinformation():
    print ("Report:")
    cur.execute("select * from email;");
    report = {};
    row = cur.fetchone();
    while row is not None:
        if row[0] in report:
            report[row[0]] += row[1];
        else:
            report[row[0]] = row[1];
        row = cur.fetchone();
    sorted_report = sorted(report, key=report.__getitem__);
    sorted_report.reverse();
    Top50 = 1;
    for x in sorted_report:
        print( "%d: %s has %s" % (Top50, x,report[x]));
        Top50 = Top50 + 1;
        if Top50 > 50:
            break;
    print("End of Rrport");
##################################################################################################################
print("Checking the information start here !");
print("assume the mailling table has been create otherwise will run the follow code");
setEmail = setAllDomain(tmp);
print("Here will print out every row Domain of Email in the table mailing ");
print(setEmail);
information = seeTotalEmails(setEmail);  #sort how many number in a domain of email in dict
                                         #eg (hotmail.com : N, gmail.com : N)
print("Number of each domain will be sort into databases:");
print(information);
print("********************************************************************");
todayDate = time.strftime("%Y-%m-%d");    #to get time information and will insert other new table later
cur.execute("create table email(Domain varchar(255) NOT NULL ,Count int,OrderTime Date)");
#to create a new table and insert all sort data
inserttable(information);                 #to get function inserttable for insert all information in a new table
checkingEnter1 = input("If you want to know last 30 days compared to the total enter y or n: ");
#to check user want to see information for last 30 days
if (checkingEnter1 == 'y'):
    selectDate();

checkingEnter2 = input("If you want to know the top 50 domains by count sorted by last 30 day enter y or n: ");
if (checkingEnter2 == 'y'):
    topinformation();
print("Thany you very much to use this sript ! From Jianfei(Jae) Lin");

