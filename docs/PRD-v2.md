# Product Requirements Document

**Project:** Smart Plant Pot ("Talking Plant")
**Version:** 2.0
**Date:** 2026-09-09
**Supersedes:** PRD.md v1.0 (2026-09-08)
**Status:** Draft — ready for build

---

## 0. What changed from v1.0, and why

v1.0 was pressure-tested against the real hardware datasheets and the Raspberry Pi 3 Model A+
specification. Eleven problems were found, of which four were outright blockers — the build as
specified in v1.0 could not have been assembled. This version corrects them.

| # | Problem in v1.0 | Resolution in v2.0 |
| --- | --- | --- |
| 1 | Appendix A stated both I2C sensors connect to physical pins 1/3/5/6. Pins 3 (SDA) and 5 (SCL) are each a **single** male header pin, and both sensor cables terminate in female sockets. Two female sockets cannot share one pin. | Section 9 rewires it. Power and ground go straight to the header on separate pins; only SDA and SCL are split across a breadboard. |
| 2 | No mention of I2C clock stretching. The Adafruit seesaw chip stretches the clock; the Pi's BCM2835 I2C peripheral handles that incorrectly, producing intermittent garbage readings and `OSError: [Errno 121]`. | NFR-08 makes the baudrate change mandatory and testable. |
| 3 | NFR-02 and Appendix A both offered "direct Ethernet" for the Pi-to-laptop link. **The Pi 3 Model A+ has no Ethernet port.** A USB-Ethernet adapter would occupy the only USB-A port, which the microphone needs. | NFR-02 rewritten around the office network with a hotspot fallback. |
| 4 | FR-02's keyboard fallback assumed a keyboard could be attached. The single USB-A port is taken by the microphone, and hold-to-record cannot be implemented over SSH because a terminal transmits key-press but not key-release events. | FR-02 rewritten: the fallback key is pressed on the MacBook, which sends start/stop to the Pi. |
| 5 | NFR-02 (isolate from venue WiFi) contradicted Section 6 (the Anthropic call needs real internet). | Resolved: the Pi requires both LAN and WAN on the same network. NFR-02 now states this and requires it be proven on day 1. |
| 6 | FR-05 proposed Piper TTS as a stretch goal on the Pi. Piper's tested baseline is a Pi 4 with 2 GB+; on 512 MB it is marginal at best and likely slower than real time. | FR-05 moves the Piper stretch goal to the MacBook. Baseline TTS changes from `pyttsx3` to `espeak-ng` called directly. |
| 7 | FR-03 specified an "ideal soil moisture range (min/max)" with no units. The seesaw sensor returns raw capacitive counts, not a percentage. | FR-03 now specifies raw counts and requires in-pot calibration (FR-07). |
| 8 | FR-04's repeat/cooldown behaviour was deferred to the dev team, making the acceptance criterion untestable. | FR-04 now specifies edge-triggered alerting with re-arm on return to range. |
| 9 | No monitor, HDMI cable, USB keyboard, USB hub, breadboard, or jumper wires appeared in the parts list. | Section 9 lists what is needed. A headless setup removes the keyboard and hub requirement entirely. |
| 10 | Room noise was unaddressed, despite the success criterion depending on Whisper correctly hearing a judge in a hackathon hall. | NFR-07 adds a microphone-placement and presenter-briefing requirement, and the STT model is upgraded. |
| 11 | The Pi-to-laptop transfer mechanism was undefined. | Section 8 specifies it. |

---

## 1. Overview

### 1.1 Purpose

The Smart Plant Pot gives a houseplant a "voice." Soil moisture, soil temperature, and light
readings are combined with an LLM (Anthropic Claude) so the pot can be asked questions aloud and
respond in character through a speaker, as if the plant itself were speaking about its own
condition and needs. The pot also speaks up unprompted when a sensor reading falls outside its
configured safe range.

### 1.2 Success Criteria

Unchanged from v1.0. Success is a working live demo in which:

- A judge or presenter holds a physical button, asks the plant a question aloud, releases the
  button, and the plant responds audibly with a relevant, in-character answer reflecting its
  actual current sensor readings.
- The plant can be shown proactively speaking up when a reading is pushed outside its safe range.

This is a demo-first build. There is no post-hackathon production, maintenance, or user base
requirement.

### 1.3 Background

Greenfield build. Two-day development window, four developers, all beginners with Raspberry Pi
hardware. No existing system or prior art. All hardware in Appendix A has been procured and has
arrived. The team additionally has a monitor, an HDMI cable, a used breadboard, and jumper wires.

Development and the demo both take place in the team's company office. This is a significant
de-risking factor: the network can be validated on day 1 in the same room the demo runs in.

---

## 2. Users

Unchanged from v1.0.

| User type | Description | Primary goal | Key frustration today |
| --- | --- | --- | --- |
| Demo presenter | One of the 4 team members operating the pot live at the demo table | Trigger a smooth, reliable voice interaction in front of judges | No existing way to know a plant's own "state" or needs |
| Judge / demo audience | Hackathon judges and onlookers watching the live demo | Be entertained and understand the concept quickly | N/A — first exposure to the concept |

**The Presenter** is a member of the build team, comfortable with the concept but not necessarily
the one who wired the hardware. They hold a button, ask a question in a normal speaking voice, and
let go. The interaction must be fast, forgiving, and have a tested fallback.

**The Judge** has never seen the system and will watch one or two interactions at most. The concept
must be obvious within seconds, with no explanation of sensors, APIs, or architecture required.

---

## 3. Scope

### 3.1 In Scope

- Physical push button on GPIO17 for push-to-talk: hold to record, release to send.
- MacBook-key fallback trigger (Plan B) with identical hold-to-record behaviour, routed to the Pi
  over the local network.
- Local speech-to-text on the MacBook using `whisper.cpp` with the `base.en` model.
- A configurable plant context file (moisture range in raw sensor counts, lux range, plant name,
  species, personality) included in every LLM request.
- LLM request/response via the Anthropic Python SDK, called **from the Pi**. Single request, no
  tool use, no web search, plain text response, capped at approximately two sentences.
- Text-to-speech on the Pi via `espeak-ng`, played through the USB speakers via the 3.5 mm AV jack.
- Periodic background polling of soil moisture and light on a fixed interval.
- Proactive unprompted speech when a reading leaves its safe range, edge-triggered.
- A single busy lock so the proactive check and the button-triggered flow cannot overlap.
- Sensor calibration procedure performed in the actual pot with the actual soil (FR-07).

### 3.2 Out of Scope

Unchanged from v1.0, plus two additions:

- Any production hosting, user accounts, authentication, or multi-pot support.
- Mobile app, web dashboard, or any UI beyond the pot, its speaker, mic, and button.
- Wake-word or continuous voice-activated listening.
- Cloud or paid TTS and cloud or paid STT. Both explicitly rejected.
- Cloning or imitating the voice or likeness of any named real person.
- Long-term data logging, historical trend analysis, or notifications outside the live interaction.
- Support for crop-specific pots, multiple simultaneous plants, or hardware beyond Appendix A.
- **New:** running Whisper on the Raspberry Pi. Ruled out on measured grounds — see Section 7.1.
- **New:** running Piper TTS on the Raspberry Pi. Ruled out — see FR-05.

