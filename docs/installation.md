## Installation

```shell
# Enable I2C and Serial
raspi-config
# https://github.com/johnbryanmoore/VL53L0X_rasp_python/issues/13
# Select Interfacing options->I2C choose Yes and hit Enter, then go to Finish and reboot

# https://github.com/codebugtools/codebug_tether/issues/17#issuecomment-414870493
# Select Interfacing options->Serial choose and hit Enter, Select NO for both questions

sudo cp misc/baiiab.service /etc/systemd/system/baiiab.service
sudo systemctl enable baiiab
```

## Operations

```shell
sudo systemctl restart baiiab

# View startup logs
sudo journalctl -u baiiab -f

# View app logs
tail -f ~/baiiab/logs/baiiab.log
```

## Run manually

```shell
sudo systemctl stop baiiab
cd baiiab/
/usr/bin/python /home/pi/baiiab/service.py
```
