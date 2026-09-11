Mashup

Problem Statement
Most people who kill houseplants or fail at windowsill crop-growing lack insight into how their friendly flora are doing. Generic care instructions (e.g. “water weekly”) ignore the plant’s actual environment, so by the time visible signs of stress appear, the window to act has usually passed. For crops specifically, this isn’t just a wilted decoration, it’s a wasted harvest, and inconsistent light and/or watering is the most common reason home crop-growing attempts fail.

Existing “smart pot” products solve the sensing issue but mostly stop at generic mood-based notifications rather than grounded, human-like, two-way interaction tied to a concrete outcome (a successful harvest).

Concept
A smart plant pot that:
1. Continuously senses soil moisture and light level
2. Gives the plant a conversational “voice” via an LLM, grounded in real sensor data rather than generic scripted messages
3. Supports two-way interaction, i.e. a person can ask the pot a direct question (“How are you doing?”) and get an answer reflecting its actual current state

Scope

In Scope:
- Soil moisture and light sensing, polled on a timer
- Text-based Q&A as the core interaction loop
- Voice I/O as a layer on top of the text pipeline
- Response prompt with a personality tuned to reference real sensor data

Out of Scope:
- Companion mobile app (a local display or laptop screen is sufficient)
- Multi-plant/multi-pot support
- Long-term historical data logging or trend graphs
- Automated watering
- Cloud account/authentication system

Goals & Success Criteria
- Judges can ask the pot an open question live and receive a coherent, sensor-driven answer in a few seconds
- The outcome framing comes across as a differentiator (not just another talking plant gadget)
- Conversation is robust enough to handle an unscripted question, not just rehearsed ones

Hardware

- https://thepihut.com/products/raspberry-pi-5?variant=42531604955331 (Raspberry Pi 5)
- https://thepihut.com/products/noobs-preinstalled-sd-card?variant=20649315598398 (MicroSD card with OS installed)
- https://thepihut.com/products/capacitive-soil-moisture-sensor?variant=32137736421438 (Capacitive Soil Moisture sensor)
- https://thepihut.com/products/adafruit-mcp3008-8-channel-10-bit-adc-with-spi-interface (Analogue-digital converter)
- https://thepihut.com/products/gravity-i2c-ip68-waterproof-ambient-light-sensor-1-65535lx?variant=42448630612163 (Waterproof light sensor)
- https://thepihut.com/products/mini-external-usb-stereo-speaker?variant=31955934801 (USB speaker)
- https://thepihut.com/products/mini-usb-microphone?variant=31955934225 (USB microphone)

Extension
Extend to window-sill crop pots: Integrate an AI camera and LCD screen with a “Days to Harvest: x” estimate. The “harvest” framing becomes the differentiator compared to generic smart pots.


- User speaks to Laptop (SPA)
- STT on Laptop (Can be done on SPA)

- Collect sensor data via Pi (Python)
- Pi sends user question + sensor data to LLM (Python)
- LLM responds (Python)
- Pi outputs via Audio (Python)
