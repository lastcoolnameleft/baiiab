import sys
from pathlib import Path

sys.path.append(str(Path(f"{__file__}").parent.parent))
from lcd.i2c_lcd import I2cLcd # Example LCD interface used

DEFAULT_I2C_ADDR = 0x27
lcd = I2cLcd(1, DEFAULT_I2C_ADDR, 4, 20)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("TEST")

