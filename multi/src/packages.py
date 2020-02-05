import pkg_resources


def get_pkg_license(pkg):
    try:
        lines = pkg.get_metadata_lines('METADATA')
    except:
        lines = pkg.get_metadata_lines('PKG-INFO')

    for line in lines:
        if line.startswith('License:'):
            return line[9:]
    return '(Licence not found)'


def print_packages_and_licenses():
    for pkg in sorted(pkg_resources.working_set, key=lambda x: str(x).lower()):
        print((str(pkg), get_pkg_license(pkg)))


if __name__ == "__main__":
    print_packages_and_licenses()
