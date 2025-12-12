.. _att-analysis:

Attribute Protocol (ATT) Payload Analysis
=========================================

This chapter focuses on the deep-dive analysis of the byte arrays (hex payloads) transmitted over the confirmed Command and Notification Characteristics (UUID 0002 and 0003). The goal is to reverse-engineer the proprietary command structure used to control the METIS Reaction Lights.

1. ATT Command Channel Structure (UUID 6e40...0002)
---------------------------------------------------

The Command Channel receives data from the Host (Central) to the Light (Peripheral). Based on typical proprietary BLE protocols, commands are structured as fixed-length or length-prefixed byte packets.

1.1. Proposed Command Packet Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We hypothesize the command packet follows a sequence of functional fields:

+-------------+-------------------------------------------------------------+---------------------------+---------------------------+
| Field (Bytes) | Role/Function                                               | Hypothesis                | Example (Placeholder)     |
+=============+=============================================================+===========================+===========================+
| **Byte 0** | **Start Byte/Command ID** | Always the same value for a specific action (e.g., ``0x01`` for 'Set Color'). | ``0x01``                  |
+-------------+-------------------------------------------------------------+---------------------------+---------------------------+
| **Byte 1** | **Device Target** | Identifies which light (``$react-1-``, ``$react-2-``, or ALL) is the recipient. | ``0xFF`` (All Lights)     |
+-------------+-------------------------------------------------------------+---------------------------+---------------------------+
| **Byte 2-N** | **Payload/Arguments** | Contains the data specific to the command (e.g., RGB values, program timing). | ``0xFF 0x00 0x00`` (Red)  |
+-------------+-------------------------------------------------------------+---------------------------+---------------------------+
| **Byte N+1** | **Checksum/CRC (Optional)** | Simple XOR or CRC check for packet integrity. | TBD                       |
+-------------+-------------------------------------------------------------+---------------------------+---------------------------+

1.2. Decoded Commands (Work in Progress)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This table will be populated with observed hex payloads and their decoded meaning, correlating the action observed on the METIS mobile app with the packet sniffed in Wireshark.

*To decode, we need the raw hex payload captured when a known action is executed (e.g., tapping 'Red' on the app).*

+------------------------+--------------------------+----------+-------------------------------------------------------------------+
| Action (App Event)     | Observed Hex Payload (UUID 0002) | Length   | Decoded Meaning                                                   |
+========================+==========================+==========+===================================================================+
| **Set Color: RED** | **PLACEHOLDER DATA** | TBD      | Command ID X, Target ALL, Color R:255, G:0, B:0                   |
+------------------------+--------------------------+----------+-------------------------------------------------------------------+
| **Set Color: BLUE** | **PLACEHOLDER DATA** | TBD      | Command ID X, Target ALL, Color R:0, G:0, B:255                   |
+------------------------+--------------------------+----------+-------------------------------------------------------------------+
| **Request Status** | **PLACEHOLDER DATA** | TBD      | Command ID Y, Requests Battery/Sensor Status                      |
+------------------------+--------------------------+----------+-------------------------------------------------------------------+

2. ATT Notification Channel Structure (UUID 6e40...0003)
--------------------------------------------------------

The Notification Channel is used by the METIS light (Peripheral) to send asynchronous status updates and trigger events to the Host (Central). The Host must be subscribed (Notify enabled) to receive these.

2.1. Proposed Event Packet Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------+-------------------------------------------------------------+---------------------------------------------------------+
| Field (Bytes) | Role/Function                                               | Hypothesis                                              |
+=============+=============================================================+=========================================================+
| **Byte 0** | **Event ID** | Identifies the type of event (e.g., ``0x10`` for 'Touch Detected'). |
+-------------+-------------------------------------------------------------+---------------------------------------------------------+
| **Byte 1** | **Source Device ID** | Identifies which light in the network generated the event (e.g., ``0x01`` for $react-1-$). |
+-------------+-------------------------------------------------------------+---------------------------------------------------------+
| **Byte 2-N** | **Event Data** | Additional data (e.g., sensor pressure value, new battery level). |
+-------------+-------------------------------------------------------------+---------------------------------------------------------+

2.2. Decoded Events (Work in Progress)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------------+--------------------------+----------+---------------------------------------------------+
| Event (Observed)       | Observed Hex Payload (UUID 0003) | Length   | Decoded Meaning                                   |
+========================+==========================+==========+===================================================+
| **Sensor Touch** | **PLACEHOLDER DATA** | TBD      | Event ID X, Source Y, Touch confirmed.            |
+------------------------+--------------------------+----------+---------------------------------------------------+
| **Battery Level** | **PLACEHOLDER DATA** | TBD      | Event ID Z, Current battery percentage: N%.       |
+------------------------+--------------------------+----------+---------------------------------------------------+