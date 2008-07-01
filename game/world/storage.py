# ###################################################
# Copyright (C) 2008 The OpenAnno Team
# team@openanno.org
# This file is part of OpenAnno.
#
# OpenAnno is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from game.util.stablelist import stablelist

class Storage(object):
	"""Class that represent a storage compartment with fixed resources slots
	
	Is inherited by Producer and Consumer.
	"""
	def __init__(self):
		# inventory: a dict with this pattern: _inventory[res_id] = (amount, size)
		self._inventory = {}
		
	def addSlot(self, res_id, size):
		""" Add the possibility to save size amount of res_id
		@param res_id: id of the resource
		@param size: maximum amount of res_id that can be stored here; -1 for infinity
		"""
		self._inventory[res_id] = [0, size]

	def alter_inventory(self, res_id, amount):
		"""Alters the inventory for the resource res_id with amount.
		@param res_id: int resource_id
		@param amount: amount that is to be added."""
		try:
			new_amount = self._inventory[res_id][0] + amount;
		except KeyError:
			return 0
		if new_amount > self._inventory[res_id][1] and self._inventory[res_id][1] != -1: 
			# stuff doesn't fit in inventory
			ret = new_amount - self._inventory[res_id][1]
			self._inventory[res_id][0] = self._inventory[res_id][1]
			return ret
		elif new_amount < 0:
			# trying to take more stuff than inventory contains
			ret = new_amount
			self._inventory[res_id][0] = 0
			return ret
		else:
			# new amount is in boundaries
			self._inventory[res_id][0] = new_amount
			return 0

	def get_value(self, res_id):
		"""Returns amount of resource res_id in the storage
		@param res_id: int resource_id
		@return int amount of resources for res_id in inventory.
		"""
		try:
			return self._inventory[res_id][0]
		except KeyError:
			return 0
	
	def get_size(self, res_id):
		""" Returns the capacity of the storage for resource res_id
		@param res_id: int resource_id
		"""
		return self._inventory[res_id][1]
		
	def __repr__(self):
		return repr(self._inventory)

	def __str__(self):
		return str(self._inventory)


class ArbitraryStorage(object):
	"""Class that represents a storage compartment for ships
	Storages have a certain number of slots and a certain maximum number of
	resources that they can store for a certain slot.
	"""
	def __init__(self, slots, size):
		self._inventory = stablelist()
		self.slots = slots
		self.size = size
		
	def alter_inventory(self, res_id, amount):
		# try using existing slots
		for slot in self._inventory:
			if slot[0] == res_id:
				new_amount = slot[1] + amount
				if new_amount < 0:
					slot[1] = 0
					amount = new_amount
				elif new_amount > self.size:
					slot[1] = self.size
					amount = new_amount - self.size
					
		# handle stuff that couldn't be handled with existing slots
		if amount > 0:
			if len(self._inventory) < self.slots: 
				if amount > self.size:
					self._inventory.append([res_id, self.size])
					return self.alter_inventory(res_id, amount - self.size)
				else:
					self._inventory.append([res_id, amount])
					amount = 0
			
		# return what couldn't be added/taken
		return amount
	
	def get_value(self, res_id):
		ret = 0
		for slot in self._inventory:
			if slot[0] == res_id:
				ret += slot[1]
		return ret
	