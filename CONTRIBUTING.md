Contributing to Metis Forza
Thank you for your interest in contributing to Metis Forza! This library is designed to simplify the integration of Metis BLE devices into Python projects, ensuring high performance and ease of use.

By following these guidelines, you help maintain a clean, readable, and sustainable codebase.

🛠 Development Standards
This project strictly follows Python community standards to ensure maximum compatibility and maintainability.

1. Naming Convention (PEP 8)
Packages and Modules: All lowercase, with underscores if necessary (e.g., metis_forza).

Classes: PascalCase (e.g., MetisClient, MetisManager).

Functions and Variables: snake_case (e.g., init_drill(), reaction_time).

Constants: All uppercase (e.g., CMD_HANDLE).

2. Package Structure
All core logic must reside within the metis_forza/ directory.

client.py: Low-level logic and single-device management.

manager.py: High-level logic for multi-device coordination.

__init__.py: Exposure of public classes and enums.

3. Asynchronous Management
The library is built on asyncio and bleak. Every new feature must be non-blocking. Avoid using time.sleep(); always prefer await asyncio.sleep().

🏗 Development Setup
To start developing:

Clone the repository:

Bash

git clone https://github.com/your-username/metis-forza.git
cd metis-forza
Install dependencies:

Bash

pip install bleak
Install the package in editable mode:

Bash

pip install -e .
🚀 Contribution Workflow
Open an Issue: Before making significant changes, please open an issue to discuss your proposal.

Create a Branch: Use descriptive names like feature/new-handle-logic or fix/keep-alive-timeout.

Write the Code: Ensure your code adheres to the correct GATT handles:

0x0003: System commands and Keep-alive (ping).

0x0005: Data notifications (MDR/Impact data).

0x0006: Drill Initialization (Opcode 0x02).

Test Your Changes: If you don't have the hardware available, please validate the bitmask logic and async flow.

Submit a Pull Request: Clearly describe what you changed and why.

📋 Protocol & Handle Notes
When modifying BLE communications, keep the Metis protocol logic in mind:

Init Bitmask: The 0x02 command (sent to handle 0x0006) must always have Bit 0 set to 1.

Sound Feedback: Remember that the sound bit logic is inverted (1 = Mute, 0 = Sound ON).

Keep-Alive: The device requires a 0x20 ping every 3-5 seconds on handle 0x0003 to prevent connection timeout.

📞 Support
If you have questions regarding the project structure or the BLE protocol, please contact the maintainer or open a discussion in the repository.

Stay alert, stay safe!
