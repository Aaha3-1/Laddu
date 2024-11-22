# Maintainer: Aaha3 <Aaha3.sh@gmail.com>

pkgname='laddu'
pkgver='1.4.6'
pkgrel=1
pkgdesc="laddu -S <package> | Useful AUR helper written in Python."
arch=('x86_64')
url=""
license=('GPL')
depends=('git','Python','colorama')
makedepends=(python-build python-install python-wheel)
source=('laddu::<giturl>')
sha256sums=(SKIP)

pkgver() {
         cd "$pkgver"
         git describe --long --abrev=7 | sed 's/\([^-]*-g\)/r\1/;s/-/./g' 
}

build() {
	cd "$pkgname-$pkgver"
        python -m build --wheel --no-isolation	
}

package() {
	cd "$pkgname-$pkgver"
	python -m installer --destdir="$pkgdir" dist/*.whl
}
