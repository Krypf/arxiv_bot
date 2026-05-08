tell application "System Events"
	-- T
	key code 17
	delay 3.0
	-- Cmd+Enter
	key code 36 using {command down}
	delay 2.0
	-- Cmd+W
	key code 13 using {command down}
	delay 1.0
	-- return
	key code 36
end tell