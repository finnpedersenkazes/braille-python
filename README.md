# Braille Display and Linux

Being blind and using IT can be quite a challenge. But it is also an opportunity.

The intention with this project is to challenge the idea that braille solutions have to be expensive and for the few. Would it be possible to make games and applications for older braille displays at a relatively low cost? Would it be possible for students using Python to write these solutions?

## Project Structure

```
.
├── src/                    # Main library source code
│   └── __init__.py
├── examples/               # Example scripts demonstrating usage
│   ├── example01.py
│   ├── example01a.py
│   ├── example01b.py
│   ├── example02.py
│   ├── example02a.py
│   ├── example02b.py
│   ├── example02c.py
│   ├── example03.py
│   ├── example03a.py
│   ├── example03b.py
│   ├── example03c.py
│   ├── example03d.py
│   └── example04a.py
├── scripts/                # Utility scripts
│   ├── diagnostics.py
│   ├── setup_braille_display.sh
│   └── fix_brltty_installation.sh
├── tests/                  # Unit tests
│   └── __init__.py
├── docs/                   # Documentation
│   ├── Installation.md
│   └── BI 20X EN-UG 1.1.1.md
├── requirements.txt        # Project dependencies
├── pyproject.toml         # Modern Python project configuration
└── README.md              # This file
```

## BrlAPI

This solution is based on BrlAPI and BrlTTY.

https://brltty.app/

## Setup

### System Dependencies

See [docs/Installation.md](docs/Installation.md) for detailed installation instructions for different Linux distributions.

Quick start for Ubuntu/Raspberry Pi OS:

```bash
sudo apt update
sudo apt install brltty python3-brlapi python3-louis python3-venv
```

**Note:** `python3-brlapi` and `python3-louis` are system packages and are not available via pip.

### Python Environment Setup

Create a virtual environment with access to system packages (required for brlapi and louis):

```bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate  # On Linux/Mac
```

### Python Dependencies

Install Python dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

This will install:
- `python-xlib` - Required for keyboard input handling
- `pytest` - For running tests

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

### Running the Examples

Run example scripts from the project root:

```bash
python examples/example01.py
```

### Running Utilities

Use the diagnostic script to check your braille display setup:

```bash
python scripts/diagnostics.py
```

Use the setup script to configure your braille display:

```bash
bash scripts/setup_braille_display.sh
```

## System Installation

For detailed system-level installation and configuration instructions, see [docs/Installation.md](docs/Installation.md).

#### Raspberry Pi OS

Install the required packages:

```bash
sudo apt update
sudo apt install brltty python3-brlapi python3-louis python3-venv
```

Ensure BRLTTY starts automatically on boot and is running:

```bash
sudo systemctl enable brltty  # Enable to start automatically on boot
sudo systemctl start brltty   # Start the service now
```

**Important:** The `enable` command ensures BRLTTY starts automatically whenever the computer boots or reboots. This is essential for automatic operation without manual intervention.

Verify the installation:

```bash
brltty -v
python3 -c "import brlapi; import louis; print('Packages installed successfully')"
systemctl status brltty
```

**Note:** You may need to add your user to the `brltty` or `dialout` group to access the braille display:

```bash
sudo usermod -a -G brltty $USER
```

After adding yourself to the group, log out and log back in for the changes to take effect.

**Configuration:** BRLTTY will automatically detect most braille displays. If you need to configure a specific device, edit `/etc/brltty.conf`. See the [BRLTTY Guidelines](https://brltty.app/guidelines.html) for distribution-specific configuration details.

#### Ubuntu 

Install the required packages:

```bash
sudo apt update
sudo apt install brltty python3-brlapi python3-louis python3-venv
```

Ensure BRLTTY starts automatically on boot and is running:

```bash
sudo systemctl enable brltty  # Enable to start automatically on boot
sudo systemctl start brltty   # Start the service now
```

**Important:** The `enable` command ensures BRLTTY starts automatically whenever the computer boots or reboots. This is essential for automatic operation without manual intervention.

Verify the installation:

```bash
brltty -v
python3 -c "import brlapi; import louis; print('Packages installed successfully')"
systemctl status brltty
```

**Note:** You may need to add your user to the `brltty` or `dialout` group to access the braille display:

```bash
sudo usermod -a -G brltty $USER
```

After adding yourself to the group, log out and log back in for the changes to take effect.

**Configuration:** BRLTTY will automatically detect most braille displays. If you need to configure a specific device, edit `/etc/brltty.conf`. See the [BRLTTY Guidelines](https://brltty.app/guidelines.html) for distribution-specific configuration details.

**Additional Resources:**
- [BRLTTY Official Website](https://brltty.app/)
- [BRLTTY Documentation](https://brltty.app/doc/)
- [BRLTTY Guidelines for Linux Distributions](https://brltty.app/guidelines.html)
- [BRLTTY Reference Manual](https://brltty.app/doc/Manual-BRLTTY/English/BRLTTY.html) 



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

[User's Guide](https://support.freedomscientific.com/Content/Documents/Manuals/Focus/Focus40Blue/Focus-40-Blue-Online-Users-Guide.htm)

[Updating the Focus Blue Firmware](https://support.freedomscientific.com/Downloads/Focus/Focus4Downloads)


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
