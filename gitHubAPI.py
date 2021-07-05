import os
import requests
from dotenv import load_dotenv
from github import Github

load_dotenv() # load all the environment variables from the .env file

SEARCH_KEYWORD_1 = "framework"
SEARCH_KEYWORD_2 = "language"
SEARCH_KEYWORD_3 = "library"
SEARCH_KEYWORD_4 = "package"
SEARCH_KEYWORD_5 = "architecture"
SEARCH_KEYWORD_6 = "platform"
SEARCH_KEYWORD_7 = "plugin"
SEARCH_KEYWORD_8 = "database"

TOTAL_READMES_TO_GET = 100

def generateQueryString():
  
  searchKeywords = SEARCH_KEYWORD_1 + " " + SEARCH_KEYWORD_2 + " " + SEARCH_KEYWORD_3 + " " + SEARCH_KEYWORD_5

  return searchKeywords + " " + "in:readme"

def downloadFile(url, saveAsName):
  if "counter" not in downloadFile.__dict__: 
    downloadFile.counter = 1
  
  # print('Downloading Readme file', downloadFile.counter, "/", LIMIT)
  
  response = requests.get(url, allow_redirects=True)
  saveAsLocation = 'Readme Files/' + saveAsName + '.md'
  # saveAsLocation = 'Readme/README' + str(downloadFile.counter) + '.md'
  # saveAsLocation = 'Readme Files/README' + str(downloadFile.counter) + '.md'  # counter + 1 to avoid 0th index in file name
  downloadFile.counter += 1
  open(saveAsLocation, 'wb').write(response.content)

def callGitHubSearchAPI():

  access_token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')

  # Creating a Github instance:
  githubObj = Github(access_token)

  githubObj = Github(base_url="https://api.github.com", login_or_token=access_token)

  repositories = githubObj.search_repositories(query = QUERY_STRING)

  readmesObtained = 0
  index = 0

  file = open('output.txt', 'w')

  while(readmesObtained < TOTAL_READMES_TO_GET):
    repo = repositories[index]
    languagesDict = repo.get_languages()
    
    if(len(languagesDict) > 0):  # filter out repos that have no language used
      
      saveAsName = 'README-' + str(readmesObtained + 1) + '-' + repo.full_name.replace("/","-")
      print('Obtaining', saveAsName)

      file.write(str(saveAsName) + '\n\n')
      file.write('Languages used: ' + str(languagesDict) + '\n\n\n')

      try:
        contents = repo.get_contents("README.md")
      except:
        try:
          contents = repo.get_contents("readme.md")
        except:
          try:
            contents = repo.get_contents("Readme.md")
          except:
            try:
              contents = repo.get_contents("README.mdown")
            except:
              try:
                contents = repo.get_contents("README.rst")
              except:
                try:
                  contents = repo.get_contents("README.adoc")
                except:
                  contents = repo.get_contents("README")

      url = contents.download_url
      
      downloadFile(url, saveAsName)

      readmesObtained += 1
    index += 1
  file.close()

QUERY_STRING = generateQueryString()

print(QUERY_STRING)

callGitHubSearchAPI()
