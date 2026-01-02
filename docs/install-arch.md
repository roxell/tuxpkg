## Installing the Arch Linux packages


!!! note
    tuxpkg requires Python 3.6 or newer.


### Method 1: Using pacman repository

If the pacman database is available, you can install using the repository:

1. Create /etc/pacman.d/tuxpkg.conf with the following contents:

```
[tuxpkg]
SigLevel = Optional TrustAll
Server = https://linaro.gitlab.io/tuxpkg/packages/
```

2. Include it from /etc/pacman.conf. Add one line at the bottom:

```
Include = /etc/pacman.d/*.conf
```

If you already have this line, do nothing.

3. Sync and install:

```shell
# pacman -Syu
# pacman -S tuxpkg
```

Upgrades will be available in the same repository.

### Method 2: Manual download and install

If the pacman database is not available, download and install manually:

```shell
# curl -LO https://linaro.gitlab.io/tuxpkg/packages/tuxpkg-VERSION-any.pkg.tar.zst
# pacman -U tuxpkg-VERSION-any.pkg.tar.zst
```

Replace VERSION with the desired version number.
