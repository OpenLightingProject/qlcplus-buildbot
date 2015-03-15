#!/usr/bin/python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Create dummy password files for QLC+ buildbot slaves to aid with checking
# buildbot config.

import os
import config_helper

config = config_helper.LoadConfig('build.config')
slaves = config_helper.SlaveStore(config['SLAVES'])

print "Starting"

for slave in slaves.GetSlaves():
  print "Checking slave %s" % slave.name()
  pass_path = slave.password_file_path();
  if (not os.path.isfile(pass_path)) and (not os.path.exists(pass_path)):
    print "\tPassword file %s doesn't exist, creating a dummy one" % pass_path
    open(pass_path, "a").close()
    if os.path.isfile(pass_path):
      print "\tSuccessfully created a dummy file at %s" % pass_path
