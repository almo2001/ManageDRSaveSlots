import atexit
import json
import os
import re
import shutil
import sys

#-----------------------
# "constant" definitions

c_version = "V0.9.1"

c_almoDataPath = os.path.join(os.getenv('LOCALAPPDATA'), "AlmoDeadzoneRogueSaveManager")
c_almoDisclaimerFile = os.path.join(c_almoDataPath, "ADRSMDisclaimerAccepted.txt")
c_almoSaveLibraryPath = os.path.join(c_almoDataPath, "SaveLibrary")
c_almoSaveNamesFile = os.path.join(c_almoDataPath, "ADRSM-SlotNames.txt")
c_almoSaveBasenameWithPath = os.path.join(c_almoSaveLibraryPath, "ADRSM-SaveSlot-")
c_almoStateFile = os.path.join(c_almoDataPath, "ADRSMState.txt")
c_deadzoneSaveFilesPath = os.path.join(os.getenv('LOCALAPPDATA'), "Valhalla\\Saved\\SaveGames")
c_deadzoneSaveFile = os.path.join(os.getenv('LOCALAPPDATA'), "Valhalla\\Saved\\SaveGames\\ValSaveGame-steam-3228590-0.sav")
c_deadzoneSaveFile2 = os.path.join(os.getenv('LOCALAPPDATA'), "Valhalla\\Saved\\SaveGames\\ValSaveGame-steam-3228590-0Backup.sav")
c_dashes = "------------------------------------------------------------------------------------------"
c_maxSlots = 6

# --------------------
# function definitions

def CopyFromSlotToGame(slotNum):
	shutil.copy(c_almoSaveBasenameWithPath + str(slotNum) + ".sav", c_deadzoneSaveFile)
	shutil.copy(c_almoSaveBasenameWithPath + str(slotNum) + ".sav", c_deadzoneSaveFile2)
	return

def CopyFromGameToSlot(slotNum):
	if os.path.exists(c_deadzoneSaveFile) and os.path.exists(c_deadzoneSaveFile2):
		if os.path.getmtime(c_deadzoneSaveFile) > os.path.getmtime(c_deadzoneSaveFile2):
			shutil.copy(c_deadzoneSaveFile, c_almoSaveBasenameWithPath + str(slotNum) + ".sav")
		else:
			shutil.copy(c_deadzoneSaveFile2, c_almoSaveBasenameWithPath + str(slotNum) + ".sav")
	elif os.path.exists(c_deadzoneSaveFile):
			shutil.copy(c_deadzoneSaveFile, c_almoSaveBasenameWithPath + str(slotNum) + ".sav")
	elif os.path.exists(c_deadzoneSaveFile2):
			shutil.copy(c_deadzoneSaveFile2, c_almoSaveBasenameWithPath + str(slotNum) + ".sav")
	else:
		print("Could not find a save file.")
		print("I looked for " + c_deadzoneSaveFile + " or " + c_deadzoneSaveFile2 + ".")
		sys.exit(1)

def DisplayAllSaves():
	currentSlot = GetCurrentSaveSlotNum()
	PrintOpeningLine("Existing Save Slots")
	print
	nameDict = dict(sorted(GetSaveFileNamesDict().items()))
	for slotNum in nameDict:
		if(slotNum == currentSlot):
			print("*", end='')
		else:
			print(" ", end='')
		print(" Slot " + slotNum + ": " + nameDict[slotNum])
	print()
	print()

def DisplayDisclaimer():
	PrintOpeningLine("Disclaimer:")
	print()
	print("This tool is not in any way endorsed or supported by Prophecy Games.")
	print("If you suffer a loss of data after using this tool, please do not ask people")
	PrintEndingLine("about it in their discord channel. Also do not try to contect the developers.")
	print()
	response = input("Please type 'yes' and hit enter to indicate that you have read this:")
	if response.lower() == "yes":
		return True
	else:
		return False
		