---

## 4. Features & Acceptance Criteria

### 4.1 Push-to-Talk Voice Question (Core Loop)

**Description:** The presenter holds the physical button, speaks a question, and releases to send.
The Pi records, ships the audio to the MacBook for transcription, receives text back, sends that
text plus the plant context and live sensor readings to the Anthropic API, and speaks the response
through the speaker.

**Requirement ref:** FR-01 · **Priority:** Must Have

**Acceptance Criteria:**

- [ ] Holding the button starts recording via the USB microphone; recording stops the moment the
      button is released.
- [ ] Audio is captured as 16 kHz mono 16-bit WAV. (Whisper resamples to 16 kHz internally;
      recording at that rate directly avoids a conversion step and keeps files small.)
- [ ] The WAV is POSTed to the transcription service on the MacBook and text is returned
      (see FR-06 and Section 8).
- [ ] The transcribed question, the full plant context (FR-03), and the sensor readings taken at
      the moment of the request are combined into a single Anthropic API request.
- [ ] The response is converted to speech and played audibly within 10 seconds of button release.
      Design target is 4 seconds (see NFR-01).
- [ ] The spoken response reflects the plant's actual current readings and configured personality,
      not a generic canned answer.
- [ ] If no speech is captured, or Whisper returns an empty or whitespace-only string, the system
      does not crash and speaks a short fixed "I didn't catch that" line **without** calling the
      Anthropic API.
- [ ] Every external call (transcription POST, Anthropic call) has an explicit timeout and a
      spoken failure line, so a network problem produces audible feedback rather than silence.

**Usability Criteria:**

- [ ] A presenter told only "hold the button, ask a question, let go" succeeds on their first
      attempt.
- [ ] The delay between release and the plant beginning to speak is short enough that a judge does
      not think the system has frozen.

---

### 4.2 MacBook Key Fallback Trigger (Plan B)

**Description:** If the physical button proves unreliable, a key held on the MacBook provides the
same hold-to-record, release-to-send trigger. The key is captured on the MacBook — **not** over
SSH — and sent to the Pi as explicit start and stop messages.

**Requirement ref:** FR-02 · **Priority:** Must Have

**Rationale for the change from v1.0:** v1.0 assumed a keyboard attached to the Pi. The Pi 3A+ has
one USB-A port and the microphone occupies it. The obvious workaround — pressing a key in an SSH
session — does not work: a terminal transmits key-press events but not key-release events, so
"release to send" cannot be detected. Capturing the key locally on the MacBook (where both press
and release are available) and sending two messages to the Pi solves this with no extra hardware.

**Acceptance Criteria:**

- [ ] A designated key held on the MacBook starts recording on the Pi; releasing it stops recording
      and sends.
- [ ] Both the GPIO button and the MacBook key call the same underlying recording function on the
      Pi. Switching between them requires no code changes.
- [ ] The Pi exposes a small local HTTP endpoint that accepts start and stop messages
      (see Section 8).
- [ ] The fallback is tested and confirmed working before the demo, not built and assumed
      functional.

---

### 4.3 Plant Context Configuration

**Description:** A configurable, structured set of information about the specific plant, included
in every LLM request so responses are grounded in its real identity and thresholds.

**Requirement ref:** FR-03 · **Priority:** Must Have

**Acceptance Criteria:**

- [ ] Stored in a single JSON file that a non-developer team member can edit on demo day without
      touching pipeline code.
- [ ] Contains at minimum: plant name, species, ideal soil moisture range as **raw seesaw
      capacitive counts** (min/max integers), ideal light range in **lux** (min/max), and a
      personality description.
- [ ] Every LLM request — button-triggered and proactive — includes the full context alongside the
      live readings at request time.
- [ ] No web search or external lookup is performed by the LLM. All plant-specific knowledge is
      supplied in the request.
- [ ] Editing the file and restarting the service changes the plant's behaviour with no code edits.

**Units note (new in v2.0):** v1.0 said "ideal soil moisture range (min/max)" without units. The
Adafruit seesaw sensor returns a raw capacitive count, roughly 200 in open air and roughly 2000
fully submerged, varying by soil type and by individual sensor. It is **not** a percentage. Values
must come from the calibration in FR-07, not from a datasheet or a guess.

Reference shape:

```json
{
  "name": "Kevin",
  "species": "Monstera deliciosa",
  "moisture_counts": { "min": 900, "max": 1600 },
  "light_lux": { "min": 200, "max": 10000 },
  "personality": "An energetic Australian wildlife-presenter tone. Dramatic, warm, a bit theatrical. Never breaks character.",
  "poll_interval_seconds": 300,
  "llm_model": "claude-opus-5",
  "max_tokens": 150
}
```

---

### 4.4 Proactive Threshold Alert (Unprompted Speech)

**Description:** The system periodically checks moisture and light against the safe ranges. When a
reading leaves its range, the plant speaks up in character without being asked.

**Requirement ref:** FR-04 · **Priority:** Should Have

**Acceptance Criteria:**

- [ ] Both sensors are polled on a fixed interval, configurable in the plant context file.
      Default 300 seconds.
- [ ] When a reading moves from inside its range to outside, an LLM request is triggered
      automatically including the context and the out-of-range reading, and the response is spoken.
- [ ] **Edge-triggered, not level-triggered.** Each sensor holds an `alerted` boolean. The alert
      fires only on the transition into breach; the flag is set when it fires and cleared only when
      that sensor's reading returns to inside its range. A sensor that stays out of range does not
      speak again.
- [ ] If a periodic check occurs while any response is being generated or played, the check is
      skipped entirely rather than queued or interleaved.
- [ ] Demonstrable on demand: covering the light sensor triggers an alert, uncovering it re-arms,
      covering it again triggers a fresh alert.

**Rationale for the change from v1.0:** v1.0 left cooldown behaviour "to be decided by the dev team
during build," which is not a testable acceptance criterion. Edge-triggering is simple to implement,
cannot produce a nagging loop, and demos cleanly — the judge can trigger it themselves by putting a
hand over the light sensor.

---

### 4.5 Local Text-to-Speech Output

**Description:** The LLM's text response is spoken through the USB speakers using free, offline
tooling on the Pi.

**Requirement ref:** FR-05 · **Priority:** Must Have

**Acceptance Criteria:**

- [ ] Baseline uses `espeak-ng` invoked directly on the Pi. Zero API keys, negligible CPU and RAM,
      synthesis is effectively instantaneous.
- [ ] Audio plays through the USB-powered speakers via the Pi's 3.5 mm AV jack, powered from a
      separate charger (Section 9).
- [ ] Audio output routing is verified with `speaker-test -t wav -c 2` before any application code
      is written.
- [ ] **Stretch goal (Could Have):** if time remains after all Must Have and Should Have items
      work, run **Piper TTS on the MacBook** at medium voice quality and stream the resulting WAV
      back to the Pi, which plays it with `aplay`. Adds no internet dependency.

**Two changes from v1.0:**

*`pyttsx3` dropped.* On Linux `pyttsx3` is a wrapper that shells out to espeak. It produces the
identical voice while adding a dependency and a known `runAndWait()` blocking quirk on the Pi.
Calling `espeak-ng` directly is simpler and more predictable.

