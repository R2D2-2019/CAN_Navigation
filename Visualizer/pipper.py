import subprocess
import sys


def install_packages(packages: list):
    """
    Installs packages if not present.
    :param packages: list of packages you want to install
    """
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed = [r.decode().split('==')[0] for r in reqs.split()]

    for package in packages:
        if package == __name__:
            continue
        if package not in installed:
            subprocess.call(['pip', 'install', package])
        else:
            print("{} already installed.".format(package))
