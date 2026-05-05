tell application "System Events"
	-- T
	key code 17
	delay 2.0
	-- Enter
	key code 36
	delay 5.0
	-- Cmd+Enter
	key code 36 using {command down}
	delay 3.0
	-- Option+` (backtick)
	key code 50 using {option down}
	delay 1.0
end tell
