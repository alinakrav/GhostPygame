# Alina Kravchenko  101113276
import pygame
pygame.init()

instructions = """\nYou must provide 2 image files. The first image
given will be the background, and the second will be the foreground that will
appear as a 'ghost' at the specified coordinate. Either drag these images,
one by one, from your file manager into the terminal, or enter the file names
(with the extension) manually with single quotes around each file (do not separate
them with anything else). The files should be given in this format:
'background_image.bmp''foreground_image.bmp'
You will be asked your preferred method of entering the coordinates, as you can
either enter them through the terminal, or move your cursor around the window
with the background image and click."""
if input("Do you need instructions for this program? (y/n)\t\t") == "y":
    print(instructions)

# keep prompting user for file names, ask to give instructions if they fail to enter them correctly
while True:
    try:
        i1, i2 = input("\nDrag your files here:\n").split("''")
        break
    except ValueError as error:
        if input("\nRepeat the instructions? (y/n)\t\t") == "y":
            print(instructions)
# create pygame window, load back and foreground images (i1 is background, i2 is foreground), then paste background onto the window
win = pygame.display.set_mode()
i1, i2 = pygame.image.load(i1[1:]).convert(), pygame.image.load(i2[:-1]).convert()
pygame.display.set_mode((i1.get_width(), i1.get_height()))
win.blit(i1, (0, 0))
# declare the variables that will be used for ghost's centre coordinates
xCentre, yCentre = 0, 0
# ask user which method they want to use for coordinate selection
selectMethod = input("\nDo you want to use the terminal or mouse to select coordinates? (t/m)\t\t")
if selectMethod == "t":
    # check that THE CENTRE of the ghost will be within the window's bounds
    while True:
        xCentre, yCentre = [int(a) for a in input("\nEnter valid coordinates for the ghost, separated by a comma.\t\t").split(",")]
        if (xCentre >= 0) and (yCentre >= 0) and (win.get_width() > xCentre) and (win.get_height() > yCentre):
            break
else:
    print("\nGo to the Pygame window and select.\n")
    # create Font object
    pygame.font.init()
    myFont = pygame.font.SysFont(None, 20)
    #  keep getting mouse's coordinates and drawing them, in black, right where the cursor is
    while True:
        xMouse, yMouse = pygame.mouse.get_pos()
        win.blit(myFont.render("({}, {})".format(xMouse, yMouse), True, (0, 0, 0)), (xMouse, yMouse))
        pygame.display.update()
        # redraw the background to prepare for new text being drawn on the next loop iteration
        win.blit(i1, (0, 0))
        # when the mouse is clicked, save the mouse's coordinates and exit the while loop since the ghost's centre is now selected
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                xCentre, yCentre = xMouse, yMouse
        if xCentre == xMouse:
            break

# for each column, and each row of the ghost image
for xGhost in range(i2.get_width()):
    for yGhost in range(i2.get_height()):
        # calculate background coordinates where the ghost pixels should be copied, in relation to where the middle of the ghost image is
        xBkgd, yBkgd = xCentre - int(i2.get_width()/2) + xGhost, yCentre - int(i2.get_height()/2) + yGhost
        # get the current ghost pixel's colour value, then see if it's green based on its approximate RGB values
        rgbaGhost  = i2.get_at((xGhost, yGhost))
        green = (rgbaGhost[0] < 10) and (rgbaGhost[2] < 80) and (rgbaGhost[1] > 245)
        # if pixel isn't green and is in bounds of the background, copy its colour averaged with the background (for translucent effect)
        if (not green) and (xBkgd >= 0) and (yBkgd >= 0) and (win.get_width() > xBkgd) and (win.get_height() > yBkgd):
            rgb1 = win.get_at((xBkgd, yBkgd))
            r1, g1, b1 = rgb1[0], rgb1[1], rgb1[2]
            rgb2 = i2.get_at((xGhost, yGhost))
            r2, g2 , b2 = rgb2[0], rgb2[1], rgb2[2]
            win.set_at((xBkgd, yBkgd), ((r1+r2)/2, (b1+b2)/2, (g1+g2)/2))
pygame.display.update()

# force pygame window to stay open until user closes it
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
