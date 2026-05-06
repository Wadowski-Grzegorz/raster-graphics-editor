# Custom 2D Raster Graphics Editor with Low-Level Pixel Manipulation
A Python-based digital painting application featuring custom pixel-level processing. 
The project implements manually developed drawing tools, layer compositing, and direct image buffer manipulation.
It demonstrates a layered GUI-Controller-Core architecture with event-driven communication.

Supports layer-based editing, brush-based drawing, and basic image transformations.

## Demo
The demo presenting:
- Importing an external image into the application
- Converting a layer type and changing their order
- Operations on layers using tools with adjustable brushes
- Saving work as a PNG file

https://github.com/user-attachments/assets/fa775903-d319-4434-ac50-9c9eee54f57f


## System Architecture
<diagram><img width="1546" height="716" alt="Group 5" src="https://github.com/user-attachments/assets/1fd18cf4-60fa-459e-8aea-8d94ea438708" />

The application is structured using a layered GUI-Controller-Core architecture, enabling separation of concerns between user interaction and business logic.
The Application Runtime State is managed within the Core layer as well as pixel-level processing.
The GUI handles user interaction and communicates with the Core through the Controller. It is updated based on events via an event manager implementing an observer pattern.

## Communication (Event System)
The application uses an event-driven communication model based on two complementary mechanisms:
- **GUI events (signals and slots)**

   Used for handling user interactions generated within the GUI layer. These events are mapped to application-level commands and forwarded to the Core via the Controller. The same mechanism is also used for communication between GUI components.
- **EventManager (publish-subscribe)**

   Communication within the Core, as well as from Core to GUI, is handled by an EventManager class following publish-subscribe pattern, where:
   - Core components emit events describing state changes or performed actions
   - Components in both Core and GUI layers subscribe to selected events and react accordingly
   - The GUI layer does not access Core objects directly, but updates its state based on emitted events

This division of communication mechanisms ensures a clear separation between layers and maintains loose coupling across the system.


## Layer System
Managing image data within the application is handled by the Layer System, which provides a structured model for storing, modifying, and organizing layer state.

<diagram><img width="981" height="735" alt="Group 8" src="https://github.com/user-attachments/assets/ad6aafb1-d23d-4244-b5cf-e9c7011ec458" />

The model is divided into two main implementations:
- RasterLayer, which allows direct modification of a pixel buffer, enabling irreversible image editing operations.
- LosslessLayer, which preserves the original image data and applies transformations in a non-destructive manner by maintaining a separate transformed state.

Both layer types inherit from  a common Layer class, ensuring a consistent interface and unified handling across the system. 
Layers can be created either as empty layers or by importing external images.
All state management and processing of layers are handled within the Core layer. The GUI accesses layer data through DTOs, which are used for rendering and user interaction.


## Brush System
Brushes define how pixels are selected for tool operations and the intensity of their influence. 
Each brush is defined by a geometric shape and a set of parameters that determine the intensity of pixel modifications, such as opacity and flow, which can be adjusted in real-time through the GUI.
A brush does not modify layer data on its own. Independent from tools, brushes can be reused across multiple tool implementations, enabling modular approach.


## Tool System
The Tool System is responsible for executing user-driven operations on layer data or on how they are presented to the user, depending on the tool type. It defines how user input is interpreted and translated into modifications applied to layer data. 

Tools handle interaction events such as press, move and release. Each tool encapsulates a specific type of behavior (e.g. drawing, transforming, resizing).
Tools cooperate with the Brush System, which defines how pixels are selected and influenced during tool execution. A brush object in Brush System is not a tool itself but a separate component.

Tools are divided into two categories: CoreTool and GuiTool. CoreTool instances operate directly on layer data and modify its state, while GuiTool instances affect only the visual representation of layers in the user interface. 
Both classes inherit from a common base Tool class to ensure a consistent interface across the system.


## Rendering
Rendering of layer content is performed by the Canvas in the GUI layer, which visualizes the current application state. When events indicating changes in layers occur, the Canvas updates its visualization accordingly. 

Layers are composited according to their order, visibility, position and scale.
The rendering mechanism operates on DTO representations of layers and does not access Core data directly.

To maintain performance, redraws are rate-limited.

## Image Processing Implementation
User, by using a tool, can edit how a layer is displayed or its content. Mouse input containing the position on the Canvas is provided to tools via events, which trigger corresponding operations on the active tool.

Image processing is implemented in a low-level manner through direct manipulation of raster buffers. Tools operate on pixel buffers, applying modifications based on user input without relying on high-level image editing frameworks.

These operations depend on the type of interaction and are applied to pixel regions defined by the active brush. The brush also determines the intensity of the effect.
Operations are first executed on a temporary layer, which is also used as a preview. The temporary layer is then committed to the target layer by directly modifying or blending the existing pixel data using separate custom logic for RGB and alpha channels.

Some tools operate on full layer buffers and use external image processing utilities for geometric transformations. The resulting image is then manually written back to the layer by replacing its internal buffer.
In cases where a temporary layer is used, only the overlapping region between the temporary layer and the current layer is processed and transferred. This is required because layers may differ in size and position within the canvas space.


## Setup and Run
**Requirements**
- Python 3.11+
- PyQt6
- numpy
- opencv-python

**Install**
```bash
pip install -r requirements.txt
```

**Run**
```bash
python main.py
```
