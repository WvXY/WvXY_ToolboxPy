# wXyEngine

## Description
A tiny 2D game engine written in Python using Moderngl

It derives from my master thesis project.
It is currently under development and not ready for use.
I will add more functions as my project progresses.

## Structure

this engine is structured following JoltPhysics engine structure


The engine is divided into several modules:
- **Geometry**: contains the geometry classes of the engine
- **Physics**: contains the physics classes of the engine
- **Rendering**: contains the rendering classes of the engine



## Installation (Conda Environment)
```bash
conda create -n wXyEnginEnv python=3.11 
conda activate floorplan-conda
pip install imgui moderngl moderngl-window
conda install pytorch torchvision torchaudio pytorch-cuda>=12.1 -c pytorch -c nvidia
```

## TODO
- [ ] Add a proper README.md
- [ ] Rename class and submodule names to be more consistent
- [ ] Use only PyTorch

## References
- https://youtu.be/Y9U9IE0gVHA?si=kwfcpUtY0MACyFwI
- https://github.com/jrouwe/JoltPhysics/tree/master/Jolt
