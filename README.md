# Battleship

We decided to make the classic game of Battleship in Python. We decided that we would use a 10x10 grid, and 5 ships. One 5 length, one 4 length, one 3 length, one horizontal 4 length, and one horizontal 2 length. We also decided that it would be more interesting if we were to use an AI as the second player, a proper UI instead of console programming, and object based programming.

# Python Object Based Programming

Early on we realized that it would be beneficial to use the object based functionality that Python provides, mainly classes. The idea behind object based programming is that you can create a template(a class) with given attributes and functionality as many times as you need it. For instance, if you were making a game and you wanted to have lots similar or identical enemies, and for each one of those particular enemies you needed to keep track of their health, and position. For each one you'd also want to have a function to attack the player, move, and die. While you could create functions and lots of different global variables to accomplish, it would be far easier to create a class. Here is the pseudocode for the class described above:

```python
class Enemy:
  def __init__(self, position, health):
    self.position = position
    self.health = health
    
  def move(self, distance):
    self.position += distance
    # Move the player model here
    
  def attack(self):
    # Attack code here
    
  def check_health(self):
    if self.health == 0:
      # Die code here
  ```
  
Now, for each enemy I want I simply have to initialize the class as a variable:
  
```python
enemy1 = Enemy(5, 10)
enemy2 = Enemy(1, 1)
```

While this may seem complicated, it is actually very simple.

Here is a breakdown of what everything means:

1. The __init__() is what's called a constructor. It constructs the class, and any parameters, other than "self" which we will discuss later, need to be provided when initializing any objects created from the class. In this case, health and position need to be provided to the class.
  
2. Self is the object. Self.anything means that variable is a parameter of the object, and **can have a unique value for each instance of the class**. Those variables can be accessed in any function of the class by calling self.variablename. They can also be accessed outside of the function by calling classvariablename.variablename. They can also be created at any time, in any function in or outside of the class as long as they follow the conventions above. 

Another use of a class is as a storage system. You can have a class that you only initialize once, but you can have all of your related variables as parameters of the class instead of global variables, simplifying your program. We used classes in a variety of circumstances, ranging from when we needed to make a 100 different buttons to cover a grid to when we needed to making a menu with only one global variable. 


# Python UI Programming

We decided that UI based programming would make our program more interesting, despite the challenges it poses. Pythons UI library is called Tkinter, or TK Interface. Everything in Tkinter has to be done with code. In Tkinter you have a screen, usually called "main" or "root", but creating this makes a blank screen. You can then add Buttons, Labels, Text Boxes, and Canvases(Used for displaying images, and creating other geometric things) to this screen. If you want to change windows(For instance going from a menu screen to a settings screen) you need to create a Frame, and store the objects that make up these screens in this Frame. For instance:

```python
import tkinter as tk  # Common convention, renaming Tkinter into something more concise

root = tk.Tk()  # Main screen
menu = tk.Frame(root)  # The parameter is what the frame is going to be displayed on
settings = tk.Frame(root)
menuLabel = tk.Label(menu, text="Menu:")
menuLabel.pack()  # This places the menu label into its parent, in this case the menu object
settingsLabel = tk.Label(settings, text="Settings:")
settingsLabel.pack()
menu.pack()  # This finally places something we can see
root.mainloop()  # This generates the main window
```

There is obviously a lot more that can be done with this, and a lot more to be explained, but that is the basics for UI Programming.

# Combining UI and Object Based Programming
In the last example, we created 5 global variables, making a non-functional menu and settings window. As you can imagine, when creating a functional UI it is very easy to create lots of global variables to make your UI work. Naturally, this can quickly add complexity to your program, making it harder and more time consuming to understand and debug. A simple way to manage this complexity is with classes. Here is a quick example on how the above example into 3 global variables:

```python
import tkinter as tk

class Window(tk.Frame):  # This imports from the Frame class, making your class an extention of the frame class
  def __init__(self, parent, name, *args, **kwargs):  
  # Parent is the parent of your frame, name is the name of your frame, 
  # *args and **kwargs are simply any other arguments provided, which can be used in the frame
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.label =  tk.Label(self, text=name)
    self.label.pack()
    
    
 root = tk.Tk()
 settings = Window(root, "settings")
 menu = Window(root, "menu")
 menu.pack()
 root.mainloop()
 ```
 
That example condensed the previous 5 global variables into 3, which isn't a big difference, but keep in mind that every element on the menu and settings screen is another global variable, so if you have 5 different options from your menu screen and 5 in your settings screen on top of the labels, that's 15 global variables condensed into 3 which is a huge difference! We used this almost every time we needed to something related to UI programming.
    
 
