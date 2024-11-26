# Laddu Package Manager
import colorama
import requests
from sys import argv
from os import system
from time import sleep
from subprocess import run

# Setup
VERSION = f"laddu v1.4.6"
VERSION_RAW = "v1.4.6"
Depends = ['colorama','requests']
argc = len(argv)
cyan = colorama.Fore.LIGHTCYAN_EX
normal = colorama.Fore.RESET
l = "{"
r = "}"

def Sync():
    print(f"\n{cyan}::{normal} Resolving Dependencies...")
    sleep(3)
    print(f"{cyan}::{normal} Looking For Conflicting Packages...")
    sleep(3)
    print(f"\n{cyan}::{normal} Sync Explicit (1): {argv[2].split('/', 1)[-1]}")
    sleep(3)
    yn = input(f"\n\n{cyan}::{normal} Proceed with installation of {argv[2].split('/', 1)[-1]}? [Y/n] ")
    if yn.lower() == "y":
        # system("makepkg -C")
        repo = get_repo_url(username=argv[2].split('/', 1)[0],repo_name=argv[2].split('/', 1)[-1])
        system(f"git clone {repo}.git")
        print(" -> Gathered Repo Files")
        sleep(3)
        rev = input(f"\n{cyan}::{normal} Proceed with Review of PKGBUILD? [Y/n] ")
        if rev == "y":
            system(f"cd {argv[2].split('/', 1)[-1]} && cat PKGBUILD")
            system("cd ..")
            print("\n",end='')
            end()
        elif rev == "n":
            end()
    elif yn.lower() == "n":
        print(" -> error installing repo packages")


def get_repo_url(username, repo_name):
    if username != '--aur':
        url = f"https://github.com/{username}/{repo_name}"  # Remove .git from repo_name
        return url
    elif username == '--aur':
        url = f"https://aur.archlinux.org/{repo_name}"  # Remove .git from repo_name
        return url
    else:
        print(" -> Invalid repo url")
        exit(1)


def end():
    try:
        system(f"cd {argv[2].split('/', 1)[-1]} && makepkg -si --noconfirm")
        print(f"\n -> complete building package")
        system(f"sudo rm -rf ./{argv[2].split('/', 1)[-1]}")

    except Exception:
        print(" -> error with building package")

def update():
    print(f"{cyan}::{normal} Synchronizing Package Databases...\n")
    sleep(3)
    print(f"core is up to date")
    sleep(3)
    print(f"extra is up to date")
    sleep(3)
    print(f"\n{cyan}::{normal} Searching (1): laddu-{VERSION_RAW} For Upgrades...\n\n")
    sleep(3)
    gitpak='sudo pacman -S git'
    run(gitpak,shell=True)
    
    for i in range(len(Depends)):
        req='pip install {Depends[i]}'
        run(req,shell=True)
    

try:
    
    if argv[1] == "--build" or argv[1] == "-B":
        system(f"cd {argv[2]}")
        build = input(f"\n{cyan}::{normal} Proceed with Review of PKGBUILD? [Y/n] ")
        if build == "y":
            system(f"cd {argv[2].split('/', 1)[-1]} && cat PKGBUILD")
            system("cd ..")
            print("\n",end='')
            system(f" makepkg -si")
        elif build == "n":
            system(f" makepkg -si")
    
    if argv[1] == "-h" or argv[1] == "--help":
        print(f"Usage: laddu <flags> <package>\n")
        print("note[!]: use --aur/<repo> to install aur package.\nnote[!]: use <user>/<repo> to install git packages (for search, use --git).\n")
        print(f"laddu   {l}-B --build{r} -- Builds package")
        print(f"laddu   {l}-h --help{r} -- Reveals laddu Command interface")
        print(f"laddu   {l}-R --remove{r} -- Removes any given packages")
        print(f"laddu   {l}-S --sync{r} -- Sychronizes the laddu database and installs the given package")
        print(f"laddu   {l}-Ss --search{r} -- Searches and gives user with query")
        print(f"laddu   {l}-Syu -Sua --update{r} -- Updates laddu database to the latest") 

    if argv[1] == "-Syu" or argv[1] == "--update" or argv[1] == "-Sua":
        if argv[2] == None:
            update()
        else:
            update()
            Sync()

    if argv[1] == "-R" or argv[1] == "--remove":
        print(f"{cyan}::{normal} Resolving Conflicts...")
        sleep(3)
        yn = input(f"\n\n{cyan}::{normal} Do you want to remove {argv[2]}? [Y/n] ")
        if yn.lower() == "y":
            cmd = f'sudo pacman -R {argv[2].split("/", 1)[0]}'
            run(cmd,shell=True)
        elif yn.lower() == "n":
            print(" -> error removing repo packages")
            exit(1)

    if argv[1] == "-S" or argv[1] == "--sync":
        Sync()
              
    if argv[1] == "-Ss" or argv[1] == "--search":
        search_term = sys.argv[3]
        
        if sys.argv[2] == "--aur":
            url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={search_term}"
            response = requests.get(url)
        
            if response.status_code == 200:
                data = response.json()
                
                if data['resultcount'] == 0:
                    print("No results found.")
                else:
                    for result in data['results']:
                        print(f"Package Name: {result['Name']}\nDescription: {result['Description']}\n")
            else:
                print(f" -> error: failed to fetch data from AUR. HTTP Status Code: {response.status_code}")
        
        elif sys.argv[2] == "--git":
            url = f"https://api.github.com/search/repositories?q={search_term}"
            response = requests.get(url)
        
            if response.status_code == 200:
                data = response.json()
        
                if 'items' not in data:
                    print("No results found.")
                else:
                    for repo in data['items']:
                        print(f"Repository Name: {repo['name']}\nDescription: {repo['description']}\nURL: {repo['html_url']}\n")
            else:
                print(f" -> error: failed to fetch data from GitHub. HTTP Status Code: {response.status_code}")
        
        else:
            print(" -> error: invalid option. Use --aur or --git.")

        
    if argv[1] == "-V" or argv[1] == "--version":
        print(VERSION)
        
except IndexError:
    update()
    
except Exception as e:
    print(f" -> error: {e}")
