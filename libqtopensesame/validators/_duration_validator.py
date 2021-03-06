#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt4 import QtCore, QtGui
from _base_validator import base_validator

class duration_validator(base_validator):

	"""
	desc:
		A validator for durations.
	"""

	def __init__(self, main_window, default=u'keypress'):

		super(duration_validator, self).__init__(main_window, default=default)

	def is_valid(self, val):

		if val in [u'keypress', u'mouseclick', u'sound'] \
			or self.experiment.varref(val):
			return True
		try:
			int(val)
			return True
		except:
			return False
