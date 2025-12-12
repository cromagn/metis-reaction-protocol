.. _att-analysis:

Attribute Protocol (ATT) Payload Analysis
=========================================

This chapter focuses on the deep decoding of the Attribute Protocol (ATT) payloads exchanged via the proprietary Service UUID (6e40...0001). Based on the sniffed traffic, we have established the roles of the key handles: Handle **0x0003** is the Command Channel (WRITE/TX), Handle **0x0005** is the Notification Channel (NOTIFY/RX), and Handle **0x0006** is the control channel for the notification feature.

1. Connection and Initialization Sequence (The Handshake)
---------------------------------------------------------

Every communication session between the application (Central) and the device (Peripheral) follows a precise sequence of steps defined by the Attribute Protocol (ATT) to establish and configure the communication channels.

| Step | Example Packet | Protocol | Handle | Command/Value | Description (Function) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. MTU Negotiation** | `33` (Exchange MTU Request/Response) | ATT | - | - | Negotiates the Maximum Transmission Unit size (e.g., up to 247 bytes) for larger data packets. |
| **2. Enable Notifications (CCCD)** | `35` (Write Request) | ATT | **`0x0006`** | **`0100`** | Writes the value `0100` (Enable NOTIFY) to the Client Characteristic Configuration Descriptor (CCCD). **Activates Handle `0x0005`**. |
| **3. Initial Handshake/Ping** | `34` (Write Command) | ATT | **`0x0003`** | **`20`** | The app sends the first **Keep-Alive** command to the command channel to wake the device and request the first status update. |

2. Command Structure and Mode Mapping (Handle 0x0003)
------------------------------------------------------

Analysis confirms a 2-byte structure for all light and state commands: **[Opcode] [State ID]**. The most common Opcode is **`0x02`** ("Set Light State/Mode"). Commands are repeatedly sent (10-15 times) to ensure reliable delivery.

2.1. Core Command Set
~~~~~~~~~~~~~~~~~~~~~~

| Action (App Event)          | Hex Payload        | Opcode ID | State ID | Description (Confirmed)                                            |
| :--- | :--- | :--- | :--- | :--- |
| **Keep Alive / Ping** | ``20``             | `0x20` | - | Sent periodically to maintain connection sync.                      |
| **Turn Off / Reset** | **``04 05``** (followed by **``05``**) | `0x04` / `0x05` | - | Universal command sequence to stop the current illumination/action. |
| **Set Color: RED (Default/Audio)** | ``02 89``          | `0x02` | **`0x89`** | Sets RED light with default mode (Audio likely ON). |
| **Set Color: RED (Mute)** | ``02 91``          | `0x02` | **`0x91`** | Sets RED light with **Audio explicitly OFF**. |
| **Set Color: RED (Flash)** | ``02 A1``          | `0x02` | **`0xA1`** | Sets RED light to **Flash Mode**. |
| **Set Color: RED (Vibration)** | ``02 C1``          | `0x02` | **`0xC1`** | Sets RED light to **Large Vibration Mode**. |
| **Set Color: GREEN** | ``02 8A``          | `0x02` | **`0x8A`** | Sets the light to GREEN. |
| **Set Color: YELLOW** | ``02 8B``          | `0x02` | **`0x8B`** | Sets the light to YELLOW. |
| **Set Color: BLUE** | ``02 8C``          | `0x02` | **`0x8C`** | Sets the light to BLUE. |
| **Set Color: WHITE / Other State** | ``02 CC``          | `0x02` | **`0xCC`** | **Hypothesized to be WHITE** (or another key state like "Max Brightness"). |

2.2. State ID (Byte 2) Bit Encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The analysis of the different RED modes confirms that the **State ID** byte is a bitmask controlling both the base color and operational features (like audio, flash, and vibration).

| State ID Bit (Weight) | Value $\mathbf{(Hex)}$ | Feature Control |
| :--- | :--- | :--- |
| **Bit 6** ($\mathbf{64_{10}}$) | $\mathbf{0x40}$ | **Vibration Mode Toggle** ($\mathbf{0 = OFF / 1 = ON}$) |
| **Bit 5** ($\mathbf{32_{10}}$) | $\mathbf{0x20}$ | **Flash Mode Toggle** ($\mathbf{0 = OFF / 1 = ON}$) |
| **Bit 4** ($\mathbf{16_{10}}$) | $\mathbf{0x10}$ | **Audio Mute/ON Toggle** ($\mathbf{0 = ON / 1 = MUTE}$) |
| **Bit 3** ($\mathbf{8_{10}}$) | $\mathbf{0x08}$ | *Default Audio Flag or Secondary Color Feature.* |
| **Remaining Bits** | Varies | Encode the **Base Color ID** (e.g., the difference between $89_{16}$, $8A_{16}$, $8B_{16}$, $8C_{16}$). |

3. Event/Notification Structure (Handle 0x0005)
-----------------------------------------------

The device sends notifications to the host when a status is updated or an event (like a physical touch/hit) occurs.

3.1. Core Notification Set
~~~~~~~~~~~~~~~~~~~~~~~~~~

| Event (Device->Host)          | Hex Payload (Example) | Opcode ID | Data | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Status Response** | ``21 03 87 01`` | `0x21` | Varies | Response to the ``0x20`` ping. Indicates connection health or battery status. |
| **Sensor Data Stream** | ``03 00 a0 03`` | `0x03` | Varies | Real-time data stream (e.g., sensor pressure, hit detection, or light intensity feedback) sent when a color is active. |