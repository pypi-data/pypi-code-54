################################################################################
#
#    Copyright 2015-2020 Félix Brezo and Yaiza Rubio
#
#    This program is part of OSRFramework. You can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

import argparse
import json
import sys
import urllib2

import osrframework.thirdparties.infobel_com.checkPhoneDetails as infobel_com

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A library that wraps a search onto infobel.com via Google.', prog='checkPhoneDetails.py', add_help=False)
    # Adding the main options
    # Defining the mutually exclusive group for the main options
    parser.add_argument('-q', '--query', metavar='<query>', action='store', help='query to be performed to infobel.com.', required=True)

    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    groupAbout.add_argument('--version', action='version', version='%(prog)s 0.1.0', help='shows the version of the program and exists.')

    args = parser.parse_args()

    print(json.dumps(infobel_com.checkPhoneDetails(query=args.query), indent=2))
