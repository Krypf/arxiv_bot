set R to {}
set n to 6

repeat n times
    copy (random number from 0.3 to 0.5) to end of R
end repeat

-- log R

tell application "System Events"
    -- Press T (copy tweet text & advance to next)
    key code 17
    delay item 1 of R
    -- Switch to Twitter tab
    key code 48 using {control down}
    delay item 2 of R
    -- Press N to open new tweet box
    key code 45
    delay item 3 of R
    -- Paste copied text
    key code 9 using {command down}
    delay (item 4 of R + 0.5)
    -- Post tweet (Cmd+Enter)
    key code 36 using {command down}
    delay (item 5 of R + 1.0)
    -- Switch back to arXiv Poster tab
    key code 48 using {control down, shift down}
    delay (item 6 of R + 0.5)
end tell