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

- [ ] Implement CV (Computer Vision) blocks (e.g. find colour, find pattern, find face, find human, and so on...)
- [ ] Implement More automation like Scroll, Type Text, Send Email, ...
- [ ] Implement Simple Scripting - Add Variables and If/Else Statement blocks
- [ ] Add the ability to save the current canvas as a single node to use in more advanced workflows
- [ ] Redesign UI
- [ ] Fix maaaany bugs

### Version 0.1

- [ ] Finish implementing Keyboard (right now, most keys do not work)
- [ ] Fix mouse selection area (broken in current PySide version, might need to monkey-patch it)
- [ ] Add Ctrl+C and Ctrl+V to copy paste currently selected node/s
- [ ] Add support for multiple branches out of one node
- [ ] Separate Mouse Move from Clicking (Move is useless because Clicking moves, then clicks)
- [ ] F2 doesn't always stop all nodes from firing

#### Release 0.1.4 - Visualisations Update
- Nodes are now highlighted when active
- Backdrops are now highlighted when active
- Stop (or F2) now hard stops automation instead of soft stopping
- End Block now has 2 options: `Repeat` - go back to Start block | `Single` - finish and stop

#### Release 0.1 - Preview Update
- Basic implementation of Mouse and Keyboard automation
- Basic GUI with block-nodes and backdrop for grouping
- Simultaneous block execution
- Multithreaded
- Save/Load system
- F1 - Start Hotkey | F2 - Stop Hotkey
- F3 - over the screen overlay to display X and Y coordinates of the mouse
