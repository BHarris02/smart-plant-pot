# Product Requirements Document

**Project:** Smart Plant Pot ("Talking Plant")
**Version:** 1.0
**Date:** 2026-09-08
**Prepared by:** Requirements Elicitation Skill
**Status:** Draft - Awaiting stakeholder sign-off

---

## 1. Overview

### 1.1 Purpose

The Smart Plant Pot is a hackathon project that gives a houseplant a "voice." Using soil moisture,
soil temperature, and light sensors combined with an LLM (Anthropic Claude), the pot can be asked
questions aloud and respond in character through a speaker — as if the plant itself were speaking
about its own condition and needs. The pot can also proactively speak up, unprompted, if its
sensor readings fall outside a configured safe range (e.g. too dry, too dark).

### 1.2 Success Criteria

Success is a working live demo at the hackathon in which:

- A judge or presenter holds down a physical button, asks the plant a question aloud, releases
  the button, and the plant responds audibly through the speaker with a relevant, in-character
  answer that reflects its actual current sensor readings.
- The plant can be shown proactively speaking up when a sensor reading is pushed outside its
  configured safe range (can be demonstrated live or via a controlled trigger).

This is a demo-first build. There is no post-hackathon production, maintenance, or user base
requirement — success is defined entirely by whether the above works reliably in front of judges.

### 1.3 Background

This is a greenfield hackathon build with a 2-day development window and a team of 4 developers,
all beginners with Raspberry Pi hardware. There is no existing system, codebase, or prior art to
build on. The hardware (Raspberry Pi 3 Model A+, I2C soil and light sensors, USB microphone, USB
speakers) has already been selected and procured (see Section 7 and Appendix A).

---

## 2. Users

| User type            | Description                                                        | Primary goal                                                              | Key frustration today                          |
| -------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------ |
| Demo presenter        | One of the 4 team members operating the pot live at the demo table | Trigger a smooth, reliable voice interaction with the plant in front of judges | No existing way to know a plant's own "state" or needs |
| Judge / demo audience | Hackathon judges and onlookers watching the live demo              | Be entertained/impressed and understand the concept quickly                | N/A — first exposure to the concept              |

### User Personas

**The Presenter** is a member of the build team, comfortable with the concept but not necessarily
the one who wired the hardware. During the demo they hold down a physical button, ask the plant a
question in a normal speaking voice, and let go. They need the interaction to be fast, forgiving of
imperfect wiring, and to have a reliable fallback if the primary input method fails mid-demo.

**The Judge** has never seen this system before and will watch one or two interactions at most.
They need the concept ("this plant can tell you what it needs, in character") to be obvious within
seconds — no explanation of sensors, APIs, or architecture should be necessary to understand what
just happened.

---

## 3. Scope

### 3.1 In Scope

- Physical button (GPIO-wired) for push-to-talk voice input: hold to record, release to send.
- Keyboard-key fallback trigger (Plan B) if the physical button fails or is unreliable, using the
  same hold-to-record/release-to-send behaviour.
- Local speech-to-text transcription of the recorded question, run on a team laptop (not the Pi)
  to work around the Pi 3A+'s limited RAM.
- A configurable "plant context" (moisture range, light range, plant name/species, personality/voice
  style) that is included in every request sent to the LLM.
- LLM request/response cycle via the Anthropic API: transcribed question + plant context sent as a
  single request, no external search, no tool use — response is a plain text string.
- Text-to-speech playback of the LLM's response through the USB speakers, using a local/offline TTS
  engine (no third-party TTS API).
- Periodic background polling of soil moisture and light sensors on a fixed interval.
- Proactive unprompted speech: if a periodic reading falls outside the configured safe range, the
  same LLM + TTS pipeline is triggered automatically to speak up about it.
- Basic turn-taking so the proactive check and the button-triggered flow cannot speak over each
  other (single "busy" flag; proactive checks are skipped while a response is already playing).

### 3.2 Out of Scope

- Any production hosting, user accounts, authentication, or multi-pot/multi-user support.
- Mobile app, web dashboard, or any UI beyond the physical pot and its speaker/mic/button.
- Wake-word or continuous voice-activated listening (explicitly deferred in favour of push-to-talk).
- Cloud/paid TTS (e.g. ElevenLabs, OpenAI TTS) and cloud STT (e.g. OpenAI Whisper API) — both
  explicitly rejected in favour of free/local processing (see Section 6, Constraints).
