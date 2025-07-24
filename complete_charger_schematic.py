import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon
import numpy as np

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Title
ax.text(8, 11.5, '3S Li-ion Battery Charger System with BQ24610', 
        fontsize=16, fontweight='bold', ha='center')

# USB Type-C Section
usb_box = FancyBboxPatch((0.5, 8), 2, 2, boxstyle="round,pad=0.1", 
                          facecolor='lightblue', edgecolor='black', linewidth=2)
ax.add_patch(usb_box)
ax.text(1.5, 9, 'USB Type-C\nPort', ha='center', va='center', fontsize=10)

# CHK224 PD Controller
chk_box = FancyBboxPatch((3, 8), 2, 2, boxstyle="round,pad=0.1", 
                         facecolor='lightgreen', edgecolor='black', linewidth=2)
ax.add_patch(chk_box)
ax.text(4, 9, 'CHK224\nPD Controller', ha='center', va='center', fontsize=10)

# TPS43061 Buck-Boost
tps_box = FancyBboxPatch((6, 8), 2.5, 2, boxstyle="round,pad=0.1", 
                         facecolor='lightyellow', edgecolor='black', linewidth=2)
ax.add_patch(tps_box)
ax.text(7.25, 9, 'TPS43061\nBuck-Boost\n13V Output', ha='center', va='center', fontsize=10)

# BQ24610 Charger Controller
bq_box = FancyBboxPatch((9.5, 7), 3, 4, boxstyle="round,pad=0.1", 
                        facecolor='lightcoral', edgecolor='black', linewidth=2)
ax.add_patch(bq_box)
ax.text(11, 9, 'BQ24610\nCharger\nController', ha='center', va='center', fontsize=12, fontweight='bold')

# MOSFETs
mosfet1 = Rectangle((13, 9), 1, 1, facecolor='lightgray', edgecolor='black')
mosfet2 = Rectangle((13, 7.5), 1, 1, facecolor='lightgray', edgecolor='black')
ax.add_patch(mosfet1)
ax.add_patch(mosfet2)
ax.text(13.5, 9.5, 'Q1', ha='center', va='center', fontsize=9)
ax.text(13.5, 8, 'Q2', ha='center', va='center', fontsize=9)

# Inductor
inductor_x = np.linspace(14.5, 15.5, 100)
inductor_y = 8.5 + 0.2 * np.sin(10 * np.pi * (inductor_x - 14.5))
ax.plot(inductor_x, inductor_y, 'k-', linewidth=2)
ax.text(15, 9.2, 'L1\n10µH', ha='center', fontsize=8)

# Battery Pack
battery_box = FancyBboxPatch((14, 4), 2, 3, boxstyle="round,pad=0.1", 
                             facecolor='lightsteelblue', edgecolor='black', linewidth=2)
ax.add_patch(battery_box)
ax.text(15, 5.5, '3S Battery\nPack\n(3x18650)', ha='center', va='center', fontsize=10)

# BQ34Z100 Gauge
gauge_box = FancyBboxPatch((11, 4), 2, 2, boxstyle="round,pad=0.1", 
                           facecolor='plum', edgecolor='black', linewidth=2)
ax.add_patch(gauge_box)
ax.text(12, 5, 'BQ34Z100-G1\nBattery\nGauge', ha='center', va='center', fontsize=10)

# ESP32
esp_box = FancyBboxPatch((6, 4), 2.5, 2, boxstyle="round,pad=0.1", 
                         facecolor='lightcyan', edgecolor='black', linewidth=2)
ax.add_patch(esp_box)
ax.text(7.25, 5, 'ESP32\nMCU', ha='center', va='center', fontsize=10)

