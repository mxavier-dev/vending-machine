# 🛒 Vending Machine

A simple, modular vending machine application that models *product inventory*, *purchase flow*, *payment handling*, and *change dispensing*. This repository contains the core logic and tests needed to run and extend a vending machine simulation or a real-world integration.

## 🚀 Features

- **Add/Remove Products**: Select products and manage your cart.
- **Real-Time Stock Control**: Stock updates dynamically as products are added or removed.
- **Change Calculation**: Detailed breakdown of change in bills and coins.
- **Modern UI**: Built with `customtkinter` for a sleek, user-friendly interface.

## 🛠️ Technologies

- **Python 3**
- **Customtkinter** (Graphical User Interface)

## 📸 Preview
<img width="230" height="400" alt="shot-2026-02-06_17-16-25" src="https://github.com/user-attachments/assets/7912b04f-c5b2-49f2-86be-137174c895cf" /><br>
*Main interface of the vending machine simulator*

## 📥 Installation

### ⚙️ Application

You can download the ready-to-use executable in the [Releases](https://github.com/mxavier-dev/vending-machine/releases/tag/v.1.1) section. *(Only for linux)*

### 🐍 Code
1. Clone the repository:
```bash
git clone https://github.com/mxavier-dev/vending-machine
```   
2. Install the required library:
```bash
pip install customtkinter
```
3. Run the project:

*(The example uses the English version, but if you are using the Portuguese version, copy the command below and replace `EN` to `PT-BR`.)*
```bash
python3 vending_machine_EN.py
```
> If display a error *'python3 not found'* make sure the python is installed.
> But if the error persists replace `python3` to `python`

## 💡 How It Works

- **Select Products**: Click on the product buttons to add items to your cart.
- **Manage Cart**: Use the "-1" buttons
 to remove items from your cart.
- **Enter Payment**: Type the amount of money you're inserting into the machine.
- **Complete Purchase**: Click "FINALIZE PURCHASE" to finalize your order and receive your change (if applicable).

## 📫 Contact

Developed by **Matheus de Freitas Xavier** • [Linkedin Profile](https://www.linkedin.com/in/matheus-xavier-a14b0732a)
