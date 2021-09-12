import os
from dotenv import load_dotenv
from github import Github

load_dotenv() # load all the environment variables from the .env file

TOTAL_REPOS_TO_GET = 100
MIN_STARS = 50
MIN_WATCHING = 50

OUTPUT_FILE_NAME = 'repos.txt'

languageDict = {}


def updateLanguageStats(languages):
  for language in languages:
    if language in languageDict:
      languageDict[language] += 1
    else:
      languageDict[language] = 1

def getRepos(githubObj, minStarCount, minWatchCount, outputFileName):
  
  emptyFile(outputFileName)

  print('\nFiltering Repos...\n')

  repositories = githubObj.get_repos()

  index = 0
  reposObtainedSoFar = 0

  while(reposObtainedSoFar < TOTAL_REPOS_TO_GET):
    
    repo = repositories[index]

    print('Checking repo number {}'.format(index + 1))

    try:
      repoStars = repo.stargazers_count
      repoWatchers = repo.subscribers_count
    except:
      print('There is a problem with the repository number {}, {}\n Ignored\n'.format(index + 1, repo.html_url))
      repoStars = -1
      repoWatchers = -1

    if(repoStars >= minStarCount and repoWatchers >= minWatchCount):
      reposObtainedSoFar += 1
      
      print('\nFound {} repos so far\n'.format(reposObtainedSoFar))

      updateLanguageStats(repo.get_languages())


      writeToFile(outputFileName, str(reposObtainedSoFar), repo.full_name, repo.html_url)
    
    index += 1



def searchRepos(githubObj, minStarCount, minWatchCount, outputFileName):
  
  emptyFile(outputFileName)

  print('\nFiltering Repos...\n')

  repositories = githubObj.search_repositories(query = 'stars:>={}'.format(minStarCount))

  index = 0
  reposObtainedSoFar = 0

  while(reposObtainedSoFar < TOTAL_REPOS_TO_GET):
    
    repo = repositories[index]

    print('Checking repo number {}'.format(index + 1))

    try:
      repoStars = repo.stargazers_count
      repoWatchers = repo.subscribers_count
    except:
      print('There is a problem with the repository number {}, {}\n Ignored\n'.format(index + 1, repo.html_url))
      repoStars = -1
      repoWatchers = -1

    if(repoStars >= minStarCount and repoWatchers >= minWatchCount):
      reposObtainedSoFar += 1
      
      print('\nFound {} repos so far\n'.format(reposObtainedSoFar))
      
      writeToFile(outputFileName, str(reposObtainedSoFar), repo.full_name, repo.html_url)
    
    index += 1

def emptyFile(outputFileName):
  file = open(outputFileName, "w")
  file.close()

def writeToFile(outputFileName, srNo, repoName, repoUrl):
  file = open(outputFileName, "a")
  repoInfoString = srNo + " " + repoName + " " + repoUrl + '\n\n'
  file.write(repoInfoString)
  file.close()

def createGithubObj():
  access_token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')

  # Creating a Github instance:
  githubObj = Github(access_token)

  githubObj = Github(base_url="https://api.github.com", login_or_token=access_token)

  return githubObj

githubObj = createGithubObj()

getRepos(githubObj, MIN_STARS, MIN_WATCHING, OUTPUT_FILE_NAME)

print(languageDict)

print('Program Terminated')