*Piper moved off the Pi.* Piper's tested baseline is a Pi 4 with 2 GB or more of RAM. On a Pi 3A+
with 512 MB, onnxruntime plus a voice model is tight, and synthesis on the quad A53 is likely
slower than real time — a two-sentence reply could take 5–10 seconds to generate, which would
consume the entire latency budget for a cosmetic gain. The M1 runs the same model near-instantly.

---

### 4.6 Local Speech-to-Text Transcription

**Description:** Recorded audio is transcribed on the MacBook using a local Whisper model. This is
the only part of the pipeline that does not run on the Pi.

**Requirement ref:** FR-06 · **Priority:** Must Have

**Acceptance Criteria:**

- [ ] The MacBook runs `whisper.cpp` with the **`base.en`** model and Metal acceleration.
- [ ] It exposes a local HTTP endpoint accepting a WAV upload and returning JSON containing the
      transcribed text (Section 8).
- [ ] The Pi POSTs its recording there and uses the returned text in the LLM request.
- [ ] The Pi-to-MacBook link is validated in the office on day 1 (NFR-02).
- [ ] Measured: transcription of a 5-second clip completes in under 1 second.

**Model choice rationale (new in v2.0):** `tiny.en` (~75 MB) transcribes in roughly 0.2 s but is
noticeably weaker in background noise and on proper nouns — including the plant's own name, which
it will be asked about repeatedly. `base.en` (~142 MB) takes roughly 0.5 s on M1 with Metal. The
0.3 s cost is negligible against the 10 s budget and buys materially better accuracy in the one
condition that matters. `small.en` remains available as an upgrade if rehearsal shows it is needed.

---

### 4.7 Sensor Calibration (New in v2.0)

**Description:** The moisture thresholds in the plant context must be derived from measurements
taken with the actual sensor in the actual pot, before they mean anything.

**Requirement ref:** FR-07 · **Priority:** Must Have

**Acceptance Criteria:**

- [ ] A short script prints live moisture counts and lux at 1-second intervals.
- [ ] Three moisture readings are recorded and written into the plant context file: sensor in open
      air (dry reference), sensor in the pot's soil when dry, sensor in the pot's soil shortly
      after watering.
- [ ] Light thresholds are recorded under the actual demo-table lighting, and with a hand covering
      the sensor, so the "too dark" threshold is known to be reachable on demand.
- [ ] Thresholds are chosen such that both alert conditions can be triggered live during the demo
      by a physical action a judge can perform (covering the light sensor; lifting the probe out of
      the soil).

**Why this is a Must Have:** FR-04 is unfalsifiable without it. Uncalibrated thresholds either
never fire or fire constantly, and either way the second success criterion cannot be demonstrated.

---

## 5. Non-Functional Requirements

| ID | Category | Requirement | Acceptance criterion |
| --- | --- | --- | --- |
| NFR-01 | Performance | End-to-end time from button release to audible response start. Target 4 s, hard ceiling 10 s. | A timed test run in the office before the demo. Budget: ~0.1 s upload + ~0.5 s Whisper `base.en` + ~1.5–3 s Anthropic + ~0.1 s espeak. If over 10 s, reduce `max_tokens` first, then A/B the model (NFR-09). |
| NFR-02 | Network | The Pi requires **both** a route to the MacBook **and** internet access for the Anthropic call, on the same network. | Plan A is the office WiFi. Plan B is an iPhone hotspot both devices join. Both proven in the office on day 1, not on demo day. See the day-1 network gate below. |
| NFR-03 | Cost | All AI/ML processing other than the LLM must be free. | STT is local `whisper.cpp`. TTS is local `espeak-ng` (and optionally Piper). Only the Anthropic call is paid. |
| NFR-04 | Reliability | The core loop must have a working, tested fallback trigger. | FR-02 built and demonstrated working before the demo. |
| NFR-05 | Legal/Ethical | No cloning or imitation of a specific named real person's voice or likeness. | Personality achieved through accent and character prompting only. |
| NFR-06 | Concurrency | The proactive flow and the button-triggered flow must never overlap. | A single lock guards response generation and playback. The periodic check acquires it non-blockingly and skips if unavailable. |
| NFR-07 | Audio capture | Transcription must be robust to hackathon-hall background noise. | Microphone mounted at the pot's rim. Presenter briefed to speak from roughly 15 cm. Verified by a transcription test with the office at normal noise levels. |
| NFR-08 | Hardware I2C | The Pi's I2C bus must be slowed to tolerate the seesaw sensor's clock stretching. | `dtparam=i2c_arm=on,i2c_arm_baudrate=10000` present in `/boot/firmware/config.txt`. Verified by `i2cdetect -y 1` showing both `0x23` and `0x36`, and by 100 consecutive moisture reads with no `OSError`. |
| NFR-09 | LLM latency | Model choice is a config value, not a code change. | `llm_model` lives in the plant context file. Built against `claude-opus-5` at `effort: low`; A/B tested against `claude-haiku-4-5` at rehearsal by editing one string. |
| NFR-10 | Secrets | The Anthropic API key must not be hardcoded or committed. | Key supplied to the Pi via the `ANTHROPIC_API_KEY` environment variable. The SDK reads it automatically from a zero-argument client. |

### Day-1 network gate (NFR-02)

Two checks, both in the **first hour** of day 1. They gate everything else and both have known
failure modes that look like unrelated bugs later.

1. **Pi-to-Mac reachability.** From the MacBook, `ping raspberrypi.local`. If this fails, the office
   network uses client isolation and you are on Plan B (hotspot) for the rest of the project.
2. **Pi-to-internet reachability.** From the Pi over SSH, confirm it can reach the Anthropic API.
   Corporate networks frequently use a captive portal or device registration. **A headless Pi
   cannot complete a browser-based login.** If the Pi cannot reach the internet, you are on Plan B.

If either check fails, switch to the hotspot immediately and re-run both. Do not defer this. A
failure discovered on day 2 presents as "the LLM is broken" and costs hours.

---

## 6. Constraints

- **Timeline:** 2 days. The Must/Should/Could prioritisation reflects this hard constraint and
  should not be revisited without deprioritising something else.
- **Team:** 4 developers, all beginners with Raspberry Pi hardware. Pre-built libraries are
  preferred over custom implementation throughout.
- **Hardware:** Raspberry Pi 3 Model A+ — 512 MB RAM, **one USB-A port, no Ethernet port**. The USB
  port is permanently occupied by the microphone. Speakers are powered separately and connected via
  the 3.5 mm jack.
- **No paid AI services except the LLM.**
- **No literal celebrity voice cloning.**
- **The Pi needs genuine internet access**, because the Anthropic call is made from the Pi. Any
  network plan that isolates the Pi from the internet breaks the build.

---

## 7. Data & Integrations

**Key data entities:**

- **Plant context** — name, species, moisture range in raw counts, lux range, personality, poll
  interval, model id, token cap. Single JSON file.
- **Sensor readings** — soil moisture (raw counts), soil temperature (°C), ambient light (lux).
  Read live, used transiently. No historical storage.
