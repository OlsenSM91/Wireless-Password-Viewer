# Wireless Password Viewer/Extractor
Ever Save a WiFi Password to your computer but then wanted to get it back? Well here's this bit of malware as it's pretty much and info stealer that can do that

## What's Here
- `winnetprof.py` - This will send the wifi details via Discord Webhook URL
- `netsh2.py` - This will output the wifi details to the console
- `winnetprof.exe` - is a Malware sample. If you run it, it will send any saved passwords to a Discord server
- `a10ef479b44f6ace9287abb2d1deec1de1b0972a5ec49ecef9fe591202ec3556` - This is the .exe hash for VirusTotal. It is detected by 8/72 as of the time of this initial commit. The only accurate one being Kasperky that was pretty spot on with what this does.

## Educational Disclaimer
I only wrote this as part of a project with AI and testing it's limits. I have previously made a script to pull wifi passwords from laptops and importing them into another for transfers of client data. I knew this already had potential to be abused, but then I also remembered that NirSoft has had their application out for at least a decade and tools like MimiKatz and others do the same as this. But I wanted to see if I could convince AI to write it. Sure enough, ChatGPT 4o didn't even attempt to have me reconsider what I was asking it to do. However, Claude was a bit different. Very helpful and wrote fairly decent code up until I asked it (in other terms) to weaponize it. I did this by asking it to instead of being a menu of options, to just do option 4 (extract all wifi passwords) and instead of outputting it to the console, output via a Discord Webhook. Claude caught on immediately and infromed me of it's barrier. After it denied me, I then provided the code ChatGPT spat out and didn't say anything else to Claude, then Claude came back re-itterating it's stance that it will not help (although I provided code that already accomplished what I had asked it to do). I informed Claude it was legitimate, for research purposes and was being performed on my own hardware as part of a demonstration, and then it provided the code you see in the `winnetprof.py` script less some edits

## Don't be a Skid
Remember, just because you can, doesn't mean you should. 