- Cloning or imitating the voice/likeness of any named real person (e.g. a celebrity) — accents and
  character tone are achievable and in scope, but literal voice cloning of a real individual is not.
- Long-term data logging, historical trend analysis, or notifications outside of the live spoken
  interaction (e.g. no SMS/push notifications).
- Support for crop-specific pots, multiple simultaneous plants, or any hardware beyond the parts
  list in Appendix A.

---

## 4. Features & Acceptance Criteria

### 4.1 Push-to-Talk Voice Question (Core Loop)

**Description:** The presenter holds down a physical button, speaks a question to the plant, and
releases the button to send. The system transcribes the question, sends it with the plant's
context to the LLM, and speaks the response aloud through the speaker.

**Requirement ref:** FR-01

**Priority:** Must Have

**Acceptance Criteria:**

- [ ] Holding the button starts audio recording via the USB microphone; recording stops the moment
      the button is released.
- [ ] The recorded audio is transcribed to text (via local Whisper running on a team laptop, not
      the Pi).
- [ ] The transcribed question is combined with the current plant context (see FR-03) into a single
      request sent to the Anthropic API.
- [ ] The LLM's text response is converted to speech and played audibly through the USB speakers
      within a reasonable time of releasing the button (target: under 10 seconds end-to-end,
      acknowledging local STT/TTS speed is a risk factor — see NFR-01).
- [ ] The spoken response reflects the plant's actual current sensor readings and configured
      personality/voice style, not a generic canned answer.
- [ ] If no question is captured (e.g. button released with no speech, or silence), the system does
      not crash and either says nothing or gives a short "I didn't catch that" style response.

**Usability Criteria:**

- [ ] A presenter who has never used the system before can successfully trigger a question-and-answer
      exchange on their first attempt, having only been told "hold the button, ask a question, let go."
- [ ] The delay between releasing the button and the plant beginning to respond is short enough that
      a judge does not think the system has failed or frozen.

---

### 4.2 Keyboard Fallback Trigger (Plan B)

**Description:** If the physical button proves unreliable during setup or the live demo, a
keyboard key (e.g. spacebar) on a connected keyboard provides an identical hold-to-record,
release-to-send trigger, using the exact same recording/transcription/response pipeline as FR-01.

**Requirement ref:** FR-02

**Priority:** Must Have

**Acceptance Criteria:**

- [ ] A designated key can be held down to start recording and released to send, mirroring the
      physical button's behaviour exactly.
- [ ] Switching between the button and the keyboard fallback requires no code changes — both should
      be able to trigger the same underlying recording function (e.g. both wired to call the same
      script/function).
- [ ] The fallback has been tested and confirmed working before the demo, not just built and assumed
      functional.

---

### 4.3 Plant Context Configuration

**Description:** A configurable, structured set of information about the specific plant in the pot
that is included in every LLM request, so the plant's responses are grounded in its real identity
and thresholds rather than the LLM guessing or web-searching.

**Requirement ref:** FR-03

**Priority:** Must Have

**Acceptance Criteria:**

- [ ] The context is stored in a single, easily editable file (e.g. JSON, YAML, or Python dict) that
      a non-developer team member can update on demo day without touching the pipeline code.
- [ ] The context includes at minimum: plant name/nickname, plant species, ideal soil moisture range
      (min/max), ideal light range in lux (min/max), and a personality/voice style description
      (e.g. tone, accent, character).
- [ ] Every request made to the LLM (both button-triggered and proactive) includes the full current
      context alongside the live sensor readings at the time of the request.
- [ ] No external web search or lookup is performed by the LLM at request time — all plant-specific
      knowledge the LLM needs is provided directly in the request.

---

### 4.4 Proactive Threshold Alert (Unprompted Speech)

**Description:** The system periodically checks soil moisture and light readings against the safe
ranges defined in the plant context. If a reading falls outside the safe range, the plant proactively
speaks up through the speaker without being asked a question, explaining what is wrong in character.

**Requirement ref:** FR-04

**Priority:** Should Have

**Acceptance Criteria:**

- [ ] Soil moisture and light sensors are read on a fixed polling interval (recommended: every 5–10
      minutes, configurable).
- [ ] If a reading is outside the min/max range defined in the plant context, an LLM request is
      automatically triggered including the context and the out-of-range reading, and the response
      is spoken aloud.
- [ ] If a periodic check occurs while a button-triggered (or fallback-triggered) response is already
      being generated or played, the periodic check is skipped rather than overlapping/interrupting.