- **Transcript/response pairs** — transient. Not persisted.

**External integrations:**

- **Anthropic API (Claude)** — called from the Pi with the official `anthropic` Python SDK. Requires
  internet and an API key supplied via environment variable.
- **`whisper.cpp`** — runs on the MacBook. Not a hosted API.
- **`espeak-ng`** — runs on the Pi. Not a hosted API.

**Data sensitivity:** None. No personal data, no accounts, no PII. Audio recordings are transient.

### 7.1 Why Whisper cannot run on the Pi

Recorded because it was asked during review and the reasoning is not obvious.

The 32 GB microSD card is the Pi's mandatory boot disk and only storage — the Pi does not boot
without it. It is **not** a substitute for RAM. Whisper needs its model and working buffers
resident in RAM, and the Pi has 512 MB regardless of card size. Configuring the SD card as swap
would technically allow a larger model to load, but SD random I/O is orders of magnitude slower
than RAM; transcription would become unusable, and the sustained writes risk corrupting the card
mid-demo.

Speed is the binding constraint even where RAM is not. `tiny.en` fits in 512 MB but takes roughly
15–30 seconds to transcribe 5 seconds of speech on the Pi's quad Cortex-A53. The same clip takes
roughly 0.5 seconds on the M1 with `base.en` — a gap of roughly 30–50× — and `base.en` is the more
accurate model. Transcription is therefore the one component that must live on the MacBook.

---

## 8. Interfaces Between Pi and MacBook (New in v2.0)

v1.0 did not specify how audio and text move between machines. Both directions are plain HTTP over
the local network, which keeps the whole thing debuggable with `curl`.

**MacBook — transcription service**

- `POST /transcribe` — body is a `multipart/form-data` WAV upload (16 kHz, mono, 16-bit).
- Returns `{"text": "..."}`. Returns `{"text": ""}` for silence; the Pi treats empty as
  "didn't catch that" (FR-01) and does not call the LLM.
- Called by the Pi after every recording.

**Pi — trigger service (Plan B only)**

- `POST /trigger` with `{"action": "start"}` and `{"action": "stop"}`.
- Called by a small script on the MacBook that captures key-down and key-up locally.
- Calls the same recording function as the GPIO button (FR-02).

Both services are minimal Flask apps. The Pi addresses the MacBook by IP, configured in one place.

---

## 9. Hardware Assembly (Replaces v1.0 Appendix A build notes)

### 9.1 Wiring

The v1.0 plan cannot be assembled. The corrected plan below avoids the problem by observing that
the Pi exposes 3V3 on **two** pins and GND on **eight**, so only SDA and SCL actually need
splitting.

Direct to the header, no breadboard:

| Wire | Function | Pi physical pin |
| --- | --- | --- |
| Soil sensor VIN | 3V3 | **1** |
| Soil sensor GND | GND | **6** |
| Light sensor VIN | 3V3 | **17** |
| Light sensor GND | GND | **9** |
| Button leg A | GPIO17 | **11** |
| Button leg B | GND | **14** |

Via the breadboard, one row each:

| Breadboard row | Contains |
| --- | --- |
| Row 1 (SDA) | Jumper from Pi pin **3** · soil sensor SDA · light sensor SDA |
| Row 2 (SCL) | Jumper from Pi pin **5** · soil sensor SCL · light sensor SCL |

Six male-to-male jumpers total. The sensor cables terminate in female DuPont sockets, so each one
pushes onto the exposed male end of a jumper standing in the breadboard row.

**Before applying power, verify:** soil VIN is on pin 1 and light VIN is on pin 17. Pins 2 and 4
sit immediately alongside and carry **5 V**. The Pi's GPIO is not 5 V tolerant, and 5 V on an I2C
line can permanently damage the board. Count the pins twice.

I2C addresses do not conflict: seesaw soil sensor `0x36`, BH1750 `0x23`.

Any breadboard works — it is a passive grid of spring contacts with no model-specific behaviour.
A previously used one is fine.

### 9.2 Software configuration, in order

1. **Flash the SD card** with Raspberry Pi Imager on the MacBook. Use the gear icon to preconfigure
   hostname, username, password, WiFi credentials, and **enable SSH**. This removes the need for a
   keyboard attached to the Pi entirely, which is what keeps the single USB-A port permanently
   available for the microphone. Raspberry Pi OS **Lite (64-bit)** is recommended — the desktop
   environment consumes roughly 200 MB of the 512 MB available.
2. **First boot with the monitor attached** so boot messages and the IP address are visible if
   anything goes wrong. After that, work over SSH from the MacBook.
3. **Enable and slow I2C.** Add to `/boot/firmware/config.txt` (on Raspberry Pi OS Bookworm and
   later; on older releases this file is at `/boot/config.txt`):

   ```
   dtparam=i2c_arm=on,i2c_arm_baudrate=10000
   ```

   Reboot. Confirm with `sudo i2cdetect -y 1` — both `23` and `36` must appear in the grid. If
   readings are still unstable, lower the baudrate to `5000`.
4. **Verify audio in and out** before writing any application code. `arecord -l` lists the USB
   microphone; `speaker-test -t wav -c 2` confirms output through the 3.5 mm jack. Configure the
   ALSA default devices if needed — the microphone and the headphone jack are separate cards. On
   older Raspberry Pi OS releases, output routing may need forcing to the headphone jack with
   `amixer cset numid=3 1`.
5. **Install dependencies:** `espeak-ng`, `python3-flask`, `adafruit-circuitpython-seesaw`,
   `adafruit-circuitpython-bh1750`, `anthropic`. `gpiozero` ships with Raspberry Pi OS.

### 9.3 Physical placement

- Only the ribbed probe end of the soil sensor goes into the soil. The end carrying the connector
  must stay dry.
- The microphone mounts at the pot's rim, pointing up and outward toward where the presenter stands
  (NFR-07).
- Speakers are powered from a separate phone charger, with their 3.5 mm plug in the Pi's AV jack.

### 9.4 Parts

Original list, all arrived:

| Item | Price |
| --- | --- |
| Raspberry Pi 3 Model A+ | £24.00 |
| Official 12.5 W micro-USB PSU | £7.70 |
| microSD card 32 GB | owned |
| Adafruit STEMMA Soil Sensor (ADA4026) | £7.20 |
| Adafruit BH1750 Light Sensor | £4.40 |
| JST PH 4-pin to female socket cable, 200 mm | £1.30 |
| STEMMA QT JST-SH 4-pin to female sockets, 150 mm | £1.00 |
| Mini USB microphone | £5.20 |
| USB powered speakers | £8.70 |
| Momentary push button + jumper wires | ~£1.00 |

Also required, and confirmed available: monitor, HDMI cable, breadboard, male-to-male jumper wires.

**No longer required** (removed by the headless setup decision): USB keyboard, USB hub,
USB-Ethernet adapter.

---

## 10. Team Workstreams

Four parallel streams. Streams 3 and 4 need no hardware at all and can begin immediately.

