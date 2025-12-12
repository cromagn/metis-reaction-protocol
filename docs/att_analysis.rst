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

2. Command Structure and Color Mapping (Handle 0x0003)
------------------------------------------------------

Analysis confirms a 2-byte structure for color commands: **[Opcode] [Color ID]**. The light/color commands (Opcode `0x02`) are repeatedly sent (10-15 times) to ensure successful reception by the device.

2.1. Core Command Set
~~~~~~~~~~~~~~~~~~~~~~

| Action (App Event)          | Hex Payload        | Opcode ID | Color/State ID | Description (Confirmed)                                            |
| :--- | :--- | :--- | :--- | :--- |
| **Keep Alive / Ping** | ``20``             | `0x20` | - | Sent periodically to maintain connection sync.                      |
| **Turn Off / Reset** | **``04 05``** (followed by **``05``**) | `0x04` / `0x05` | - | Universal command sequence to stop the current illumination/action. |
| **Set Color: RED** | ``02 89``          | `0x02` | **`0x89`** | Sets the light to RED. Opcode `0x02` = "Set Light State". |
| **Set Color: GREEN** | ``02 8A``          | `0x02` | **`0x8A`** | Sets the light to GREEN. |
| **Set Color: YELLOW** | ``02 8B``          | `0x02` | **`0x8B`** | Sets the light to YELLOW (Confirms the sequential ID logic). |
| **Set Color: BLUE** | ``02 8C``          | `0x02` | **`0x8C`** | Sets the light to BLUE. |
| **Set Color: WHITE / Other State** | ``02 CC``          | `0x02` | **`0xCC`** | **Hypothesized to be WHITE** (or another key state like "Max Brightness"). |

3. Event/Notification Structure (Handle 0x0005)
-----------------------------------------------

The device sends notifications to the host when a status is updated or an event (like a physical touch/hit) occurs.

3.1. Core Notification Set
~~~~~~~~~~~~~~~~~~~~~~~~~~

| Event (Device->Host)          | Hex Payload (Example) | Opcode ID | Data | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Status Response** | ``21 03 87 01`` | `0x21` | Varies | Response to the ``0x20`` ping. Indicates connection health or battery status. |
| **Sensor Data Stream** | ``03 00 a0 03`` | `0x03` | Varies | Real-time data stream (e.g., sensor pressure, hit detection, or light intensity feedback) sent when a color is active. |