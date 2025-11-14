## Installation

```shell
# Enable I2C and Serial
sudo raspi-config
# https://github.com/johnbryanmoore/VL53L0X_rasp_python/issues/13
# 0W: Select Interfacing options->I2C choose Yes and hit Enter, then go to Finish and reboot
# 02W: Select Interfacing options->I2C choose Yes and hit Enter, then go to Finish and reboot

# https://github.com/codebugtools/codebug_tether/issues/17#issuecomment-414870493
# Select Interfacing options->Serial choose and hit Enter, Select NO for first question, YES for 2nd

# Add to ~/.config/pip/pip.conf (or create it)
mkdir -p ~/.config/pip
echo "[install]" >> ~/.config/pip/pip.conf
echo "user = true" >> ~/.config/pip/pip.conf
echo "[global]" >> ~/.config/pip/pip.conf
echo "extra-index-url = https://www.piwheels.org/simple" >> ~/.config/pip/pip.conf
echo "break-system-packages = true" >> ~/.config/pip/pip.conf


git clone git@github.com:lastcoolnameleft/baiiab.git
cd baiiiab
pip install -r requirements.txt

sudo cp misc/baiiab.service /etc/systemd/system/
sudo cp misc/otel-upload.service /etc/systemd/system/
sudo systemctl enable baiiab
sudo systemctl enable otel-upload.service
```

## OTEL Installation

```shell
sudo cp /home/pi/baiiab/misc/otel-upload.service /etc/systemd/system/
sudo systemctl status otel-upload.service
sudo journalctl -u otel-upload.service -f

```

## Operations

```shell
sudo systemctl restart baiiab

# View startup logs
sudo journalctl -u baiiab -f
sudo journalctl -u otel-upload -f

# View app logs
tail -f ~/baiiab/logs/baiiab.log
```

## Run manually

```shell
sudo systemctl stop baiiab
cd baiiab/
/usr/bin/python /home/pi/baiiab/service.py
# OTEL
/usr/bin/python3 /home/pi/baiiab/helpers/otel_upload_service.py
```

## Debugging

```shell
sudo i2cdetect -y 1 # Should see LDC at 0x27
```