| Stream | Owner | Work | Hardware needed |
| --- | --- | --- | --- |
| 1 | Dev A | Flash and boot the Pi, run the day-1 network gate, wire the sensors and button, verify I2C, run FR-07 calibration | Yes — starts immediately |
| 2 | Dev B | Audio record and playback on the Pi, GPIO button handling, the busy lock, main orchestration loop | Yes — **blocked until stream 1 completes Pi setup** |
| 3 | Dev C | `whisper.cpp` setup on the MacBook, the `/transcribe` Flask service, the Plan B key-capture script | No — testable against a pre-recorded WAV |
| 4 | Dev D | Plant context schema and file, prompt design, personality, the Anthropic call, response shaping | No — testable as a standalone Python function |

**Open risk:** stream 2 sits behind stream 1's Pi setup. A mock sensor and mock audio layer was
considered and not adopted; without it, Dev B has no work until the Pi is reachable over SSH.
Suggested mitigation, at the team's discretion: Dev B pairs with Dev A on the wiring (which also
removes the single-point-of-knowledge risk on the hardware), or writes the orchestration loop
against stub functions that return fixed values.

**Open risk:** no hard integration deadline has been set. In a two-day build, the point at which
everything must run end-to-end — with the remainder reserved for rehearsal — is normally fixed in
advance so that unfinished work gets cut rather than rushed. Currently undefined.

---

## 11. Demo Rehearsal Checklist

Section 8 of v1.0 correctly flagged that latency and alert timing must be rehearsed rather than
only implemented. Concretely:

- [ ] Time ten full button-press cycles. Record the slowest. It must be under 10 seconds.
- [ ] Run a transcription test with the office at normal noise levels, not in silence.
- [ ] Trigger the light alert by hand three times, confirming re-arm works between each (FR-04).
- [ ] Demonstrate the Plan B MacBook key end to end, on the demo network.
- [ ] Unplug and replug everything once, then confirm the system still comes up — this is the state
      it will be in when you arrive at the demo table.
- [ ] Confirm the plant context file can be edited and the change takes effect, by someone who did
      not write the code.
- [ ] A/B `claude-opus-5` against `claude-haiku-4-5` on live latency and response quality (NFR-09).

---

## 12. Sign-off

| Role | Name | Status | Date |
| --- | --- | --- | --- |
| Stakeholder | greenthumb / Tyleezy | Pending | |
| Requirements (v1.0) | Requirements Elicitation Skill | Prepared | 2026-09-08 |
| Requirements (v2.0) | Forge Idea review | Prepared | 2026-09-09 |

---

## Appendix B — Build Runbook

A step-by-step path from boxed parts to a working pot. Written for a team with no prior Raspberry
Pi experience. Follow it in order — several steps exist specifically to catch a failure before it
becomes hard to diagnose.

Anything marked **GATE** must pass before moving on. A gate that fails costs minutes now and hours
later.

### B.1 Day 1, first hour — the network gate

Do this before touching a single wire. Everything else depends on it, and both failure modes
disguise themselves as unrelated bugs later.

```bash
# On the MacBook — can it see the Pi at all?
ping -c 3 raspberrypi.local
```

If that fails after the Pi is up (step B.3), the office network uses client isolation. Switch to
the iPhone hotspot, join both devices, and re-run.

```bash
# On the Pi, over SSH — can it reach the Anthropic API?
curl -s -o /dev/null -w "%{http_code}\n" https://api.anthropic.com/v1/messages
```

Any HTTP code (`401`, `404`, `405`) means the Pi has internet — you are seeing the API reject an
unauthenticated request, which is exactly right. A hang, a timeout, or `000` means it does not.
Corporate networks commonly use a captive portal or device registration, and **a headless Pi cannot
complete a browser login.** If this fails, you are on the hotspot.

**GATE:** both commands must succeed on the same network before proceeding.

### B.2 Flash the SD card

On the MacBook. Download Raspberry Pi Imager from raspberrypi.com.

1. **Choose Device** → Raspberry Pi 3.
2. **Choose OS** → Raspberry Pi OS (other) → **Raspberry Pi OS Lite (64-bit)**. Lite, not Desktop —
   the desktop environment eats roughly 200 MB of your 512 MB.
3. **Choose Storage** → your 32 GB card.
4. **Next** → **Edit Settings**. This screen is the one that saves you a keyboard, so do not skip it:
   - Set hostname to `raspberrypi`
   - Set username and password (write them down)
   - Configure wireless LAN — SSID, password, and country code
   - Set the locale
   - On the **Services** tab, tick **Enable SSH** → *Use password authentication*
5. Write, then eject.

> **Why this matters:** with SSH and WiFi preconfigured, you never attach a keyboard to the Pi.
> That is what keeps the single USB-A port permanently free for the microphone. If you skip this
> screen you will need a USB keyboard, and then you cannot plug in the mic.

### B.3 First boot

Put the card in the slot on the **underside** of the Pi. Attach the monitor by HDMI — you will not
need it after this step, but if something goes wrong the screen is where it says so. Plug in the
power supply last.

Wait about 60 seconds, then from the MacBook:

```bash
ssh yourusername@raspberrypi.local
```

If `raspberrypi.local` does not resolve, read the IP address off the monitor and use that instead.

```bash
sudo apt update && sudo apt full-upgrade -y
```

**GATE:** you have an SSH shell on the Pi. Unplug the monitor.

### B.4 Enable and slow the I2C bus

```bash
sudo raspi-config    # Interface Options → I2C → Yes
sudo nano /boot/firmware/config.txt
```

Find the existing `dtparam=i2c_arm=on` line and replace it with:

```
dtparam=i2c_arm=on,i2c_arm_baudrate=10000
```

On Raspberry Pi OS Bookworm and later the file is at `/boot/firmware/config.txt`. On older
releases it is `/boot/config.txt`. Then `sudo reboot`.

> **Why 10 kHz instead of the default 100 kHz:** the Adafruit seesaw chip in the soil sensor
> stretches the I2C clock, and the Pi's BCM2835 I2C peripheral implements clock stretching
> incorrectly. At normal speed you get intermittent garbage readings and occasional
> `OSError: [Errno 121] Remote I/O error` — the worst kind of bug, because it works most of the
> time. Slowing the clock buries the stretch inside a single cycle. Both sensors still poll far
> faster than the 5-minute interval needs.

### B.5 Install dependencies

```bash
sudo apt install -y espeak-ng i2c-tools alsa-utils python3-pip python3-venv

python3 -m venv --system-site-packages ~/pot-env
source ~/pot-env/bin/activate
pip install adafruit-circuitpython-seesaw adafruit-circuitpython-bh1750 anthropic flask
```

`--system-site-packages` matters: `gpiozero` ships with the OS rather than pip, and a plain venv
would not see it.

Add `source ~/pot-env/bin/activate` to the end of `~/.bashrc` so every SSH session starts in the
venv.

### B.6 Wire the sensors and button

**Power the Pi down first:** `sudo shutdown -h now`, wait for the green light to stop, then unplug.

Pin 1 is the corner pin nearest the microSD slot and the board edge. Odd pins are the row nearest
the board edge; even pins are the inner row. Counting is easiest in pairs: pins 1/2 are the first
pair, 3/4 the second, 5/6 the third, and so on.

