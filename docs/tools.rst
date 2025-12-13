.. _tools:

Tools
==========================================
- `nRF Util <https://www.nordicsemi.com/Products/Development-tools/nRF-Util>`_

- `Wireshark <https://www.wireshark.org/>`_

- `Hardware <https://it.aliexpress.com/item/1005009621898979.html>`_


How to sniff
============
.. _1. Set the correct probe:

.. image:: _static/Howto_0.jpg
   :alt: BLE Sniff Device
   :align: center
   :width: 75%
   
.. _2. Choose the correct MAC:

.. image:: _static/HowTo_1.jpg
   :alt: Set the correct MAC
   :align: center
   :width: 50%
   
.. _3. Start sniffing (Play):

.. image:: _static/HowTo_2.jpg
   :alt: Play
   :align: center
   :width: 100%

.. _4. Filter by:
- :kbd: `_ws.col.protocol == "ATT"`
- :kbd: `frame contains "re"`
-