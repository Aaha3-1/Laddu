# Laddu // An AUR Helper

`Laddu` Is a Small and Simple AUR Helper Which Was Programmed with Python

## Installation

to install Laddu, you can use the following script below:
```
sudo pacman -S --needed git base-devel
git clone https://github.com/Aaha3-1/Laddu
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
  laddu -S <user>/<reponame>
  ```
- To install from hardisk, use:
  ```
  laddu -B <path>
  ```