| Wire | Function | Pi physical pin |
| --- | --- | --- |
| Soil sensor VIN | 3V3 | **1** |
| Soil sensor GND | GND | **6** |
| Light sensor VIN | 3V3 | **17** |
| Light sensor GND | GND | **9** |
| Button leg A | GPIO17 | **11** |
| Button leg B | GND | **14** |

Then the breadboard, two rows:

- **Row 1 (SDA):** a male-male jumper from Pi pin **3** into the row, plus two more jumpers standing
  in the same row for the soil and light **SDA** sockets to push onto.
- **Row 2 (SCL):** the same, from Pi pin **5**, for both **SCL** sockets.

A breadboard row is five connected holes, so a row comfortably holds all three.

> **Count the pins twice before applying power.** Pins 2 and 4 sit immediately alongside pin 1 and
> carry **5 V**. The Pi's GPIO is not 5 V tolerant, and 5 V on an I2C line can permanently damage
> the board. Soil VIN goes to pin **1**; light VIN goes to pin **17**.

> **Wire colours are not a reliable guide.** Adafruit's JST PH and JST SH cables use different
> colour orders. Go by the label silkscreened on the sensor board next to the connector, not by
> the colour of the wire.

Push the button's legs into the breadboard rather than trying to hold jumpers against it — a
momentary button has four legs that are internally paired, and a loose connection here is the most
common cause of a "the button doesn't work" afternoon. No resistor is needed; `gpiozero` enables
the Pi's internal pull-up by default.

Power back on.

### B.7 Verify the sensors

```bash
sudo i2cdetect -y 1
```

**GATE:** both `23` (BH1750) and `36` (seesaw soil sensor) must appear in the grid.

- Neither appears → check 3V3 and GND first, then SDA/SCL.
- Only one appears → the missing device's SDA or SCL is not seated in its breadboard row.
- Both appear → wiring is correct.

Then a live read (`~/sensors.py`):

```python
import time, board
from adafruit_seesaw.seesaw import Seesaw
import adafruit_bh1750

i2c = board.I2C()
soil = Seesaw(i2c, addr=0x36)
light = adafruit_bh1750.BH1750(i2c)

while True:
    print(f"moisture={soil.moisture_read():5d}  "
          f"soil_temp={soil.get_temp():5.1f}C  "
          f"lux={light.lux:8.1f}")
    time.sleep(1)
```

**GATE:** let it run for 100 readings with no `OSError`. If errors appear, drop the baudrate in
`/boot/firmware/config.txt` to `5000` and reboot.

### B.8 Verify audio — before writing any application code

```bash
arecord -l              # lists capture devices — find the USB mic's card number
aplay -l                # lists playback devices
```

Note the microphone's card and device numbers from `arecord -l` (commonly card 1, device 0).

```bash
# Record 5 seconds at the rate Whisper wants
arecord -D plughw:1,0 -f S16_LE -r 16000 -c 1 -d 5 /tmp/test.wav
aplay /tmp/test.wav
speaker-test -t wav -c 2      # Ctrl-C to stop
espeak-ng "I am a plant and I am thirsty"
```

**GATE:** you can hear your own recording, and you can hear espeak, both through the speakers.

If there is no sound: check the speakers have their own power, that the 3.5 mm plug is fully seated
in the Pi's AV jack (not the HDMI port), and try `alsamixer` to confirm the volume is not at zero.
On older Raspberry Pi OS releases, force output to the headphone jack with `amixer cset numid=3 1`.

If `arecord` fails, the card number is wrong — re-read `arecord -l` and substitute.

Recording at 16 kHz mono is deliberate: it is exactly what Whisper wants, so no conversion step is
needed and the files stay small enough that the network hop is negligible.

### B.9 Set up Whisper on the MacBook

```bash
brew install cmake
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp
sh ./models/download-ggml-model.sh base.en
cmake -B build && cmake --build build -j --config Release
```

Verify and time it:

```bash
time ./build/bin/whisper-cli -m models/ggml-base.en.bin -f samples/jfk.wav
```

**GATE:** it transcribes, and Metal acceleration appears in the startup log. Expect well under a
second for an 11-second clip on an M1.

Find the MacBook's IP for the Pi to POST to:

```bash
ipconfig getifaddr en0
```

Wrap `whisper-cli` in a small Flask app exposing `POST /transcribe` per Section 8, listening on
`0.0.0.0` so the Pi can reach it — not `127.0.0.1`, which is the most common reason the Pi gets
connection refused.

### B.10 The Anthropic key

On the Pi:

```bash
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.bashrc
source ~/.bashrc
```

Then in code, construct the client with no arguments — the SDK reads the environment variable
itself:

```python
import anthropic
client = anthropic.Anthropic()

response = client.messages.create(
    model=cfg["llm_model"],          # "claude-opus-5"
    max_tokens=cfg["max_tokens"],    # 150
    output_config={"effort": "low"}, # keeps latency down; adaptive thinking stays on
    system=build_system_prompt(cfg), # personality + species + thresholds
    messages=[{"role": "user", "content": question_with_readings}],
)
text = "".join(b.text for b in response.content if b.type == "text")
```

`response.content` is a list of blocks, not a string — always filter on `b.type == "text"` rather
than indexing `[0]`.

Never hardcode the key or paste it into a file you might share. Per NFR-10 it lives only in the
environment.

To A/B the model at rehearsal (NFR-09), change `llm_model` in the plant context JSON to
`claude-haiku-4-5` and restart. No code change.

### B.11 Calibrate the sensors (FR-07)

Run `~/sensors.py` from B.7 and record five numbers. They go straight into the plant context file.

| Reading | How | Records |
| --- | --- | --- |
| Moisture, open air | Hold the probe in the air | Your dry floor |
| Moisture, dry soil | Probe in the pot before watering | Lower threshold candidate |
| Moisture, watered soil | Probe in the pot ~1 min after watering | Upper threshold candidate |
| Lux, demo table | Sensor sitting where it will sit | Normal light level |
| Lux, hand covering | Palm over the sensor | Your "too dark" floor |

Set `moisture_counts.min` a little above the dry-soil figure and `light_lux.min` between the
covered and uncovered readings.

**GATE:** covering the sensor with a hand must reliably cross the threshold. If it does not, the
proactive alert cannot be demonstrated on demand and the second success criterion is unprovable.

Only the ribbed probe goes into the soil. The end with the connector stays dry.

### B.12 Order of assembly for the software

Build in this sequence so that each piece is testable the moment it is written:

1. Sensor read function — verified against B.7.
2. Record function — verified by playing back the WAV.
3. Transcribe function — POST a saved WAV, confirm the text comes back.
4. LLM function — call it with hardcoded readings and a hardcoded question, print the reply.
5. Speak function — pipe a fixed string to `espeak-ng`.
6. Chain 1–5 behind the button.
7. Add the polling loop and the busy lock last.

Steps 3 and 4 need no hardware and are exactly what streams 3 and 4 own (Section 10).

### B.13 Troubleshooting

