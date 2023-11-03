# Bad AI In A Box

This repository contains the details for the inspiration, build, and design of Bad AI In A Box.

CLICK to watch the video!

[<img src="https://i.ytimg.com/vi/_tY3fxE0qaY/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=_tY3fxE0qaY "Bad AI In A Box")

## Background

With the proliferation of AI in all things, I wanted to find a way to explore this new technology myself while also making something fun and quasi-useful.

NOTE: Even though the title is "Bad AI", I don't think that the AI is inherently evil, or even of low quality.  In fact, quite the opposite!  The main reason for calling it so is because the main scenario is to create an AI that gives out "bad advice".  So, it's more of a naughty AI.  BAIIAB is also an acronym which makes me happy.

## Technologies used

- [Azure Open AI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview) - This is used to generate the responses
- [Adafruit Thermal Printer](https://www.adafruit.com/product/597) - This creates the receipts for the response.  It's fun to have something which I can give out to other people
- [Prusa i3 MK3](https://www.prusa3d.com/category/original-prusa-i3-mk3s/) - My 3d printer which I used to create the box
- [Raspberry Pi 0w](https://www.raspberrypi.com/products/raspberry-pi-zero-w/) - The "brains" of the box.  It is the controller which runs all of the code
- [20x4 LCD display module](https://amzn.to/3Qn3L1B) - Human readable display
- [Rotary encoder](https://amzn.to/3QKMn8G) - Used to interface with the RPi

## FAQ

- Q: How does this use OpenAI?
  - Using the [configuration file](https://github.com/lastcoolnameleft/baiiab/blob/main/conf/menu.json), BAIIAB will convert the user's input to a [prompt](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api) which it will then send to Azure OpenAI Service and then send the response to the thermal printer
- Q: That's so cool!  How can I build one myself?
  - A: I haven't documented the full process yet, but message me and I can share details with you.