#pip imports
#pip install gspread oauth2client
# pip install praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import praw
from pprint import pprint
import os
scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
] #scope


# https://stackoverflow.com/questions/63512788/how-to-fix-the-google-auth-exceptions-refresherror-no-access-token-in-respon
SPREADSHEET_LOCATION = os.environ.get('REDDIT_SHEET_MANAGER_GSPREAD_SPREADSHEET_LOCATION')

PRAW_CLIENT_ID = os.environ.get('REDDIT_SHEET_MANAGER_PRAW_CLIENT_ID')
PRAW_CLIENT_SECRET = os.environ.get('REDDIT_SHEET_MANAGER_PRAW_CLIENT_SECRET')
REDDIT_USERNAME= os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open(SPREADSHEET_LOCATION).sheet1

data = sheet.get_all_records() # all records that we will use
stillSavedPosts = [] #will be populated with ones still saved indexes, then we will call sort 
# print(data[0])

# row = sheet.row_values(1)
# column = sheet.column_values(1)
# cell = sheet.cell(1, 2).value

# try:
#     find = sheet.find("heufue", in_column=1)
#     print('found')
# except gspread.exceptions.CellNotFound:
#     print('not found')
# https://stackoverflow.com/questions/59446405/python-gspread-cellnotfound-exception-error
# col = int(find._col)
# row= int(find._row)
# https://stackoverflow.com/questions/61599272/google-sheets-search-column-for-value-using-python
# pprint(vars(find))

# sheet.update_cell(row, col, 'new name')




reddit = praw.Reddit(client_id =PRAW_CLIENT_ID, 
client_secret= PRAW_CLIENT_SECRET,
username= REDDIT_USERNAME,
password= REDDIT_PASSWORD,
user_agent='redditSheetManagerv1' )



# print("rigfRED'stwitco5")

# pprint(data)

# subreddit = reddit.subreddit('python')

# for submission in subreddit.hot(limit=500):
#     print(submission.title)

user = reddit.user.me()
savedUrls =[] # dict of saved urls

# print(user)

# saved = user.saved(limit=1)

# for item in saved:
#     print(vars(saved))

#https://stackoverflow.com/questions/610883/how-to-know-if-an-object-has-an-attribute-in-python

#item values that we need
# subreddit name = item.subreddit.display_name
# post title = item.title
# post link = item.permalink
# post external link = item.url


def getAlreadyInserted(): #insertion of already existing into list , called in pull and remove
    for r in data:
        savedUrls.append(r.get('reddit link'))
        # print(r.get('reddit link'))
        # print("----")
def pullFromRedditSaved(): #pull from reddit saved function
    getAlreadyInserted()
    print("Pulling from your saved...")
    try:
        for item in user.saved(limit=None):
            postSubName=item.subreddit.display_name
            postTitle=''
            postLink="https://www.reddit.com/"+item.permalink
            postExternalUrl=''
            postCreationTime=float(item.created)
            # print(postSubName)
            if(hasattr(item,'title')):
                postTitle=item.title # assigning title
            if(hasattr(item,'url' )):
                postExternalUrl=item.url
            if(postLink not in savedUrls): #not in dictionary
                insertRow = [postSubName, postTitle,postLink, 
                    postExternalUrl, postCreationTime]
                sheet.append_row(insertRow) # append to the end
                # print(insertRow)
                savedUrls.append(postLink)
    except gspread.exceptions.APIError:
        print("Exceeded Google Sheet (gspread) API calls, please wait 1 minute")

# gspread.exceptions.APIError
def removeUnsaved(): #remove saved function
    getAlreadyInserted()
    print("Removing Unsaved...")
    savedOnSite=[]
    for item in user.saved(limit=None):
        postLink="https://www.reddit.com/"+item.permalink
        savedOnSite.append(postLink)
    for inSheet in savedUrls:
        if(inSheet not in savedOnSite):
            findOut = sheet.find(inSheet, in_column=3)
            sheet.delete_rows(int(findOut._row))

def clearSheet():
    print("clearing sheet...")
    sheet.clear()

def checkNumeric( userInput):
    if(not userInput.isnumeric()): 
        return False
    return True

def checkRange(userInput, range):
    inputVal= int(userInput)-1
    if(inputVal>range):
        return False
    return True
        
userOptions = [ pullFromRedditSaved , removeUnsaved]
# https://stackoverflow.com/questions/27472704/store-functions-in-list-and-call-them-later

print("Enter the number of the command you want to enter: ")

counter=0
for opt in userOptions:
    counter+=1
    print(str(counter)+") "+ opt.__name__)

userChoice=input(' ')

checkingNumeral = checkNumeric(userChoice)

while( not checkingNumeral):
    userChoice=input('Enter a number less than '+str(counter+1)+': ')
    checkingNumeral= checkNumeric(userChoice)

choiceVal = int(userChoice)-1
userOptions[choiceVal]()



# pullFromRedditSaved()
# oldpullFromRedditSaved()
# removeUnsaved()



##