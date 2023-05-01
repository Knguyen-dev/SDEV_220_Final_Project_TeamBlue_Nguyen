from tkinter import *
# File that contains useful functions that are used frequently

## strips the input of entry widget of trailing or leading whitespace
def stripEntryWidgets(entryWidgets):
	strippedWidgets = []
	for entry in entryWidgets:
		inputValue = entry.get().strip()
		entry.delete(0, END)
		entry.insert(0, inputValue)
		strippedWidgets.append(entry)
	return strippedWidgets

## Checks if any one of the entry widgets in the list entryWidgets has no input
def isEmptyEntryWidgets(entryWidgets):
	for entry in entryWidgets:
		if entry.get() == "":
			return True
	return False