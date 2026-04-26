# Voxel Art Model Gun Disassembly/Assembly Simulator

This project aims to create a simple voxel-based gun simulator where users can disassemble and reassemble a gun model.

## Task Description

Create a voxel art model gun disassembly/assembly simulator. The program should allow users to load a voxel-based gun model, disassemble it into parts, and reassemble it. Use a simple voxel representation (e.g., 3D array of colors). Implement basic controls: select part, move, rotate, attach/detach. Provide a text-based or simple GUI interface (e.g., using Python with curses or a lightweight library like pygame). Include sample voxel data for a simple gun (e.g., a pistol with barrel, slide, frame, magazine). The code should be well-structured, modular, and include comments explaining the voxel gun simulator logic.

## Preparation Steps

1. **Set up Kilo Code CLI for Qwen model**
   ```bash
   kilo config set provider qwen-code
   kilo config set model qwen-coder-plus
   ```

2. **Set up Kilo Code CLI for Kimi K2.6 model**
   ```bash
   kilo config set provider openai-compatible  # or kimi-coding if available
   kilo config set base_url https://api.moonshot.ai/v1  # example, adjust as needed
   kilo config set model kimi-k2.6
   kilo config set api_key YOUR_KIMI_API_KEY
   ```

3. **Run the coding task**
   ```bash
   kilo run --auto "voxel_task.txt"
   ```

   Or specify output file:
   ```bash
   kilo run --auto "Read voxel_task.txt and implement the simulator in Python, saving to voxel_gun.py"
   ```

4. **Using Agent Swarm (Kimi K2.6 feature)**
   - Kimi K2.6 supports up to 300 sub-agents for complex tasks.
   - In Kilo Code, you can leverage this by providing a prompt that encourages decomposition.
   - Example: "Break down the voxel gun simulator into modules: voxel representation, gun model, disassembly logic, assembly logic, user interface, and main loop. Implement each module and integrate."

## Files

- `voxel_task.txt`: The original task prompt.
- `voxel_gun.py`: Expected output implementation (to be generated).
- `run_qwen.sh`: Script to run with Qwen model.
- `run_kimi.sh`: Script to run with Kimi K2.6 model.

## Notes

- Ensure you have API keys for the respective providers.
- The Kilo Gateway must be running for model access.
- For Kimi K2.6, you may need to use the OpenAI-compatible endpoint with the appropriate base URL and model ID.