| Symptom | Most likely cause |
| --- | --- |
| `i2cdetect` shows nothing | I2C not enabled in `raspi-config`, or 3V3/GND not connected |
| `i2cdetect` shows one address only | The missing sensor's SDA or SCL is not seated in its breadboard row |
| Intermittent `OSError: [Errno 121]` | Baudrate still too high — drop to `5000` and reboot |
| Moisture reads a constant ~200 | Probe is in air, or VIN is not connected |
| `arecord: No such file or directory` | Wrong card number in `-D plughw:N,0` — re-check `arecord -l` |
| No sound from espeak | Speakers unpowered, plug in the wrong socket, or volume at zero in `alsamixer` |
| Button fires constantly | Leg wired to 3V3 instead of GND — it must be GPIO17 and GND |
| Button never fires | Legs in the wrong breadboard rows — a momentary button's four legs are internally paired |
| Pi cannot reach the Mac | Client isolation on the office WiFi, or Flask bound to `127.0.0.1` instead of `0.0.0.0` |
| Anthropic call hangs | The Pi has no internet — re-run the B.1 gate |
| `raspberrypi.local` won't resolve | Use the raw IP; find it with `hostname -I` on the Pi |

---

## Appendix C — Glossary

Every acronym, abbreviation, and piece of jargon used in this document. Grouped by area rather than
strictly alphabetised, because most lookups happen while you are working on one particular thing.

### C.1 Document and process

| Term | Stands for | Meaning here |
| --- | --- | --- |
| **PRD** | Product Requirements Document | This document. Defines what gets built and how you know it works. |
| **FR** | Functional Requirement | A thing the system does. `FR-01` is the push-to-talk loop. |
| **NFR** | Non-Functional Requirement | A quality the system must have — speed, reliability, cost. Not a feature. |
| **UX** | User Experience | How the thing feels to use, as opposed to whether it technically works. |
| **GATE** | — | A checkpoint in Appendix B that must pass before moving on. Not an acronym; a convention used in this doc. |
| **A/B test** | — | Running two options under the same conditions and comparing. Here: Opus 5 versus Haiku 4.5 for latency. |
| **Must / Should / Could Have** | — | Priority levels. Must Have or the demo fails; Should Have if time allows; Could Have only if everything else is done. |

### C.2 Hardware and electronics

| Term | Stands for | Meaning here |
| --- | --- | --- |
| **GPIO** | General-Purpose Input/Output | The 40 pins along the Pi's edge. Software can read or set each one. `GPIO17` is the button's pin. |
| **I2C** | Inter-Integrated Circuit ("eye-squared-see") | A two-wire bus that lets several sensors share the same pair of wires. Each device has its own address, so they don't collide. |
| **SDA** | Serial Data | The I2C data wire. Physical pin 3 on the Pi. |
| **SCL** | Serial Clock | The I2C clock wire. Physical pin 5 on the Pi. |
| **I2C address** | — | A number identifying a device on the bus. Soil sensor `0x36`, light sensor `0x23`. `0x` means hexadecimal. |
| **Clock stretching** | — | When a slow device holds the clock line down to say "wait, not ready." The Pi handles this badly, which is why NFR-08 slows the bus. |
| **Baudrate** | — | The bus speed. Default 100000 (100 kHz); we set 10000 (10 kHz). |
| **VIN** | Voltage In | The power input pin on a sensor. Connects to a 3V3 pin on the Pi. |
| **GND** | Ground | The return path for current. Every device needs one. The Pi has eight GND pins. |
| **3V3** | 3.3 volts | The Pi's logic voltage. Both sensors run on this. |
| **5V** | 5 volts | Also present on pins 2 and 4. **Do not connect it to a sensor or an I2C line** — the Pi's GPIO is not 5 V tolerant and will be damaged. |
| **Pull-up resistor** | — | Holds a pin at a known voltage when nothing is pressing the button. The Pi has these built in; `gpiozero` switches one on for you. |
| **Momentary button** | — | A button that is only "on" while held, like a doorbell. Four legs, internally paired. |
| **Breadboard** | — | A passive grid of spring-loaded holes for joining wires without soldering. Each row of five holes is internally connected. Fully model-agnostic — any breadboard works. |
| **Jumper wire** | — | A short wire with connectors on both ends. **Male** = a pin; **female** = a socket. You need male-to-male for the breadboard rows. |
| **DuPont** | — | The common name for the small rectangular jumper connectors. Your sensor cables end in female DuPont sockets. |
| **JST PH / JST SH** | — | Two connector families, differing in pin spacing (2.0 mm and 1.0 mm). The soil sensor uses PH, the light sensor SH. They are not interchangeable — this is why you bought two different cables. |
| **STEMMA / STEMMA QT** | — | Adafruit's names for their plug-and-play sensor connectors. STEMMA QT is the small one and is electrically the same as SparkFun's **Qwiic**. |
| **seesaw** | — | The small microcontroller Adafruit put on the soil sensor board. It does the capacitive measurement and reports it over I2C. It is also the thing that stretches the clock. |
| **Capacitive sensing** | — | Measuring moisture by how the soil changes an electrical field, with no exposed metal to corrode. Returns a raw count, not a percentage. |
| **BH1750** | — | The light sensor's chip. Reports illuminance directly in lux. |
| **ADA4026** | — | Adafruit's product number for the STEMMA soil sensor. |
| **lux** | — | The unit of illuminance. Roughly: dim room 50, office 300–500, overcast day 1000, direct sun 100000. |
| **RAM** | Random Access Memory | Working memory. The Pi has 512 MB, and this is the constraint that pushes Whisper onto the MacBook. |
| **microSD / SD** | Secure Digital | The memory card. On the Pi it is the boot disk and the only storage — the Pi will not start without it. **Storage, not RAM.** |
| **USB / USB-A** | Universal Serial Bus | The rectangular port. The Pi 3A+ has exactly one, and the microphone owns it. |
| **HDMI** | High-Definition Multimedia Interface | The video output. Used only for first boot. |
| **AV jack** | Audio/Video | The Pi's 3.5 mm socket. Carries both analogue stereo audio and composite video. Your speakers plug in here. |
| **PSU** | Power Supply Unit | The plug. Use the official 12.5 W one — underpowered supplies cause random reboots that look like software bugs. |
| **CPU** | Central Processing Unit | The main processor. |
| **A53** | ARM Cortex-A53 | The specific processor core in the Pi 3A+. Four of them at 1.4 GHz. |
| **BCM2835** | — | The Broadcom chip family whose I2C peripheral implements clock stretching incorrectly. The reason for NFR-08. |
| **M1** | — | Apple's first in-house Mac processor. In your MacBook Pro. |
| **Metal** | — | Apple's GPU framework. `whisper.cpp` uses it for the large speed-up on the M1. |

### C.3 Networking