def DisplayIntro():
	print()
	print("-----------------------------------------")
	print("Almo's Deadzone: Rogue Save File Manager!")
	print("Version " + c_version + ".")
	print("Prophecy Games does not endorse or support this tool. Use at your own risk, etc.")
	print("I think your Deadzone saves are here:")
	print(c_deadzoneSaveFilesPath)
	print("Please backup any .sav files there before using this tool.")
	print("You can find the library of save files at:")
	PrintEndingLine(c_almoSaveLibraryPath)
	print()

def DisplayOptions():
	print("Options: (S)witch (C)reate (R)ename (D)elete E(x)it")

def GetCurrentSaveSlotNum():
	with open(c_almoStateFile, "r") as almoStateFile:
		currentSaveSlot = almoStateFile.read()
	return currentSaveSlot

def GetListOfSaveFiles():
	listOfSaveFiles = os.listdir(c_almoSaveLibraryPath)
	listOfSaveFiles.sort()
	return listOfSaveFiles

def GetSaveFileNamesDict():
	with open(c_almoSaveNamesFile, "r") as listOfNamesDictFile:
		loadedDict = json.load(listOfNamesDictFile)
	return loadedDict

def Initialize():
	if not os.path.isdir(c_almoDataPath):
		os.makedirs(c_almoSaveLibraryPath)
		PrintOpeningLine("Save directory created.")
	else:
		PrintOpeningLine("Save directory exists.")

	if not os.path.exists(c_almoStateFile):
		WriteCurrentSlotNum(1)
		print("Status file created.")
	else:
		print("Status file exists.")

	if not os.path.exists(c_almoSaveNamesFile):
		with open(c_almoSaveNamesFile, "w") as almoSaveNamesFile:
			almoSaveNamesFile.write("{}")
		print("Save names file created.")
	else:
		print("Save names file exists.")
	
	listOfSaveFiles = GetListOfSaveFiles()
	if len(listOfSaveFiles) == 0:
		CopyFromGameToSlot(1)
		print("Slot 1 initialized with Deadzone's save data.")
		
		slotDict = { '1' : "Default" }
		WriteSlotDict(slotDict)
		
		listOfSaveFiles = GetListOfSaveFiles()
		if len(listOfSaveFiles) == 0:
			print("Unable to create initial save slot.")
			sys.exit(1)

	PrintEndingLine("Current save slot is #" + str(GetCurrentSaveSlotNum()) + ".")
	print()

def Pause():
	input("\nPress Enter to quit.")

def PrintOpeningLine(instr):
	print(c_dashes[0:len(instr)])
	print(instr)
	
def PrintEndingLine(instr):
	print(instr)
	print(c_dashes[0:len(instr)])

def SaveFileExists(saveNumber):
	return os.path.exists(c_almoSaveBasenameWithPath)

def WriteCurrentSlotNum(slotNum):
	with open(c_almoStateFile, "w") as almoStateFile:
		almoStateFile.write('{}'.format(slotNum))

def WriteSlotDict(slotDict):
	with open(c_almoSaveNamesFile, "w") as slotDictFile:
		json.dump(slotDict, slotDictFile, indent = 4)

# -----
# modes

def CreateSlot(slotDict):
	if len(slotDict) == c_maxSlots:
		print("Already at max slots.")
		return
	slotToUse = 0
	for i in range(1, c_maxSlots + 1):
		if str(i) not in slotDict:
			slotToUse = i
			break
	
	slotName = "Save " + str(slotToUse)
	slotDict[str(i)] = slotName
	CopyFromGameToSlot(slotToUse)
	WriteSlotDict(slotDict)
	print("Copied Deadzone's save data into slot " + str(slotToUse) + ".")
	
