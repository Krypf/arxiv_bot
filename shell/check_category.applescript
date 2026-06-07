tell application "Safari"
    set fname to name of current tab of front window
end tell
set tid to AppleScript's text item delimiters
set AppleScript's text item delimiters to ".json"
set bare to first text item of fname
set AppleScript's text item delimiters to tid
return bare