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

import warnings
from libopensesame.py3compat import *
from libopensesame.exceptions import osexception

class var_store(object):

	"""
	desc: |
		The `var` object provides access to experimental variables.
		Experimental variables are the variables that live in the GUI, and are
		commonly set as independent variables in the `loop` item, referred
		to using the square-bracket (`[my_variable]`) notation, and logged by
		the `logger` item.

		In addition to the functions listed below, the following semantics are
		supported:

		__Example__:

		~~~ .python
		# Set an experimental variable
		var.my_variable = u'my_value'
		# Get an experimental variable
		print(u'Subject nr = %d' % var.subject_nr)
		# Delete (unset) an experimental variable
		del var.my_variable
		# Check if an experimental variable exists
		if u'my_variable' in var:
		    print(u'my_variable exists!')
		# Loop through all experimental variables
		for var_name in var:
		    print(u'variable found: %s' % var_name)
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%
	"""

	def __init__(self, item, parent=None):

		"""
		visible: False

		desc:
			Constructor.

		arguments:
			item:
				desc:	The associated item.
				type:	item

		keywords:
			parent:
				desc:	The parent var_store (i.e. for the experiment) or `None`
						for no parent.
				type:	[var_store, NoneType]
		"""

		object.__setattr__(self, u'__item__', item)
		object.__setattr__(self, u'__parent__', parent)
		object.__setattr__(self, u'__vars__', {})
		object.__setattr__(self, u'__lock__', None)

	def __contains__(self, var):

		"""
		visible: False

		desc:
			Implements the `in` operator to check if a variable exists.
		"""

		if var in self.__vars__:
			return True
		if hasattr(self.__item__, var):
			warnings.warn(u'var %s is stored as attribute of item %s' \
				% (var, self.__item__.name))
			return True
		if self.__parent__ is not None:
			return self.__parent__.__contains__(var)
		return False

	def __delattr__(self, var):

		"""
		visible: False

		desc:
			Implements the `del` statement to delete a variable.
		"""

		if var in self.__vars__:
			del self.__vars__[var]
		if hasattr(self.__item__, var):
			warnings.warn(u'var %s is stored as attribute of item %s' \
				% (var, self.__item__.name))
			delattr(self.__item__, var)

	def __getattr__(self, var):

		"""
		visible: False

		desc:
			Implements property retrieval to allow direct access to variables.
		"""

		return self.get(var)

	def __setattr__(self, var, val):

		"""
		visible: False

		desc:
			Implements property assignment.
		"""

		self.__vars__[var] = val

	def get(self, var, default=None, _eval=True, valid=None):

		"""
		desc:
			Gets an experimental variable.

		arguments:
			var:
				desc:	The variable to retrieve.
				type:	[str, unicode]

		keywords:
			default:
				desc:	A default value in case the variable doesn't exist, or
						`None` for no default value.
				type:	any
			_eval:
				desc:	Determines whether the returned should be evaluated for
						variable references.
				type:	bool
			valid:
				desc:	A list of valid values, or `None` to allow all values.
				type:	[NoneType, list]

		example: |
			print('my_variable = %s' % var.get(u'my_variable'))
			# Equivalent to:
			print('my_variable = %s' % var.my_variable)
			# But if you want to pass keyword arguments you need to use `get()`:
			var.get(u'my_variable', default=u'a_default_value')
		"""

		if self.__lock__ == var:
			raise osexception(
				u"Recursion detected! Is variable '%s' defined in terms of itself (e.g., 'var = [var]') in item '%s'" \
				% (var, self.name))
		if var in self.__vars__:
			val = self.__vars__[var]
		elif hasattr(self.__item__, var):
			warnings.warn(u'var %s is stored as attribute of item %s' \
				% (var, self.__item__.name))
			val = getattr(self.__item__, var)
		elif self.__parent__ is not None:
			val = self.__parent__.get(var, default=default, _eval=_eval,
				valid=valid)
		elif default is not None:
			val = default
		else:
			raise osexception(
				u"Variable '%s' is not set in item '%s'.<br /><br />You are trying to use a variable that does not exist. Make sure that you have spelled and capitalized the variable name correctly. You may wish to use the variable inspector (Control + I) to find the intended variable." \
				% (var, self.__item__.name))
		if valid is not None and val not in valid:
			raise osexception(u'Variable %s should be in %s, not %s' \
				% (var, valid, val))
		if _eval:
			object.__setattr__(self, u'__lock__', var)
			val = self.__item__.eval_text(val)
			object.__setattr__(self, u'__lock__', None)
		if isinstance(val, bool):
			if val:
				return u'yes'
			return u'no'
		try:
			val = float(val)
		except:
			return val
		if int(val) == val:
			return int(val)
		return val

	def has(self, var):

		"""
		desc:
			Checks if an experimental variable exists.

		arguments:
			var:
				desc:	The variable to check.
				type:	[str, unicode]

		example: |
			if var.has(u'my_variable'):
				print(u'my_variable has been defined!')
			# Equivalent to:
			if u'my_variable' in var:
				print(u'my_variable has been defined!')
		"""

		return self.__contains__(var)

	def set(self, var, val):

		"""
		desc:
			Sets and experimental variable.

		arguments:
			var:
				desc:	The variable to assign.
				type:	[str, unicode]
			val:
				desc:	The value to assign.
				type:	any

		example: |
			var.set(u'my_variable', u'my_value')
			# Equivalent to
			var.my_variable = u'my_value'
		"""

		self.__setattr__(var, val)

	def unset(self, var):

		"""
		desc:
			Deletes a variable.

		arguments:
			var:
				desc:	The variable to delete.
				type:	[str, unicode]

		example: |
			var.unset(u'my_variable')
			# Equivalent to:
			del var.my_variable
		"""

		self.__delattr__(var)

	def __iter__(self):

		"""
		visible: False

		desc:
			Implements the iterator.
		"""

		return var_store_iterator(self)

	def __len__(self):

		"""
		visible: False

		desc:
			Returns the number of experimental variables that are stored in the
			`var_store` object.

		returns:
			desc:	The number of experimental variables.
			type:	int
		"""

		return len(self.__vars__)

	def vars(self):

		"""
		desc:
			Returns a list of experimental variables. Because experimental
			variables can be stored in multiple places, this list may not be
			exhaustive. That is, `u'my_var' in var` may return `True`, while
			u'my_var' is not in the list of variables as returned by this
			function.

		returns:
			desc:	A list of variable names.
			type:	list
		"""

		return sorted(list(self.__vars__.keys()))

	def items(self):

		"""
		desc:
			Returns a list of (variable_name, value) tuples. See [vars] for a
			note about the non-exhaustiveness of this function.

		returns:
			desc:	A list of (variable_name, value) tuples.
			type:	list
		"""

		return list(self.__vars__.items())

class var_store_iterator(object):

	def __init__(self, var):

		self.var = var
		self.vars = var.vars()

	def __iter__(self):

		return self

	def __next__(self):

		# For Python 3
		return self.next()

	def next(self):

		if len(self.vars) == 0:
			raise StopIteration
		return self.vars.pop()