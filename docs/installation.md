## Installation

```
# Enable I2C and Serial
raspi-config
# https://github.com/johnbryanmoore/VL53L0X_rasp_python/issues/13
# Select Interfacing options->I2C choose and hit Enter, then go to Finish and reboot

# https://github.com/codebugtools/codebug_tether/issues/17#issuecomment-414870493
# Select Interfacing options->Serial choose and hit Enter, Select NO for both questions

sudo cp misc/baiiab.service /etc/systemd/system/baiiab.service
sudo systemctl enable baiiab
```

## Operations

```
sudo systemctl restart baiiab

# View logs
sudo journalctl -u baiiab -f
```

## Run manually

```
sudo systemctl stop baiiab
cd baiiab/
/usr/bin/python /home/pi/baiiab/service.py
```