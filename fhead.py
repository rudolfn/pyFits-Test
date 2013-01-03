#!/usr/bin/env python

#    freeFITS.py: modify license information in FITS header
#    Copyright (C) 2013  Zdeněk Janák <janak@physics.muni.cz>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import warnings
import argparse
import pyfits
import sys


## keywords
lickeys = ("LICENSE", "LICVER", "LICURL")


## licenses
liclist = {
    "cc0": {
        "name": "CC0",
        "ver": "1.0",
        "url": "http://creativecommons.org/publicdomain/zero/1.0/"
    },
    "cc_by": {
        "name": "CC BY",
        "ver": "3.0",
        "url": "http://creativecommons.org/licenses/by/3.0/"
    },
    "cc_by_sa": {
        "name": "CC BY-SA",
        "ver": "3.0",
        "url": "http://creativecommons.org/licenses/by-sa/3.0/"
    },
    "cc_by_nd": {
        "name": "CC BY-ND",
        "ver": "3.0",
        "url": "http://creativecommons.org/licenses/by-nd/3.0/"
    },
    "cc_by_nc": {
        "name": "CC BY-NC",
        "ver": "3.0",
        "url": "http://creativecommons.org/licenses/by-nc/3.0/"
    },
    "cc_by_nc_sa": {
        "name": "CC BY-NC-SA",
        "ver": "3.0",
        "url": "http://creativecommons.org/licenses/by-nc-sa/3.0/"
    },
    "cc_by_nc_nd": {
        "name": "CC BY-NC-ND",
        "ver": "3.0",
        "url": "http://creativecommons.org/licenses/by-nc-nd/3.0/"
    },
    "pdm": {
        "name": "Public Domain Mark",
        "ver": "1.0",
        "url": "http://creativecommons.org/publicdomain/mark/1.0/"
    }
}


def list_licenses(licenses):
    """Print list of available licenses"""
    #print("Available licenses:\n")
    for license in licenses:
        print("{0}: {name} {ver} ({url})".format(license, **licenses[license]))


def info_license(fitsfile):
    """Print license information stored in FITS"""
    try:
        license = pyfits.getval(fitsfile, "LICENSE")
    except KeyError:
        print("License information not found.")
    else:
        licver = pyfits.getval(fitsfile, "LICVER")
        licurl = pyfits.getval(fitsfile, "LICURL")
        print("{lic} {ver} ({url})".format(lic=license, ver=licver, url=licurl))


def add_license(fitsfile, lic):
    """Add license information to FITS"""
    try:
        hdulist = pyfits.open(fitsfile, mode="update")
    except:
        print("Oops! Something's gone wrong :-(", file=sys.stderr)
    else:
        prihdr = hdulist[0].header
        prihdr["LICENSE"] = liclist[lic]["name"]
        prihdr["LICVER"] = liclist[lic]["ver"]
        prihdr["LICURL"] = liclist[lic]["url"]
        add_comments(prihdr)
        hdulist.close()


def add_comments(header):
    """Add comments to header keywords"""
    try:
        header.comments["LICENSE"] = "License of data"
        header.comments["LICVER"] = "Version of license"
        header.comments["LICURL"] = "URL of license"
    except:
        print("Oops! Something's gone wrong :-(", file=sys.stderr)


def del_license(fitsfile, keys):
    """Delete license information from FITS"""
    try:
        for key in keys:
            pyfits.delval(fitsfile, key)
    except KeyError:
        print("License information not found.", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fitsfile",
                        help="name of FITS file")
    parser.add_argument("-l", "--list",
                        help="list available licenses", action="store_true")
    parser.add_argument("-i", "--info",
                        help="show license information in FITS file",
                        action="store_true")
    parser.add_argument("-a", "--add",
                        help="add license information to FITS file")
    parser.add_argument("-d", "--delete",
                        help="delete license information from FITS file",
                        action="store_true")
    args = parser.parse_args()

    if args.list:
        list_licenses(liclist)
    elif args.info:
        info_license(args.fitsfile)
    elif args.add:
        add_license(args.fitsfile, args.add)
    elif args.delete:
        del_license(args.fitsfile, lickeys)
