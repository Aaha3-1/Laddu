import colorama
import requests
from sys import argv
from os import system
from time import sleep
from subprocess import run

# Setup
VERSION = "laddu v1.4.6"
VERSION_RAW = "v1.4.6"
pkg_name_desc = {}
Depends = ['colorama', 'requests', 'argparse']
cyan = colorama.Fore.LIGHTCYAN_EX
normal = colorama.Fore.RESET

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Laddu Package Manager')
    parser.add_argument('command', choices=['-S', '--sync', '-Ss', '--search', '-Syu', '--update', '-Sua', '--build', '-B', '-R', '--remove', '-h', '--help', '-V', '--version'], help='Command to execute')
    parser.add_argument('--aur', nargs='?', const=True, help='AUR search option')
    parser.add_argument('--git', nargs='?', const=True, help='GitHub search option')
    parser.add_argument('package', nargs='?', help='Package to operate on')
    return parser.parse_args()

def search(package, aur, git):
    if aur:
        url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={package}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['resultcount'] == 0:
                print("No results found.")
            else:
                for result in data['results']:
                    pkg_name_desc[result['Name']] = result['Description']
                    print(f"Package Name: {result['Name']}\nDescription: {result['Description']}\n")
        else:
            print(f" -> error: failed to fetch data from AUR. HTTP Status Code: {response.status_code}")
    elif git:
        url = f"https://api.github.com/search/repositories?q={package}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' not in data:
                print("No results found.")
            else:
                for i, repo in enumerate(data['items']):
                    print(f"{i + 1}. Repository Name: {repo['name']}\nDescription: {repo['description']}\nURL: {repo['html_url']}\n")
        else:
            print(f" -> error: failed to fetch data from GitHub. HTTP Status Code: {response.status_code}")
    else:
        print(" -> error: invalid option. Use --aur or --git.")

def sync(package):
    search(package, '--aur' in argv, '--git' in argv)
    option = input('Enter Package Number (eg. 0,1,2,3,4)\n==> ')
    sleep(3)
    print(f"\n{cyan}::{normal} Resolving Dependencies...")
    sleep(3)
    print(f"{cyan}::{normal} Looking For Conflicting Packages...")
    sleep(3)
    print(f"\n{cyan}::{normal} Sync Explicit (1): {pkg_name_desc[option]}")
    sleep(3)
    yn = input(f"\n\n{cyan}::{normal} Proceed with installation of {package}? [Y/n] ")
    if yn.lower() == "y":
        repo = get_repo_url(username=package.split('/', 1)[0], repo_name=package.split('/', 1)[-1])
        system(f"git clone {repo}.git")
        print(" -> Gathered Repo Files")
        sleep(3)
        rev = input(f"\n{cyan}::{normal} Proceed with Review of PKGBUILD? [Y/n] ")
        if rev.lower() == "y":
            system(f"cd {package.split('/', 1)[-1]} && cat PKGBUILD")
            system("cd ..")
            print("\n", end='')
            end()
        elif rev.lower() == "n":
            end()
    elif yn.lower() == "n":
        print(" -> error installing repo packages")

def get_repo_url(username, repo_name):
    if username != '--aur':
        return f"https://github.com/{username}/{repo_name}"
    elif username == '--aur':
        return f"https://aur.archlinux.org/{repo_name}"
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
    print("core is up to date")
    sleep(3)
    print("extra is up to date")
    sleep(3)
    print(f"\n{cyan}::{normal} Searching (1): laddu-{VERSION_RAW} For Upgrades...\n\n")
    sleep(3)
    gitpak = 'sudo pacman -S git'
    run(gitpak, shell=True)
    
    for dep in Depends:
        req = f'pip install {dep}'
        run(req, shell=True)

def main():
    args = parse_args()
    
    if args.command in ["--build", "-B"]:
        system(f"cd {args.package}")
        build = input(f"\n{cyan}::{normal} Proceed with Review of PKGBUILD? [Y/n] ")
        if build.lower() == "y":
            system(f"cd {args.package.split('/', 1)[-1]} && cat PKGBUILD")
            system("cd ..")
            print("\n", end='')
            system(" makepkg -si")
        elif build.lower() == "n":
            system(" makepkg -si")

    if args.command in ["-h", "--help"]:
        print(f"Usage: laddu <flags> <package>\n")
        print("note[!]: use --aur/<repo> to install aur package.\nnote[!]: use <user>/<repo> to install git packages (for search, use --git).\n")
        print(f"laddu   -B --build -- Builds package")
        print(f"laddu   -h --help -- Reveals laddu Command interface")
        print(f"laddu   -R --remove -- Removes any given packages")
        print(f"laddu   -S --sync -- Sychronizes the laddu database and installs the given package")
        print(f"laddu   -Ss --search -- Searches and gives user with query")
        print(f"laddu   -Syu -Sua --update -- Updates laddu database to the latest") 

    if args.command in ["-Syu", "--update", "-Sua"]:
        if args.package is None:
            update()
        else:
            update()
            sync(args.package)

    if args.command in ["-R", "--remove"]:
        print(f"{cyan}::{normal} Resolving Conflicts...")
        sleep(3)
        yn = input(f"\n\n{cyan}::{normal} Do you want to remove {args.package}? [Y/n] ")
        if yn.lower() == "y":
            cmd = f'sudo pacman -R {args.package.split("/", 1)[0]}'
            run(cmd, shell=True)
        elif yn.lower() == "n":
            print(" -> error removing repo packages")
            exit(1)

    if args.command in ["-S", "--sync"]:
        sync(args.package)
              
    if args.command in ["-Ss", "--search"]:
        search(args.package, args.aur, args.git)
        
    if args.command in ["-V", "--version"]:
        print(VERSION)
        
if __name__ == "__main__":
    main()
