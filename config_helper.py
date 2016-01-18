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
# Helper code for the QLC+ buildbot configs.

import os


def LoadConfig(config_file):
  """Load the buildbot config from a config file."""
  config = {}
  global_dict = {
    'Slave': SlaveConfig,
  }
  execfile(config_file, global_dict, config)
  return config


class SlaveConfig(object):
  def __init__(self, suffix, has_cpp_lint=False, has_js_lint=False,
               has_tcmalloc=False, is_slow=False, generate_doc=False,
               generate_man=False, no_build=False):
    self._suffix = suffix
    self._has_cpp_lint = has_cpp_lint
    self._has_js_lint = has_js_lint
    self._has_tcmalloc = has_tcmalloc
    self._is_slow = is_slow
    self._generate_doc = generate_doc
    self._generate_man = generate_man
    self._no_build = no_build

  @property
  def suffix(self):
    return self._suffix

  @property
  def has_cpp_lint(self):
    return self._has_cpp_lint

  @property
  def has_js_lint(self):
    return self._has_js_lint

  @property
  def has_tcmalloc(self):
    return self._has_tcmalloc

  @property
  def is_slow(self):
    return self._is_slow

  @property
  def generate_doc(self):
    return self._generate_doc

  @property
  def generate_man(self):
    return self._generate_man

  @property
  def no_build(self):
    return self._no_build


class BuildSlave(object):
  def __init__(self, platform, arch, slave_config):
    self._platform = platform
    self._arch = arch
    self._suffix = slave_config.suffix
    self._has_cpp_lint = slave_config.has_cpp_lint
    self._has_js_lint = slave_config.has_js_lint
    self._has_tcmalloc = slave_config.has_tcmalloc
    self._is_slow = slave_config.is_slow
    self._generate_doc = slave_config.generate_doc
    self._generate_man = slave_config.generate_man
    self._no_build = slave_config.no_build

  def name(self):
    """Return the name of this slave."""
    return '%s-%s-%s' % (self._platform, self._arch, self._suffix)

  def password_file_path(self):
    """Get the file path that contains the password for this slave."""
    return os.path.join(os.path.dirname(__file__), "%s.pass" % self.name())

  def password(self):
    """Get the password for this slave."""
    path = self.password_file_path()
    return open(path).read().strip()

  @property
  def has_cpp_lint(self):
    return self._has_cpp_lint

  @property
  def has_js_lint(self):
    return self._has_js_lint

  @property
  def has_tcmalloc(self):
    return self._has_tcmalloc

  @property
  def is_slow(self):
    return self._is_slow

  @property
  def generate_doc(self):
    return self._generate_doc

  @property
  def generate_man(self):
    return self._generate_man

  @property
  def no_build(self):
    return self._no_build


def HasCPPLintFilter(slave):
  """Filter on slaves that have C++ lint installed."""
  return slave.has_cpp_lint


def HasJSLintFilter(slave):
  """Filter on slaves that have JS lint installed."""
  return slave.has_js_lint


def HasTCMalloc(slave):
  """Filter on slaves that have tcmalloc installed."""
  return slave.has_tcmalloc


def IsSlow(slave):
  """Filter on slaves that are slow."""
  return slave.is_slow

def GenerateDoc(slave):
  """Filter on slaves that generate doxygen doc."""
  return slave.generate_doc


def GenerateMan(slave):
  """Filter on slaves that generate man pages."""
  return slave.generate_man


def HasBuild(slave):
  """Filter on slaves that perform builds."""
  return not slave.no_build


class SlaveStore(object):
  """Holds the BuildSlave objects."""
  def __init__(self, slave_config):
    self._slaves = []
    for platform, platform_spec in slave_config.iteritems():
      for arch, slave_names in platform_spec.iteritems():
        for slave in slave_names:
          self._slaves.append(BuildSlave(platform, arch, slave))

  def GetSlaves(self, slave_filter=None):
    """Returns all slaves matching the optional filter."""
    if slave_filter is None:
      return self._slaves[:]
    else:
      return [s for s in self._slaves if slave_filter(s)]