- [ ] Once a threshold breach has been spoken aloud, the system does not repeat the same alert on
      every subsequent poll while the condition persists (avoids the plant nagging on a loop) —
      exact repeat/cooldown behaviour to be decided by the dev team during build, but must not spam.

---

### 4.5 Local Text-to-Speech Output

**Description:** The LLM's text response is converted to audible speech and played through the USB
speakers, using free, offline-capable tooling so the demo does not depend on venue internet or paid
API credits for voice output.

**Requirement ref:** FR-05

**Priority:** Must Have

**Acceptance Criteria:**

- [ ] The baseline implementation uses `pyttsx3` (free, local, offline, no API key required).
- [ ] Audio output plays through the USB-powered speakers via the Pi's 3.5mm AV jack (per the wiring
      plan in Appendix A).
- [ ] **Stretch goal (Could Have):** if time remains after the Must Have and Should Have features are
      working, upgrade the voice from `pyttsx3` to **Piper TTS** (free, open-source, offline neural
      TTS) for noticeably more natural-sounding output, without introducing an internet dependency.

---

### 4.6 Local Speech-to-Text Transcription

**Description:** Recorded audio from the microphone is transcribed to text using a local
(non-API, non-paid) Whisper model, run on a team laptop rather than the Raspberry Pi itself due to
the Pi 3 Model A+'s limited 512MB RAM.

**Requirement ref:** FR-06

**Priority:** Must Have

**Acceptance Criteria:**

- [ ] Recorded audio files are transferred from the Pi to a laptop over a local network connection
      (see Constraints, Section 6) for transcription.
- [ ] The laptop runs a local Whisper model (e.g. `whisper.cpp` or `faster-whisper`) and returns the
      transcribed text to the Pi for use in the LLM request.
- [ ] The Pi-to-laptop connection does not depend on venue WiFi (see NFR-02).

---

## 5. Non-Functional Requirements

| ID     | Category      | Requirement                                                                                                    | Acceptance criterion                                                                                  |
| ------ | ------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| NFR-01 | Performance   | End-to-end response time (button release to audible response start) should be as short as possible; local STT/TTS on modest hardware is a known risk to this. | Team performs a timed test run before the demo; if consistently over ~10-15 seconds, investigate model size or hardware allocation. |
| NFR-02 | Network       | The Pi-to-laptop connection used for STT must not depend on venue WiFi.                                        | Pi and laptop are connected via a dedicated personal hotspot, travel router, or direct Ethernet/USB networking connection, tested before the event. |
| NFR-03 | Cost          | All AI/ML processing components other than the LLM itself must be free (no paid API usage for STT or TTS).     | STT uses local Whisper (free); TTS uses `pyttsx3` or Piper (free). Only the Anthropic LLM API call is a paid/keyed service. |
| NFR-04 | Reliability   | The core voice interaction loop (FR-01) must have a working fallback if the physical button fails.             | Keyboard fallback (FR-02) is built and tested prior to the demo, not left as an untested contingency. |
| NFR-05 | Legal/Ethical | The system must not clone or imitate the voice/likeness of a specific named real person.                       | Voice/personality is achieved via accent and character-style prompting (e.g. "energetic Australian wildlife-presenter tone"), not via cloning a real individual's voice. |
| NFR-06 | Concurrency   | The proactive alert flow (FR-04) and the button-triggered flow (FR-01) must not speak over each other.          | A single shared "busy" flag/lock ensures only one response is generated/played at a time; the periodic check yields to an in-progress user-triggered interaction. |

---

## 6. Constraints

- **Timeline:** 2 days of development, hackathon setting. Prioritisation in this PRD (Must/Should/
  Could Have) reflects this hard constraint and should not be revisited without deprioritising
  something else.
- **Team:** 4 developers, all beginners with Raspberry Pi hardware and wiring. Solutions favouring
  simplicity and pre-built libraries over custom/low-level implementation are preferred throughout.
- **Hardware:** Raspberry Pi 3 Model A+ has only 512MB RAM and a single USB-A port. This rules out
  running local Whisper STT directly on the Pi (offloaded to a laptop instead, see FR-06) and
  requires the USB port to be reserved for the microphone (speakers powered separately via 3.5mm
  jack + independent power source, per Appendix A wiring notes).
- **No paid AI services except the LLM:** STT and TTS must be free/local; only the Anthropic API
  call for the LLM reasoning step is a paid/keyed service.
- **No literal celebrity voice cloning:** accent/personality styling only, for both legal and
  platform terms-of-service reasons.