# Connections
# USB to CHK224
ax.arrow(2.5, 9, 0.4, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
ax.text(2.75, 9.2, 'CC1/CC2', fontsize=8)

# CHK224 to TPS43061
ax.arrow(5, 9, 0.9, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
ax.text(5.5, 9.2, 'VBUS', fontsize=8)

# TPS43061 to BQ24610
ax.arrow(8.5, 9, 0.9, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
ax.text(9, 9.2, '13V', fontsize=8)

# BQ24610 to MOSFETs
ax.plot([12.5, 13], [9.5, 9.5], 'k-', linewidth=1)
ax.plot([12.5, 13], [8, 8], 'k-', linewidth=1)

# MOSFETs to Battery
ax.plot([14, 14.5], [9.5, 8.5], 'k-', linewidth=2)
ax.plot([14, 14.5], [8, 8.5], 'k-', linewidth=2)
ax.plot([15.5, 15.5], [8.5, 7], 'k-', linewidth=2)

# I2C connections
ax.plot([7.25, 7.25], [6, 7], 'b--', linewidth=1)
ax.plot([7.25, 11], [7, 7], 'b--', linewidth=1)
ax.plot([11, 11], [7, 6.5], 'b--', linewidth=1)
ax.plot([12, 12], [6, 7], 'b--', linewidth=1)
ax.text(9, 7.2, 'I2C Bus', fontsize=8, color='blue')

# Control signals
ax.plot([7.25, 11], [4, 4], 'g--', linewidth=1)
ax.text(9, 3.8, 'Control Signals', fontsize=8, color='green')

# Power flow indicators
ax.annotate('', xy=(15, 4), xytext=(15, 7),
            arrowprops=dict(arrowstyle='<->', color='red', lw=2))
ax.text(15.3, 5.5, 'Charging', fontsize=8, color='red', rotation=90)

# Component values and notes
notes_text = """Key Components:
• R_SENSE: 10mΩ (1%)
• R_ISET: 68kΩ (1.2A charge)
• R_FB1: 100kΩ
• R_FB2: 20kΩ
• C_BOOT: 0.1µF
• C_OUT: 47µF
• NTC: 10kΩ @ 25°C"""

ax.text(0.5, 2, notes_text, fontsize=9, bbox=dict(boxstyle="round,pad=0.3", 
                                                   facecolor='wheat'))

# Specifications
specs_text = """Specifications:
• Input: USB Type-C (5V/12V PD)
• Battery: 3S Li-ion (12.6V max)
• Charge Current: 1.2A @ 13V, 0.45A @ 5V
• Protection: OVP, OCP, OTP
• Control: ESP32 via I2C
• Monitoring: BQ34Z100-G1"""

ax.text(9, 1.5, specs_text, fontsize=9, bbox=dict(boxstyle="round,pad=0.3", 
                                                   facecolor='lightblue'))

# Add voltage labels
ax.text(1.5, 10.3, '5V/12V', fontsize=8, ha='center')
ax.text(7.25, 10.3, '13V', fontsize=8, ha='center')
ax.text(15, 7.3, '12.6V max', fontsize=8, ha='center')

# Status LEDs
led1 = Circle((3, 6.5), 0.2, facecolor='red', edgecolor='black')
led2 = Circle((3.5, 6.5), 0.2, facecolor='green', edgecolor='black')
ax.add_patch(led1)
ax.add_patch(led2)
ax.text(3.25, 6, 'Status LEDs', fontsize=8, ha='center')

plt.title('USB Type-C PD to 3S Li-ion Battery Charger System Design', pad=20)
plt.tight_layout()
plt.savefig('/workspace/3s_battery_charger_schematic.png', dpi=300, bbox_inches='tight')
plt.show()

# Create detailed BQ24610 connection diagram
fig2, ax2 = plt.subplots(1, 1, figsize=(12, 10))
ax2.set_xlim(0, 12)
ax2.set_ylim(0, 10)
ax2.axis('off')

# BQ24610 IC
ic_box = Rectangle((4, 2), 4, 6, facecolor='lightgray', edgecolor='black', linewidth=2)
ax2.add_patch(ic_box)
ax2.text(6, 8.5, 'BQ24610', fontsize=14, fontweight='bold', ha='center')

# Pin labels and connections
pins_left = [
    ('VCC', '13V Input'),
    ('REGN', '6V LDO'),
    ('BTST', 'Bootstrap'),
    ('PH', 'Phase Node'),
    ('LODRV', 'Low Gate'),
    ('HIDRV', 'High Gate'),
    ('PGND', 'Power GND'),
    ('CE', 'Charge Enable')
]

pins_right = [
    ('SRP', 'Current Sense+'),
    ('SRN', 'Current Sense-'),
    ('FB', 'Voltage FB'),
    ('ISET', 'Current Set'),
    ('TS', 'Temp Sense'),
    ('STAT1', 'Status 1'),
    ('STAT2', 'Status 2'),
    ('AGND', 'Analog GND')
]

# Draw left pins
for i, (pin, desc) in enumerate(pins_left):
    y = 7.5 - i * 0.7
    ax2.plot([3.5, 4], [y, y], 'k-', linewidth=1)
    ax2.text(3.4, y, pin, ha='right', fontsize=9)
    ax2.text(2, y, desc, ha='right', fontsize=8, color='blue')

# Draw right pins
for i, (pin, desc) in enumerate(pins_right):
    y = 7.5 - i * 0.7
    ax2.plot([8, 8.5], [y, y], 'k-', linewidth=1)
    ax2.text(8.6, y, pin, ha='left', fontsize=9)
    ax2.text(10, y, desc, ha='left', fontsize=8, color='blue')

# Add component connections
# MOSFET section
mosfet_box = Rectangle((9, 5.5), 2, 2, facecolor='lightyellow', edgecolor='black')
ax2.add_patch(mosfet_box)
ax2.text(10, 6.5, 'Power\nMOSFETs', ha='center', fontsize=9)

# Sense resistor
ax2.text(10, 4.5, 'R_SENSE\n10mΩ', ha='center', fontsize=8, 
         bbox=dict(boxstyle="round,pad=0.2", facecolor='wheat'))

# Other components
ax2.text(1, 5, 'C_BOOT\n0.1µF', ha='center', fontsize=8,
         bbox=dict(boxstyle="round,pad=0.2", facecolor='lightcyan'))

ax2.text(10, 3.5, 'R_ISET\n68kΩ', ha='center', fontsize=8,
         bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgreen'))

ax2.text(10, 2.5, 'NTC\n10kΩ', ha='center', fontsize=8,
         bbox=dict(boxstyle="round,pad=0.2", facecolor='lightcoral'))

ax2.text(1, 1, 'To ESP32', ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue'))

plt.title('BQ24610 Detailed Pin Connections', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/workspace/bq24610_pinout_diagram.png', dpi=300, bbox_inches='tight')
plt.show()

print("Schematics created successfully!")
print("Files saved:")
print("1. /workspace/3s_battery_charger_schematic.png")
print("2. /workspace/bq24610_pinout_diagram.png")