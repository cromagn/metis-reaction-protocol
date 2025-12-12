.. _att-analysis:

Attribute Protocol (ATT) Payload Analysis
=========================================

This chapter focuses on the deep decoding of the Attribute Protocol (ATT) payloads exchanged via the proprietary Service UUID (6e40...0001). We have established that Handle **0x0003** is the Command Channel (WRITE/TX) and Handle **0x0005** is the Notification Channel (NOTIFY/RX).

1. Command Structure and Color Mapping (Handle 0x0003)
------------------------------------------------------

The analysis confirms a 2-byte structure for color commands: **[Opcode] [Color ID]**. The commands are sent repeatedly (10-15 times) to ensure delivery.

1.1. Core Command Set
~~~~~~~~~~~~~~~~~~~~~~

| Action (App Event)          | Hex Payload        | Opcode ID | Color/State ID | Description (Confirmed)                                     |
| :--- | :--- | :--- | :--- | :--- |
| **Keep Alive / Ping** | ``20``             | `0x20` | - | Sent periodically to maintain connection sync.                      |
| **Turn Off / Reset** | **``04 05``** (followed by **``05``**) | `0x04` / `0x05` | - | Universal command sequence to stop illumination/action.             |
| **Set Color: RED** | ``02 89``          | `0x02` | **`0x89`** | Sets the light to RED. Opcode `0x02` = "Set Light State".       |
| **Set Color: GREEN** | ``02 8A``          | `0x02` | **`0x8A`** | Sets the light to GREEN.                                            |
| **Set Color: YELLOW** | ``02 8B``          | `0x02` | **`0x8B`** | Sets the light to YELLOW (Confirmed by sniff).                      |
| **Set Color: BLUE** | ``02 8C``          | `0x02` | **`0x8C`** | Sets the light to BLUE.                                             |
| **Set Color: WHITE / Other State** | ``02 CC``          | `0x02` | **`0xCC`** | **Hypothesized to be WHITE** (or another key state, e.g. "Max Brightness"). |

2. Event/Notification Structure (Handle 0x0005)
-----------------------------------------------

The device sends notifications to the host when a status is updated or an event (like a physical touch/hit) occurs.

2.1. Core Notification Set
~~~~~~~~~~~~~~~~~~~~~~~~~~

| Event (Device->Host)          | Hex Payload (Example) | Opcode ID | Data | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Status Response** | ``21 03 87 01`` | `0x21` | Varies | Response to a ``0x20`` ping. Indicates connection health/battery status. |
| **Sensor Data Stream** | ``03 00 a0 03`` | `0x03` | Varies | Real-time stream data (e.g., sensor pressure, hit detection, or light intensity feedback). |