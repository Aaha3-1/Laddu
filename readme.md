# Laddu // An AUR Helper
[![Workflow Status](https://img.shields.io/github/actions/workflow/status/Aaha3-1/Laddu/python-app.yml?style=for-the-badge&logo=arch-linux&color=B4B4EF&logoColor=D9E0EE&labelColor=302D41)](https://github.com/Aaha3-1/Laddu/actions) [![repo size](https://img.shields.io/github/repo-size/Aaha3-1/Laddu?color=%23DDB6F2&label=SIZE&logo=arch-linux&style=for-the-badge&logoColor=D9E0EE&labelColor=302D41)](https://github.com/Aaha3-1/Laddu) [![last commit](https://img.shields.io/github/last-commit/Aaha3-1/Laddu?style=for-the-badge&logo=arch-linux&color=8bd5ca&logoColor=D9E0EE&labelColor=302D41)](https://github.com/Aaha3-1/Laddu/commit) [![license](https://img.shields.io/github/license/Aaha3-1/Laddu?style=for-the-badge&logo=arch-linux&color=ee999f&logoColor=D9E0EE&labelColor=302D41)](https://raw.githubusercontent.com/Aaha3-1/Laddu/refs/heads/master/LICENSE)

`Laddu` Is a Small and Simple AUR Helper Which Was Programmed with Python

## Installation

to install Laddu, you can use the following script below:
```
sudo pacman -S --needed git base-devel
git clone --depth 1 https://github.com/Aaha3-1/Laddu.git
cd Laddu
makepkg -si
```

## Usage

`Laddu` can be used to install various packages from the AUR, or Any other PKGBUILD on github, or in your Hardrive.

- To install any `AUR` package, use:
  ```
  laddu -S --aur/<package>
  ```
- To install any `github` PKGBUILD file, use:
  ```
  laddu -S --git/<reponame>
  ```
- To install from `hardisk`, use:
  ```
  laddu -B <path>
  ```
- To install any alpm package (pacman), use:
  ```
  laddu -S --alpm/<package>
  ```

 > [!WARNING]  
 > Don't install random packages without making sure it is safe.
 > Always check the `PKGBUILD` file in case you download a virus. 