| Term | Stands for | Meaning here |
| --- | --- | --- |
| **LAN** | Local Area Network | The local network. What lets the Pi talk to the MacBook. |
| **WAN** | Wide Area Network | The internet. What lets the Pi reach the Anthropic API. **You need both at once.** |
| **IP** | Internet Protocol | A device's address on a network, e.g. `192.168.1.42`. |
| **SSID** | Service Set Identifier | A WiFi network's name. |
| **SSH** | Secure Shell | A way to get a command-line session on the Pi from the MacBook, over the network. This is how you will do nearly all Pi work. |
| **Headless** | — | Running a computer with no monitor or keyboard attached, controlling it over SSH. How the Pi is set up here. |
| **Client isolation** | — | A network setting that lets devices reach the internet but not each other. Common on corporate and guest WiFi. It would break the Pi-to-MacBook hop. |
| **Captive portal** | — | The login page some networks show before granting access. **A headless Pi cannot click through one**, which is why the B.1 gate exists. |
| **Hotspot** | — | Sharing a phone's mobile data as a WiFi network. Plan B for NFR-02. |
| **`.local`** | — | A name that resolves on the local network without a DNS server, e.g. `raspberrypi.local`. Handy, but not always permitted — fall back to the raw IP. |
| **`0.0.0.0` vs `127.0.0.1`** | — | Where a server listens. `127.0.0.1` accepts only connections from the same machine; `0.0.0.0` accepts them from the network. Binding to the wrong one is the most common cause of "connection refused" between the Pi and the Mac. |
| **HTTP** | Hypertext Transfer Protocol | The protocol used for both links in Section 8. Chosen because you can debug it with `curl`. |
| **POST** | — | The HTTP method for sending data to a server. Used for the WAV upload and the trigger messages. |
| **multipart/form-data** | — | The HTTP encoding for uploading a file. How the WAV reaches the MacBook. |
| **HTTP status code** | — | The three-digit result of a request. `200` success, `401` unauthorised, `404` not found, `405` wrong method, `000` in curl means it could not connect at all. |
| **Flask** | — | A small Python web-server library. Both services in Section 8 are Flask apps. |

### C.4 Software, audio, and AI

| Term | Stands for | Meaning here |
| --- | --- | --- |
| **LLM** | Large Language Model | The AI that writes the plant's replies. Here, Anthropic's Claude. |
| **API** | Application Programming Interface | A service you call from code. The Anthropic API is where the Pi sends the question. |
| **SDK** | Software Development Kit | An official library that wraps an API. The `anthropic` Python package. |
| **API key** | — | The secret that authenticates your API calls. Kept in an environment variable, never in code (NFR-10). |
| **STT** | Speech-to-Text | Turning recorded audio into words. Whisper does this. Also called transcription or ASR. |
| **TTS** | Text-to-Speech | Turning words into audible speech. `espeak-ng` does this. |
| **Whisper** | — | OpenAI's open-source speech-recognition model. Free, and run entirely on your own machine — no API, no cost. |
| **`whisper.cpp`** | — | A fast C++ implementation of Whisper. What actually runs on the MacBook. |
| **`base.en` / `tiny.en` / `small.en`** | — | Whisper model sizes. `.en` means English-only, which is faster and more accurate than the multilingual version for English. |
| **`espeak-ng`** | — | A tiny, instant, offline speech synthesiser. Robotic-sounding. The baseline voice. |
| **`pyttsx3`** | — | A Python TTS wrapper. On Linux it just calls espeak. Dropped in v2.0 — see FR-05. |
| **Piper** | — | A modern neural TTS engine. Much more natural, needs far more compute. Stretch goal, on the MacBook. |
| **onnxruntime** | — | The library Piper uses to run its neural model. Part of why Piper is heavy for a 512 MB Pi. |
| **`max_tokens`** | — | A cap on how much the LLM may write. A token is roughly ¾ of a word. Set to 150 here to keep replies short and fast. |
| **`effort`** | — | An Anthropic API setting controlling how much the model deliberates. Set to `low` for speed. |
| **System prompt** | — | Standing instructions to the LLM, separate from the user's question. Where the plant's personality and thresholds live. |
| **Edge-triggered / level-triggered** | — | Edge-triggered fires once when a condition *becomes* true; level-triggered fires repeatedly the whole time it *is* true. FR-04 is edge-triggered so the plant does not nag. |
| **Busy lock** | — | A flag ensuring only one thing speaks at a time (NFR-06). |
| **Polling** | — | Checking something on a repeating timer, rather than being notified. How the sensors are read. |
| **WAV** | Waveform Audio File Format | Uncompressed audio. Recorded at 16 kHz mono 16-bit — exactly what Whisper wants. |
| **kHz** | kilohertz | Thousand times per second. Audio sample rate here; also the I2C bus speed. |
| **Mono / 16-bit** | — | One channel, and 16 bits of precision per sample. Standard for speech. |
| **ALSA** | Advanced Linux Sound Architecture | Linux's audio system. `arecord`, `aplay`, and `alsamixer` are all part of it. Each USB device is a separate "card" with a number. |
| **JSON** | JavaScript Object Notation | A plain-text data format. The plant context file and the transcription response both use it. |
| **OS** | Operating System | Raspberry Pi OS on the Pi, macOS on the MacBook. |
| **Bookworm** | — | The Debian release Raspberry Pi OS is currently based on. Matters because it moved `config.txt` to `/boot/firmware/`. |
| **Lite** | — | The version of Raspberry Pi OS with no desktop environment. Recommended — the desktop would eat ~200 MB of your 512 MB. |
| **`apt` / `pip`** | — | Package installers. `apt` for system software, `pip` for Python libraries. |
| **venv** | virtual environment | An isolated Python library folder, so project packages don't collide with system ones. |
| **`gpiozero`** | — | The beginner-friendly Python library for Pi pins. Ships with Raspberry Pi OS. |
| **`OSError: [Errno 121]`** | Remote I/O error | The specific error an I2C device throws when it cannot be talked to. If you see this, suspect wiring or baudrate. |
| **PII** | Personally Identifiable Information | Data identifying a person. This project collects none. |
| **AI / ML** | Artificial Intelligence / Machine Learning | Used in NFR-03 to mean the LLM, STT, and TTS components collectively. |
| **VAT** | Value Added Tax | UK sales tax. The Appendix A prices include it. |

### C.5 Commands used in Appendix B

| Command | What it does |
| --- | --- |
| `ssh user@host` | Opens a command-line session on the Pi from the MacBook |
| `sudo` | Runs a command with administrator rights |
| `apt update` / `apt install` | Refreshes the package list / installs system software |
| `nano <file>` | Simple text editor. Ctrl-O saves, Ctrl-X exits |
| `raspi-config` | The Pi's configuration menu. Used to enable I2C |
| `i2cdetect -y 1` | Scans the I2C bus and prints which addresses respond. Your main wiring test |
| `arecord` / `aplay` | Records / plays audio. `-l` lists devices |
| `speaker-test` | Plays a test tone through the speakers |
| `alsamixer` / `amixer` | Adjusts volume, interactively / from a script |
| `ping` | Checks whether one machine can reach another |
| `curl` | Makes an HTTP request from the command line. Used to test both network links |
| `hostname -I` | Prints the Pi's IP address |
| `ipconfig getifaddr en0` | Prints the MacBook's IP address (macOS only) |
| `brew` | The macOS package manager |
| `git clone` | Downloads a code repository |
| `cmake` | Builds C++ projects from source. Used for `whisper.cpp` |
| `time <command>` | Runs a command and reports how long it took |
| `shutdown -h now` | Powers the Pi down safely. **Always do this before unplugging** — pulling power from a running Pi can corrupt the SD card |

---

_This document supersedes PRD.md v1.0 and is the reference for all development, testing, and
assurance activity. Any changes after sign-off must be captured in an updated version before
implementation begins._
