from pyautogui import *

def main():
    screen = size()
    print(screen[0],screen[1])
    try:
        im = screenshot()
    except ImageNotFoundException:
        print("image not found!");
    im = im.save("ImageCatcher/test.jpg")




if __name__=='__main__':
    main()