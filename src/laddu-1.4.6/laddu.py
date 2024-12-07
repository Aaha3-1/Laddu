import colorama
import requests
from sys import argv
from os import system
from time import sleep
from subprocess import run

# Setup
VERSION_RAW = "v1.4.6"
VERSION = f"laddu-{VERSION_RAW}"
pkg_name_desc = {}
pkg_name_version = {}
Depends = ['colorama', 'requests', '--upgrade pip']
argc = len(argv)
cyan = colorama.Fore.LIGHTCYAN_EX
normal = colorama.Fore.RESET
l = "{"
r = "}"

def search(search_term, aur=False, git=False):
    if aur:
        package = search_term.split('/', 1)[-1]
        url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={package}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['resultcount'] == 0:
                print(f" -> No AUR packages found for '{search_term}'")
            else:
                for i, result in enumerate(data['results'], start=1):
                    pkg_name_desc[i] = result['Name']
                    pkg_name_version[i] = result['Version']
                    print(f"{i}. Package Name: {result['Name']}\nDescription: {result['Description']}\nVersion: {result['Version']}\n")
        else:
            print(f" -> error: failed to fetch data from AUR. HTTP Status Code: {response.status_code}")
    
    elif git:
        package = search_term.split('/', 1)[-1]
        url = f"https://api.github.com/search/repositories?q={package}"
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
    
            if 'items' not in data:
                print(f" -> No Git packages found for '{search_term}'")
            else:
                for i, repo in enumerate(data['items'], start=1):
                    pkg_name_desc[i] = repo['name']
                    pkg_name_version[i] = repo['default_branch']
                    print(f"{i + 1}. Repository Name: {repo['name']}\nDescription: {repo['description']}\nURL: {repo['html_url']}\nDefault Branch: {repo['default_branch']}\n")
        else:
            print(f" -> error: failed to fetch data from GitHub. HTTP Status Code: {response.status_code}")
    
    else:
        print(" -> error: invalid option. Use --aur or --git.")

def sync(package):
    if "--aur" in package:
        search(package.split('--aur/')[1], aur=True)
        source = "aur"
    elif "--git" in package:
        search(package.split('--git/')[1], git=True)
        source = "git"
    else:
        search(package)
        source = "unknown"

    option = int(input('Enter Package Number (e.g. 1,2,3,4):\n==> '))
    selected_pkg = pkg_name_desc[option]
    selected_version = pkg_name_version[option]
    sleep(3)
    print(f"\n{cyan}::{normal} Resolving Dependencies...")
    sleep(3)
    print(f"{cyan}::{normal} Looking For Conflicting Packages...")
    sleep(3)
    print(f"\n{cyan}::{normal} Sync Explicit: {selected_pkg}-{selected_version}")
    sleep(3)
    yn = input(f"\n\n{cyan}::{normal} Proceed with installation of {selected_pkg}-{selected_version}? [Y/n] ")
    if yn.lower() == "y":
        if source == "aur":
            repo_url = get_repo_url(username="aur", repo_name=selected_pkg)
        else:
            repo_url = get_repo_url(username=selected_pkg.split('/', 1)[0], repo_name=selected_pkg.split('/', 1)[-1])
        system(f"git clone {repo_url}.git")
        print(" -> Gathered Repo Files")
        sleep(3)
        rev = input(f"\n{cyan}::{normal} Proceed with Review of PKGBUILD? [Y/n] ")
        if rev.lower() == "y":
            system(f"cd {selected_pkg.split('/', 1)[-1]} && cat PKGBUILD")
            system("cd ..")
            print("\n", end='')
            end()
        elif rev.lower() == "n":
            end()
    elif yn.lower() == "n":
        print(" -> error installing repo packages")

def get_repo_url(username, repo_name):
    if username == "aur":
        return f"https://aur.archlinux.org/{repo_name}"
    else:
        return f"https://github.com/{username}/{repo_name}"

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
    gitpak = 'sudo pacman -S git'
    run(gitpak, shell=True)
    
    for dep in Depends:
        req = f'pip install {dep}'
        run(req, shell=True)

try:
    if argv[1] == "--build" or argv[1] == "-B":
        system(f"cd {argv[2]}")
        build = input(f"\n{cyan}::{normal} Proceed with Review of PKGBUILD? [Y/n] ")
        if build.lower() == "y":
            system(f"cd {argv[2].split('/', 1)[-1]} && cat PKGBUILD")
            system("cd ..")
            print("\n", end='')
            system(" makepkg -si")
        elif build.lower() == "n":
            system(" makepkg -si")
    
    if argv[1] == "-h" or argv[1] == "--help":
        print(f"Usage: laddu <flags> <package>\n")
        print(f"{cyan}::{normal} Note: use --aur/<repo> to install aur package.\n{cyan}::{normal} Note: use <user>/<repo> to install git packages (for search, use --git).\n")
        print(f"laddu   {l}-B --build{r} -- Builds package from hardrive")
        print(f"laddu   {l}-h --help{r} -- Reveals laddu Command interface")
        print(f"laddu   {l}-R --remove{r} -- Removes any given packages")
        print(f"laddu   {l}-S --sync{r} -- Sychronizes the laddu database and installs the given package")
        print(f"laddu   {l}-Ss --search{r} -- Searches and gives user with query")
        print(f"laddu   {l}-Syu -Sua --update{r} -- Updates laddu database to the latest")

    if argv[1] == "-Syu" or argv[1] == "--update" or argv[1] == "-Sua":
        if len(argv) < 3:
            update()
        else:
            update()
            sync(argv[2])

    if argv[1] == "-R" or argv[1] == "--remove":
        print(f"{cyan}::{normal} Resolving Conflicts...")
        sleep(3)
        yn = input(f"\n\n{cyan}::{normal} Do you want to remove {argv[2]}? [Y/n] ")
        if yn.lower() == "y":
            cmd = f'sudo pacman -R {argv[2].split("/", 1)[0]}'
            run(cmd, shell=True)
        elif yn.lower() == "n":
            print(" -> error removing repo packages")
            exit(1)

    if argv[1] == "-S" or argv[1] == "--sync":
        sync(argv[2])

    if argv[1] == "-Ss" or argv[1] == "--search":
        search(argv[3], aur=True if '--aur' in argv else False, git=True if '--git' in argv else False)
        
    if argv[1] == "-V" or argv[1] == "--version":
        print(VERSION)
        
except IndexError:
    update()
except Exception as e:
    print(f" -> error: {e}")
