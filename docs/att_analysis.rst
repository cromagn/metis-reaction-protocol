.. _att-analysis:

Attribute Protocol (ATT) Payload Analysis
=========================================

This chapter focuses on the deep decoding of the Attribute Protocol (ATT) payloads exchanged via the proprietary Service UUID (``6e40...0001``).

Based on the sniffed traffic, we have established the roles of the key handles:

- **Handle 0x0003** → Command Channel (WRITE / TX)
- **Handle 0x0005** → Notification Channel (NOTIFY / RX)
- **Handle 0x0006** → Client Characteristic Configuration Descriptor (CCCD)

-----------------------------------------------------------------------

1. Connection and Initialization Sequence (The Handshake)
---------------------------------------------------------

Every communication session between the application (Central) and the device (Peripheral) follows a precise sequence of steps defined by the Attribute Protocol (ATT) to establish and configure the communication channels.

+---------------------------+-------------------------------+----------+-----------+---------------+--------------------------------------------------------------+
| Step                      | Example Packet                | Protocol | Handle    | Command/Value | Description (Function)                                       |
+===========================+===============================+==========+===========+===============+==============================================================+
| **1. MTU Negotiation**    | ``33`` (Exchange MTU Req/Rsp) | ATT      | —         | —             | Negotiates the Maximum Transmission Unit size (e.g. 247 B). |
+---------------------------+-------------------------------+----------+-----------+---------------+--------------------------------------------------------------+
| **2. Enable Notifications | ``35`` (Write Request)        | ATT      | ``0x0006``| ``0100``      | Writes ``0100`` to the CCCD, enabling notifications on      |
| (CCCD)**                  |                               |          |           |               | Handle ``0x0005``.                                          |
+---------------------------+-------------------------------+----------+-----------+---------------+--------------------------------------------------------------+
| **3. Initial Handshake /  | ``34`` (Write Command)        | ATT      | ``0x0003``| ``20``        | Initial **Keep-Alive / Ping** sent to wake the device and   |
| Ping**                    |                               |          |           |               | request first status information.                           |
+---------------------------+-------------------------------+----------+-----------+---------------+--------------------------------------------------------------+

-----------------------------------------------------------------------

2. Command Structure and Mode Mapping (Handle 0x0003)
-----------------------------------------------------

Analysis confirms a **2-byte command structure** for all light and state commands:

::

   [ Opcode ] [ State ID ]

The most common Opcode is ``0x02`` (Set Light State / Mode).  
Commands are typically sent **multiple times (10–15)** to ensure reliable delivery.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2.1. Core Command Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| Action (App Event)                    | Hex Payload       | Opcode ID | State ID  | Description (Confirmed)                                       |
+=======================================+===================+===========+===========+===============================================================+
| **Keep Alive / Ping**                 | ``20``            | ``0x20``  | —         | Periodic keep-alive to maintain connection synchronization.  |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Turn Off / Reset**                  | ``04 05`` → ``05``| ``0x04`` /| —         | Universal command sequence to stop the current illumination  |
|                                       |                   | ``0x05``  |           | or activity.                                                  |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Set Color: RED (Default / Audio)**  | ``02 89``         | ``0x02``  | ``0x89``  | Sets RED light, default mode (audio likely enabled).          |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Set Color: RED (Mute)**             | ``02 91``         | ``0x02``  | ``0x91``  | Sets RED light with **audio muted**.                          |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Set Color: RED (Flash)**            | ``02 A1``         | ``0x02``  | ``0xA1``  | Sets RED light in **flash mode**.                             |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Set Color: RED (Vibration)**        | ``02 C1``         | ``0x02``  | ``0xC1``  | Sets RED light with **strong vibration mode**.               |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Set Color: GREEN**                  | ``02 8A``         | ``0x02``  | ``0x8A``  | Sets the light to GREEN.                                      |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Set Color: YELLOW**                 | ``02 8B``         | ``0x02``  | ``0x8B``  | Sets the light to YELLOW.                                     |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Set Color: BLUE**                   | ``02 8C``         | ``0x02``  | ``0x8C``  | Sets the light to BLUE.                                       |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+
| **Set Color: WHITE / Other State**    | ``02 CC``         | ``0x02``  | ``0xCC``  | **Hypothesized WHITE** or special high-intensity mode.        |
+---------------------------------------+-------------------+-----------+-----------+---------------------------------------------------------------+

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2.2. State ID (Byte 2) Bit Encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **State ID** byte is a **bitmask** controlling both the base color and optional operational features such as audio, flash, and vibration.

+----------------------------+------------------+-------------------------------------------------------------+
| State ID Bit (Weight)      | Hex Value        | Feature Control                                            |
+============================+==================+=============================================================+
| **Bit 6 (64₁₀)**           | ``0x40``         | **Vibration mode toggle** (0 = OFF / 1 = ON)               |
+----------------------------+------------------+-------------------------------------------------------------+
| **Bit 5 (32₁₀)**           | ``0x20``         | **Flash mode toggle** (0 = OFF / 1 = ON)                   |
+----------------------------+------------------+-------------------------------------------------------------+
| **Bit 4 (16₁₀)**           | ``0x10``         | **Audio mute toggle** (0 = Audio ON / 1 = MUTE)            |
+----------------------------+------------------+-------------------------------------------------------------+
| **Bit 3 (8₁₀)**            | ``0x08``         | Default audio flag or secondary color feature (hypothesis) |
+----------------------------+------------------+-------------------------------------------------------------+
| **Remaining bits**         | Varies           | Encode the **base color ID** (e.g. ``0x89``–``0x8C``).     |
+----------------------------+------------------+-------------------------------------------------------------+

-----------------------------------------------------------------------

3. Event / Notification Structure (Handle 0x0005)
-------------------------------------------------

The device sends notifications whenever a state update or physical event (e.g. touch / hit) occurs.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
3.1. Core Notification Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------------------------+---------------------+-----------+---------+-------------------------------------------------------------+
| Event (Device → Host)     | Hex Payload Example | Opcode ID | Data    | Description                                                 |
+===========================+=====================+===========+=========+=============================================================+
| **Status Response**       | ``21 03 87 01``     | ``0x21``  | Varies  | Response to ``0x20`` ping. Indicates health, session or     |
|                           |                     |           |         | battery-related status.                                    |
+---------------------------+---------------------+-----------+---------+-------------------------------------------------------------+
| **Sensor Data Stream**    | ``03 00 a0 03``     | ``0x03``  | Varies  | Real-time event stream (hit detection, pressure, intensity |
|                           |                     |           |         | feedback) while a light is active.                          |
+---------------------------+---------------------+-----------+---------+-------------------------------------------------------------+
