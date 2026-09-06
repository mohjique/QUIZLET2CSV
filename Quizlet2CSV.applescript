-- Quizlet2CSV
-- Drag a saved Quizlet flashcard-set HTML page onto this app to convert it
-- into a CSV of term/definition pairs, written next to the original file.
-- Double-clicking the app instead shows instructions, then lets you pick
-- the file(s) from a picker.

on open theFiles
	processFiles(theFiles)
end open

on run
	set introText to "Quizlet2CSV converts a saved Quizlet flashcard-set page into a clean term/definition CSV — ready to hand to an AI for studying." & return & return & ¬
		"How to use:" & return & ¬
		"1. On quizlet.com, open the flashcard set, then press Cmd+S and save it as \"Webpage, Complete.\"" & return & ¬
		"2. Drag the saved .html file onto this app icon (or click \"Choose File(s)…\" below)." & return & return & ¬
		"The resulting .csv is saved right next to the original .html file, with the same name, and Finder will open to reveal it automatically."

	set iconPosixPath to POSIX path of ((path to me as text) & "Contents:Resources:droplet.icns")
	try
		set iconRef to (POSIX file iconPosixPath) as alias
	on error
		set iconRef to missing value
	end try

	try
		if iconRef is missing value then
			display dialog introText buttons {"Cancel", "Choose File(s)…"} default button "Choose File(s)…" with title "Quizlet2CSV" with icon note
		else
			display dialog introText buttons {"Cancel", "Choose File(s)…"} default button "Choose File(s)…" with title "Quizlet2CSV" with icon iconRef
		end if
	on error number -128
		-- user cancelled
		return
	end try

	try
		set chosenFiles to choose file with prompt "Select one or more saved Quizlet flashcard-set HTML files:" of type {"public.html"} with multiple selections allowed
	on error number -128
		-- user cancelled the picker
		return
	end try

	processFiles(chosenFiles)
end run

on processFiles(theFiles)
	set pyScriptPath to POSIX path of ((path to me as text) & "Contents:Resources:quizlet_html_to_csv.py")

	set successCount to 0
	set failMessages to {}

	repeat with aFile in theFiles
		set filePosix to POSIX path of aFile
		try
			set shellCmd to "/usr/bin/env python3 " & quoted form of pyScriptPath & " " & quoted form of filePosix
			set resultText to do shell script shellCmd
			if resultText starts with "FAILED" then
				set end of failMessages to resultText
			else
				set successCount to successCount + 1
				-- Reveal the generated CSV in Finder
				set csvPosix to (do shell script "echo " & quoted form of filePosix & " | sed 's/\\.[^.]*$/.csv/'")
				try
					tell application "Finder" to reveal (POSIX file csvPosix)
					tell application "Finder" to activate
				end try
			end if
		on error errMsg
			set end of failMessages to (filePosix & " — " & errMsg)
		end try
	end repeat

	if (count of failMessages) > 0 then
		set AppleScript's text item delimiters to linefeed
		set failText to failMessages as text
		set AppleScript's text item delimiters to ""
		display dialog (successCount as text) & " file(s) converted.\n\nProblems:\n" & failText buttons {"OK"} default button "OK" with icon caution
	end if
end processFiles
