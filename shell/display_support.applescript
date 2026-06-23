-- 1. VSCode: activate, send Option+Ctrl+T, then Shift+Ctrl+2 to move to desktop 2
tell application "Visual Studio Code" to activate
delay 0.5
tell application "System Events"
	key code 17 using {option down, control down}
end tell
delay 0.5

on moveToDisplay(n)
    set triggerName to "move_to_display_" & n
    tell application "BetterTouchTool"
        trigger_named triggerName
    end tell
end moveToDisplay

-- shift control 2
moveToDisplay(2)
delay 1.0

-- 2. Safari: activate, send Option+Ctrl+E
tell application "Safari" to activate
delay 0.5
tell application "System Events"
	key code 14 using {option down, control down}
end tell