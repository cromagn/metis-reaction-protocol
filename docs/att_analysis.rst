.. _att-analysis:

Attribute Protocol (ATT) Payload Analysis
=========================================

This chapter provides a deep dive into the Attribute Protocol (ATT) payloads exchanged via the proprietary Service UUID (``6e40...0001``).

Based on the sniffed traffic, the roles of the key ATT handles are:

* **Handle ``0x0003``** → Command Channel (WRITE / TX)
* **Handle ``0x0005``** → Notification Channel (NOTIFY / RX)
* **Handle ``0x0006``** → Client Characteristic Configuration Descriptor (CCCD)

-----------------------------------------------------------------------

1. Connection and Initialization Sequence
-----------------------------------------

Every session between the Central (App) and Peripheral (Metis) follows this startup sequence:

.. list-table:: Initialization Flow
   :header-rows: 1
   :widths: 20 15 10 15 40

   * - Step
     - Protocol
     - Handle
     - Value
     - Description
   * - MTU Negotiation
     - ATT
     - —
     - —
     - Negotiates Max Transmission Unit (up to 247 bytes).
   * - Enable Notifications
     - ATT
     - ``0x0006``
     - ``0100``
     - Enables notifications on Handle ``0x0005``.
   * - Initial Ping
     - ATT
     - ``0x0003``
     - ``20``
     - Wakes the device and requests initial status.

.. image:: _static/Init_Sequence.jpg
   :alt: Initialization sequence sniff
   :align: center
   :width: 90%

-----------------------------------------------------------------------

2. Command Structure (Handle 0x0003)
------------------------------------

Commands sent to the device typically follow a **2-byte format**: ``[Opcode] [Configuration Bitmask]``.

* **Opcode 0x02:** Arms the device (starts the light/sensor).
* **Opcode 0x20:** Keep-alive / Status request.
* **Opcode 0x04 / 0x05:** Stop / Reset sequence.

Configuration Bitmask (The "State ID")
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using **Opcode 0x02**, the second byte defines the device behavior:

+-------+-------+-------+-------+-------+-------+-------+-------+
| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
+-------+-------+-------+-------+-------+-------+-------+-------+
|   Sensor Mode | Flash | !Audio| Start |     Color     | Fixed |
+-------+-------+-------+-------+-------+-------+-------+-------+

* **Bits 7-6 (Sensor Mode):** ``00``: Close | ``01``: Far | ``10``: Vib. Low | ``11``: Vib. High.
* **Bit 5 (Flash):** ``1``: Enable LED flash on impact.
* **Bit 4 (Audio Disable):** ``1``: Mute touch sound (**Inverted logic**).
* **Bit 3 (Start Sound):** ``1``: Beep when the light turns on.
* **Bits 2-1 (Color):** ``00``: Red | ``01``: Yellow | ``10``: Blue | ``11``: Green.
* **Bit 0 (Fixed):** Must always be ``1`` for command recognition.

Verified Command Examples
^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Common Configuration Payloads
   :widths: 20 20 60
   :header-rows: 1

   * - Full Payload (Hex)
     - Config Byte (Bin)
     - Description
   * - ``02 01``
     - ``0000 0001``
     - Red, Proximity (Close), Sound ON.
   * - ``02 41``
     - ``0100 0001``
     - Red, Proximity (Far), Sound ON.
   * - ``02 A1``
     - ``1010 0001``
     - Red, Vib. Low, Flash ON, Sound ON.
   * - ``02 FB``
     - ``1111 1011``
     - Yellow, Vib. High, Flash ON, Start Beep ON.

-----------------------------------------------------------------------

3. Telemetry and Notifications (Handle 0x0005)
----------------------------------------------

The device communicates events using a 4-byte notification: ``03 00 YY ZZ``.

* **Byte 0 (Opcode):** Always ``03`` for sensor events.
* **Byte 2 (Reaction Time):** Time in centiseconds (1/100s) from stimulus to impact.
* **Byte 3 (Impact Force):** Raw intensity value of the hit/proximity trigger.

Status Response
^^^^^^^^^^^^^^^
In response to a ``20`` ping, the device returns: ``21 03 XX YY``.
This typically carries battery level or system readiness states.

-----------------------------------------------------------------------

4. Connection Maintenance
-------------------------

To keep the device from timing out, the host must send:
1. **Heartbeat:** ``20`` every 2-5 seconds.
2. **Shutdown:** To stop a session, send the sequence ``04 05`` followed by ``05``.

.. image:: _static/Power_off_sequence.jpg
   :alt: Power off sequence sniff
   :align: center
   :width: 90%