- **Network dependency risk:** venue WiFi is not to be relied upon for the Pi-to-laptop STT
  connection; the LLM API call to Anthropic will still require genuine internet access.

---

## 7. Data & Integrations

**Key data entities:**

- **Plant context** — plant name/nickname, species, ideal moisture range, ideal light range,
  personality/voice style. Stored in a single editable config file.
- **Sensor readings** — soil moisture, soil temperature, ambient light (lux), read live and used
  transiently per request; no requirement for historical storage/logging in this build.
- **Transcript/response pairs** — transient, used only to build the LLM request and are not
  required to be persisted after the interaction.

**External integrations:**

- **Anthropic API (Claude)** — LLM reasoning/response generation. Requires a genuine internet
  connection and API key (already arranged by the team).
- **Local Whisper (STT)** — runs on a team laptop, not a hosted API.
- **Local `pyttsx3` / Piper (TTS)** — runs locally on the Pi, not a hosted API.

**Data sensitivity:** None. No personal data, no user accounts, no PII is collected or processed.
Audio recordings are transient (used for transcription only) and not required to be retained.

---

## 8. UX Requirements Summary

The interaction must feel immediate and "alive" rather than like operating a device — the presenter
should be able to walk up, hold a button, ask a question in a normal voice, and get an in-character
answer with no visible technical steps in between. See `UX-RESEARCH.md` for full detail, including
the specific risk that local STT/TTS latency could undermine this "alive" feeling if not tested and
tuned before the demo.

Key UX risk to flag for the dev team: response latency and the possibility of the pot's proactive
alert firing at an awkward moment (e.g. interrupting a live Q&A) are the two biggest threats to the
demo feeling polished. Both are addressed functionally in FR-04's concurrency handling and NFR-01,
but should also be rehearsed, not just implemented.

---

## 9. Sign-off

This document represents the agreed requirements for the project as captured in conversation
with the stakeholder. Before development begins, the stakeholder should review this document
and confirm it accurately reflects what was discussed.

| Role               | Name                           | Status   | Date       |
| ------------------ | ------------------------------- | -------- | ---------- |
| Stakeholder        | greenthumb                     | Pending  |            |
| BA / UX Researcher | Requirements Elicitation Skill | Prepared | 2026-09-08 |

---

## Appendix A — Parts List & Build Notes

**Supplier:** The Pi Hut (thepihut.com). All prices incl. VAT.

**Compute & Power**

- Raspberry Pi 3 Model A+ — £24.00
- Official 12.5W Micro-USB PSU (UK plug) — £7.70
- microSD card 32GB — already owned

**Sensors**

- Adafruit STEMMA Soil Sensor — I2C capacitive moisture + soil temperature (ADA4026) — £7.20
- Adafruit BH1750 Light Sensor — I2C, lux (STEMMA QT) — £4.40

**Cables**

- JST PH 4-Pin to Female Socket Cable, 200mm (soil sensor → Pi GPIO) — £1.30
- STEMMA QT/Qwiic JST-SH 4-Pin to Female Sockets, 150mm (BH1750 → Pi GPIO) — £1.00

**Audio**

- Mini USB Microphone — £5.20
- USB Powered Speakers (USB for power, 3.5mm for audio out) — £8.70

**New addition — Input Button (Plan A trigger)**

- Momentary push button (~£1) + two jumper wires (or small breadboard for reliability)
- Wiring: signal to **GPIO17 (physical pin 11)**, ground to any spare **GND pin (e.g. physical pin 9)**
- No resistor needed — use the Pi's internal pull-up resistor (configurable in software via `gpiozero`)

**Total (original list):** £59.50 (not including shipping or the new button)

**Build Notes**

- Both I2C sensors share the same bus: physical pins 1 (3V3), 3 (SDA), 5 (SCL), 6 (GND). Different
  I2C addresses, no conflict.
- The Pi 3A+ has only one USB-A port. Power the speakers from a separate phone charger/power source
  and run their 3.5mm jack into the Pi's AV socket, keeping the USB port free for the microphone.
- No soldering required for sensors (STEMMA/JST cables) or for the button (jumper wires only).
- Recommended Pi-to-laptop network setup for STT offload: personal hotspot, travel router, or
  direct Ethernet/USB connection — not venue WiFi (see NFR-02).

---

_This document is the reference for all development, testing, and assurance activity on this
project. Any changes to requirements after sign-off must be captured in an updated version of
this document before implementation begins._