def DeleteSlot(slotDict, currentSaveSlotNum):
	if len(slotDict) == 1:
		print("Cannot delete last slot.")
		return
	
	keepgoing = True
	while keepgoing:
		keepgoing = False
		slotToDelete = input("Slot number to delete or e(x)it:")
		if slotToDelete == "x":
			print("No slot deleted.")
			return
		if slotToDelete not in slotDict:
			print("Not a valid slot number.")
			keepgoing = True
		elif slotToDelete == "1":
			print("May not delete Default slot.")
			keepgoing = True
		elif slotToDelete == currentSaveSlotNum:
			print("May not delete the currently selected slot.")
			keepgoing = True
			
	print("Preparing to delete slot " + slotToDelete + ": " + slotDict[slotToDelete] + ".")
	reallyDoIt = input("Are you sure? (y/n)")
	if reallyDoIt != "y":
		print("No slot deleted.")
		return

	slotDict.pop(slotToDelete)
	WriteSlotDict(slotDict)
	os.remove(c_almoSaveBasenameWithPath + str(slotToDelete) + ".sav")
	print("Deleted slot " + slotToDelete + ".")
		
def RenameSlot(slotDict):
	if len(slotDict) <= 1:
		print()
		PrintEndingLine("Cannot rename Default slot.")
		print()
		return

	keepgoing = True
	while keepgoing:
		keepgoing = False
		slotToRename = input("Slot number to rename or e(x)it:")
		if slotToRename == "x":
			print("Did not rename a slot.")
			return
		if slotToRename not in slotDict:
			print("Not a valid slot number.")
			keepgoing = True
		if slotToRename == "1":
			print("Cannot rename Default slot.")
			keepgoing = True
		
	keepgoing = True
	while keepgoing:
		keepgoing = False
		newName = input("New name for slot number " + str(slotToRename) + ":")
		if not re.fullmatch(r"[A-Za-z0-9 ]*", newName) and len(newName) <= 20:
			print("Not a valid name. Please use only letters, numbers, and spaces. Names must be 20 characters or less.")
			keepgoing = True
			
	slotDict[slotToRename] = newName
	WriteSlotDict(slotDict)
	
	print("Renamed slot " + slotToRename + ".")

def SwitchSlot(slotDict, currentSaveSlotNum):
	if len(slotDict) <= 1:
		print()
		PrintEndingLine("No slot to switch to.")
		print()
		return
	
	keepgoing = True
	while keepgoing:
		keepgoing = False
		slotToSwitchTo = input("Slot number to switch to or e(x)it:")
		if slotToSwitchTo == "x":
			print("Did not switch slots.")
			return
		if slotToSwitchTo not in slotDict:
			print("Not a valid slot number.")
			keepgoing = True
		elif slotToSwitchTo == currentSaveSlotNum:
			print("May not switch to the currently selected slot.")
			keepgoing = True
			
	CopyFromGameToSlot(currentSaveSlotNum)
	CopyFromSlotToGame(slotToSwitchTo)
	WriteCurrentSlotNum(slotToSwitchTo)
	print("Switched to slot " + slotToSwitchTo + ".")

# -------
# program

atexit.register(Pause)

if not os.path.exists(c_almoDisclaimerFile):
	if DisplayDisclaimer():
		with open(c_almoDisclaimerFile, "w") as almoDisclaimerAcceptedFile:
			almoDisclaimerAcceptedFile.write("Yes. Accepted. Totally fine. No, really. It's cool.")
	else:
		print("Disclaimer not accepted. Exiting tool.")
		sys.exit(1)

DisplayIntro()
Initialize()
CopyFromGameToSlot(GetCurrentSaveSlotNum())

exitProgram = False
while not exitProgram:
	slotDict = GetSaveFileNamesDict()
	currentSaveSlotNum = GetCurrentSaveSlotNum()
	
	DisplayAllSaves()
	DisplayOptions()
	selectedOption = input("Select an option:")
	
	match selectedOption.lower():
		case "s":
			SwitchSlot(slotDict, currentSaveSlotNum)
			
		case "c":
			CreateSlot(slotDict)

		case "r":
			RenameSlot(slotDict)

		case "d":
			DeleteSlot(slotDict, currentSaveSlotNum)

		case "x":
			print()
			PrintEndingLine("Done messing with your save slots.")
			exitProgram = True

		case _:
			print("That's not an option.")






