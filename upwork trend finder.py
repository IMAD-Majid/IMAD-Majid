from time import sleep
import re
import cv2
import pyperclip as clipboard
from pyautogui import moveTo, click, press, hotkey, typewrite, position, screenshot, scroll, position as getMousePosition, rightClick

parentPath = ""

def locateElement(targetName, timeout):
    while True:
        print(f"{str(timeout).zfill(2)} : cursor on \"{targetName}\"", end="\r")
        sleep(1)
        timeout -= 1
        if (timeout < 0):
            print('\n')
            return position()


def locatedImage(snapshotName):
    template = cv2.imread(parentPath + snapshotName + ".png")
    screenshotPath = parentPath + "screenshot.png"
    screenshot().save(screenshotPath)
    screen = cv2.imread(screenshotPath)

    # Convert to grayscale if images are in color
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= 0.9:  # Example confidence threshold: 0.9
        return max_loc;
    else:
        return ();

def mouseTo(x, y):
    moveTo(x=x, y=y)
    pause(0.2)
    click()
     # - - - -


def enter():
    press("Enter")
     # - - - -

def pause(duration=0.5):
    sleep(duration)

def waitFor(snapshotName: str) -> None:
    while not locatedImage(snapshotName):
        print(f"...waiting for: {snapshotName}", end="\r")
        pause(1)
    print()

def clickOn(snapshotName: str) -> None:
    x, y = locatedImage(snapshotName)
    # Load the PNG image
    image = cv2.imread(parentPath + snapshotName + ".png")

    # Get the dimensions of the image
    h, w, channels = image.shape
    mouseTo(x + (w//2), y + int(h//2))

def waitThenClick(snapshotName: str) -> None:
    waitFor(snapshotName)
    clickOn(snapshotName)

def visitURL(urlToVisit: str) -> None:
    typewrite(f"location.href = '{urlToVisit}'")
    pause(1)
    enter()

trend= {}
pages = 10

print("open a new tab on the browser with a closed console window")
input("i am ready, start in 5 seconds")
for i in range(5):
    print(5-i)
    pause(1)
hotkey("f12")
pause(1)
for p in range(1, pages+1):
    visitURL(f"https://www.upwork.com/nx/search/jobs/?client_hires=1-9,10-&duration_v3=week&per_page=50&sort=recency&page={p}")
    pause(2)
    scripts = [
        "skills = '';",
        "document.querySelectorAll('span.air3-token').forEach(s => {if (!s.textContent.includes('+')) {skills += s.textContent + ', ';}});",
        "skillsString = document.createElement('span');",
        "skillsString.textContent = skills",
        "document.body.appendChild(skillsString)",
        "document.getSelection().selectAllChildren(skillsString);",
        "document.execCommand('copy');"
    ]
    for s in scripts:
        typewrite(s)
        pause(2)
        enter()
        pause(0.5)

    pause(1)
    extracted = clipboard.paste()
    for s in extracted.split(", "):
        if s == '':
            continue
        if s in trend:
            trend[s] += 1
        else:
            trend[s] = 0

print(trend)
with open("upwork trends.txt", 'w') as f:
    scores = set()
    for t in trend:
        scores.add(trend[t])
    for s in sorted(scores)[::-1]:
        for ts in trend:
            if trend[ts] == s:
                f.write(f"{ts}: {s}\n")
