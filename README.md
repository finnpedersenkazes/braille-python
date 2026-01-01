# Braille Display and Linux

Being blind and using IT can be quite a challenge. But it is also an opportunity.

The intention with this project is to challenge the idea that braille solutions have to be expensive and for the few. Would it be possible to make games and applications for older braille displays at a relatively low cost? Would it be possible for students using Python to write these solutions?

## BrlAPI

This solution is based on BrlAPI and BrlTTY.

https://brltty.app/


### Installation 

#### Raspberry Pi OS

Install the required packages:

```bash
sudo apt update
sudo apt install brltty python3-brlapi python3-louis
```

Ensure BRLTTY is running:

```bash
sudo systemctl enable brltty
sudo systemctl start brltty
```

Verify the installation:

```bash
brltty -v
python3 -c "import brlapi; import louis; print('Packages installed successfully')"
```

**Note:** You may need to add your user to the `brltty` or `dialout` group to access the braille display:

```bash
sudo usermod -a -G brltty $USER
```

After adding yourself to the group, log out and log back in for the changes to take effect.

#### Ubuntu

Install the required packages:

```bash
sudo apt update
sudo apt install brltty python3-brlapi python3-louis
```

Ensure BRLTTY is running:

```bash
sudo systemctl enable brltty
sudo systemctl start brltty
```

Verify the installation:

```bash
brltty -v
python3 -c "import brlapi; import louis; print('Packages installed successfully')"
```

**Note:** You may need to add your user to the `brltty` or `dialout` group to access the braille display:

```bash
sudo usermod -a -G brltty $USER
```

After adding yourself to the group, log out and log back in for the changes to take effect.

For more detailed configuration instructions, visit the [BRLTTY documentation](https://brltty.app/doc/). 



## Equipment

Braille displays have been around for some time.
They become more and more capable, but they are expensive.


### B.Book

[eurobraille](https://www.eurobraille.com/product/note-taker-computer-b-book-32-cells/)

B.Book is a notetaker, a Braille computer and a Braille display, all-in-one, compact and autonomous.

The price is about 6.000 €. 

It replaces the earlier model the esytime Evolution which had a price tag of 6.900 €. 


### Brailliant BI 20X

[HumanWare](https://store.humanware.com/int/brailliant-bi-20x-braille-display.html)

The Brailliant BI 20X braille display has a SD card and some application capabilities like taking notes and a simple calculator. 3.000 €.


### Focus Blue 40

[Freedom Scientific](https://shop.vispero.com/collections/braille-displays)

The Focus Blue 40. 4th Gen. has no SD card or applications.
I paid 1500 € for a demo model. It is an older model, but quite robust.

- Focus 14 Blue 5th Gen costs 1400 €
- Focus 40 Blue 5th Gen costs 3200 €
- Focus 80 Blue 5th Gen costs 8500 €


This is expensive equipment, with few capabilities and quite closed application ecosystems.

## The project

The idea is to make these tools worth more and to especially make older models useful again.

The design is quite simple.

1) Use a Raspberry Pi computer with a braille display like the Focus Blue 40.

2) Connect the braille display with the Raspberry Pi and let the braille display be input and output.

3) Write programs in a high level language like Python.

## Architecture

I imagine using an architecture similar to the Elm Architecture.
https://guide.elm-lang.org/architecture/

**A Model** that represents the state of the program.

**An init function** that initialize the Model.

**A View function** that takes the Model and displays the current state on the braille display.

**An Update function** that takes the current model and a command (each key press on the braille display represents a unique command) and updates the model accordingly.

Then the program loops back to the View function and displays the new state.

## What is needed?

The programmer would have to
1) Define the Model
2) Write an Initialize function
3) Write a View function that maps the model to the display (8 x 2 x 40) braille dots.
4) Write an Update function that for each command updates the model.

With a boilerplate like this, many developers would be able to write applications and games for braille displays.

**The benefits are many**

- I hope to help blind people, especially kids, by giving them access to fun games, education, books, educational tools, teaching them programming and much more.

- I hope to give new life to older braille displays, that currently only can be used with VoiceOver and Jaws. This would give these old displays functionality like note taking, calculator, games and more

- I hope to make it more affordable. This would benefit people with less money.
