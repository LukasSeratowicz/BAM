# BAM - Big AutoMation

**BAM** is a lightweight GUI tool designed to automate repetitive tasks in clicker games, idle games, and other simple workflows.
No more stacking items on top of your keyboard to hold a button down :)

---

## Features

- Basic support for keyboard and mouse automation  
- Simple, user-friendly interface  
- Early development stage — more features coming soon  

---

## Screenshot
![BAM Interface](https://github.com/user-attachments/assets/ccb856e7-9110-4e3c-852f-3aa96321ff7a)
*The current BAM interface*

---

## Notes

- Currently in very early development  
- Feedback and contributions are welcome  

---

## Changelog

### Future Versions:

- [ ] [BLOCK] **Capture Screen** - input: *x, y, width, height* - options: *none* - output: *image from the screen*
- [ ] [BLOCK] **Image to Text** - input: *image* - options: *color* - output: *text*
- [ ] [BLOCK] **Text to Int** - input: *text* - options: *base [Int]* - output: *integer*
- [ ] [BLOCK] **Text to Float** - input: *text* - options: *precision [Int]* - output: *float*
- [ ] [BLOCK] **Move Mouse** - input: *x, y* - options: *speed [String]* - output: *none*
- [ ] [BLOCK] **Mouse Click** - input: *button [String]* - options: *click_type [single/double]* - output: *none*
- [ ] [BLOCK] **Mouse Scroll** - input: *direction [String], amount [Int]* - options: *speed [String]* - output: *none*
- [ ] [BLOCK] **IF Statement** - input: *condition [Boolean]* - options: *none* - output: *executes block*
- [ ] [BLOCK] **WHILE Loop** - input: *condition [Boolean]* - options: *timeout [Int]* - output: *repeats block*
- [ ] [BLOCK] **FOR Loop** - input: *interval [Float] or trigger [String]* - options: *mode [periodic/trigger]* - output: *executes block*
- [ ] [BLOCK] **FLOAT Variable** - input: *float* - options: *name [String], on null [String]* - output: *said float*
- [ ] [BLOCK] **INT Variable** - input: *int* - options: *name [String], on null [String]* - output: *said int*
- [ ] [BLOCK] **BOOL Variable** - input: *int/bool* - options: *name [String], on null [String]* - output: *said bool/int*
- [ ] [BLOCK] **TEXT Variable** - input: *text* - options: *name [String], on null [String]* - output: *said text*
- [ ] [BLOCK] **ADD** - input: *int/float, int/float* - options: *variable1 minus? [Bool], variable2 minus? [Bool]* - output: *int/float*
- [ ] [BLOCK] **MULTIPLY** - input: *int/float, int/float* - options: *variable1 minus? [Bool], variable2 minus? [Bool]* - output: *int/float*
- [ ] [BLOCK] **DEVIDE** - input: *int/float, int/float* - options: *variable1 minus? [Bool], variable2 minus? [Bool]* - output: *int/float*
- [ ] [BLOCK] **App Dimensions** - input: *applications [List]* - options: *none* - output: *x, y, width, height of the app*
- [ ] Add the ability to save the current canvas as a single node to use in more advanced workflows
- [ ] Redesign Tool Bar on top
- [ ] Fix maaaany bugs

### **Version 0.2**

#### [Future Plan] **Major Release 0.2.0** - Branches Update
- [ ] Add support for multiple branches out of one node
- [ ] Rework the AutoSave system


### **Version 0.1**

#### [In Progress] **Release 0.1.9** - Mouse Node Update
- [ ] Separate Mouse Move from Clicking (Move is useless because Clicking moves, then clicks)

#### **Release 0.1.8** - Keyboard Node Update
- Keyboard Node should now support all keyboard keys

#### **Release 0.1.7** - Hotkeys Rework
- Start Blocks: now have Hotkeys to start each segment independently
- fixed F2: now more reliably stops all nodes from firing
- Reworked Nodes and Backdrop Highlights: end blocks do not clear the entire canvas
- Start Block Hotkeys are now also globally checked, no need for app focus

#### **Release 0.1.6** - Copy Paste
- Added Ctrl+C and Ctrl+V to copy paste currently selected node/s
- Fixed Multiple nodes selection: Shift-select, Ctrl-deselect
- Fixed mouse selection area

#### **Release 0.1.5** - Code Rework
- Refactor monolith code into a modular structure for development
- (no actual exe release, because no functional changes were implemented)

#### **Release 0.1.4** - Visualisations Update
- Nodes are now highlighted when active
- Backdrops are now highlighted when active
- Stop (or F2) now hard stops automation instead of soft stopping
- End Block now has 2 options: `Repeat` - go back to Start block | `Single` - finish and stop

#### **Major Release 0.1** - Preview Update
- Basic implementation of Mouse and Keyboard automation
- Basic GUI with block-nodes and backdrop for grouping
- Simultaneous block execution
- Multithreaded
- Save/Load system
- F1 - Start Hotkey | F2 - Stop Hotkey
- F3 - over the screen overlay to display X and Y coordinates of the mouse
