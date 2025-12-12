.. _ble-protocol:

Bluetooth Low Energy (BLE) Protocol Analysis
=============================================

This chapter details the findings related to the Bluetooth Low Energy communication stack, moving from the low-level identification (GAP) to the high-level data structure (GATT) that governs command and event exchange. 

1. Generic Access Profile (GAP) Analysis
----------------------------------------

The Generic Access Profile (GAP) defines how the METIS Reaction Lights make themselves available for connection. Our analysis, performed using Wireshark and a BLE sniffer, confirms the following identification patterns during the advertising phase.

1.1. Device Naming and Identification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The devices broadcast their presence using standard **SCAN_RSP** (Scan Response) packets.

* **Identifiable Name:** All devices use a common prefix followed by a unique, numeric identifier, observed in the local name field (0x09) of the advertising payload.
    * **Pattern:** ``$react-X-`` (where X is the sequential device number).
    * **Examples Observed:** ``$react-1-`` and ``$react-2-``
    * **Purpose:** This consistent naming convention simplifies the initial identification and selection process within the official mobile application.

1.2. MAC Addresses and Public Addressing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MAC addresses observed in the SCAN_RSP packets appear to be **Public Addresses** (non-randomized), which suggests that the address remains static for each device and simplifies persistent connection attempts.

* **MAC Addresses Observed:**
    * **Device $react-1- (Example):** ``7e:ad:07:91:53:e6``
    * **Device $react-2- (Example):** ``69:de:d6:c7:4c:71``
    * **Note:** Also MAC address ``cc:03:01:ea:28:91``  and ``cc:03:01:ea:28:91`` was also identified for ``$react-1-`` and ``$react-2-`` as initial address (tbd)

2. Generic Attribute Profile (GATT) Discovery
---------------------------------------------

The Attribute Discovery phase was critical in identifying the proprietary communication channels. The analysis reveals a single custom service responsible for all command and event exchange.

2.1. Identified Custom Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The primary communication channel is defined by the following proprietary 128-bit UUID, acting as a command/data relay service:

* **Custom Service UUID:** ``6e400001-b5a3-f393-e0a9-e50e24dcca9e``

2.2. Characteristic Identification Methodology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The specific roles of the two characteristics were determined by analyzing their respective **GATT Properties**, which define the direction of the data flow and strongly indicate a **UART Emulation Service** pattern (common in Nordic nRF chipsets).

+----------------------------+------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
| Characteristic UUID Suffix | Property                                 | Communication Role                                                                                                |
+============================+==========================================+===================================================================================================================+
| **0002** | ``['write', 'write-without-response']``  | **Command TX:** The presence of the ``WRITE`` property confirms this is the endpoint for commands sent *to* the device. |
+----------------------------+------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
| **0003** | ``['notify']``                           | **Event RX:** The ``NOTIFY`` property confirms the device uses this channel to send asynchronous data *to* the host.   |
+----------------------------+------------------------------------------+-------------------------------------------------------------------------------------------------------------------+

This pattern (Service-0001, Write-0002, Notify-0003) is a strong indicator of a standard **UART Emulation Service** implementation commonly found in Bluetooth chipsets like the Nordic nRF series.

2.3. Command and Event Characteristics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Based on the above methodology, the roles are clearly assigned:

* **Characteristic 1: Command Channel (TX)**
    * **UUID:** ``6e400002-b5a3-f393-e0a9-e50e24dcca9e``
    * **Role:** The **WRITE** channel for all host-to-device commands (setting color, starting a drill).

* **Characteristic 2: Notification Channel (RX)**
    * **UUID:** ``6e400003-b5a3-f393-e0a9-e50e24dcca9e``
    * **Role:** The **NOTIFICATION** channel for all device-to-host events (sensor hit, battery status).

3. Initial Protocol Hypotheses (ATT Protocol)
---------------------------------------------

Now that the Service and Characteristic UUIDs are known, the next crucial step is the deep analysis of the Attribute Protocol (ATT) payloads. This involves decoding the byte arrays sent to and from the characteristics identified above.

3.1. Command Structure Hypothesis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The proprietary protocol likely uses a structured byte array for commands sent to the **Command Channel (UUID 0002)**, typically including:

* **Command ID:** A fixed byte used to identify the function (e.g., set color, request status).
* **Device Address/ID:** Byte(s) specifying which light in the network is the target.
* **Arguments:** Payload data (e.g., RGB values, program number, duration).
* **Checksum/CRC (Optional):** Used for data integrity verification.

We will proceed to the **:doc:`att_analysis`** chapter to analyze captured data and map these initial commands.

---
Contextual Resources
--------------------

For context regarding the device functionality and use case, the following resource is useful:

* `METIS Reaction Lights | Reaction Training - YouTube <https://www.youtube.com/watch?v=i3YOfDJhfew>`_