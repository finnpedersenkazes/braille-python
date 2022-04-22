# Braille Display and Raspberry Pi

Being blind and using IT can be quite a challenge. But it is also an opportunity.

The intension with this project is to challenge the idea that braille solutions have to be expensive and for the few. Would it be possible to make games and applications for older braille displays at a relatively low cost? Would it be possible for students using Python to write these solutions?

## BrlAPI

I have just discovered BrlAPI and BrlTTY.

## Equipment

Braille displays have been around for some time.
They become more and more capable, but they are expense.


The esytime Evolution is a 6.900 € windows computer with a braille keyboard and display.

The Brailliant BI 20X braille display has a SD card and some application capabilities like taking notes and a simple calculator. 2.700 €.

The Focus Blue 40. 4th Gen. has no SD card or applications.
I paid 1500 € for a demo model. It is an older model, but quite robust.

This is expensive equipment, with few capabilities and quite closed applications.

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

- I hope to help blind people, especially kids, but giving them access to fun games, education, books, educational tools, teaching them programming and much more.

- I hope to give new life to older braille displays, that currently only can be used with VoiceOver and Jaws. This would give these old displays functionality like note taking, calculator, games and more

- I hope to make it more affordable. This would benefit people with less money.
