## 18.01.1 (2018-01-05)

- [solvers] Fix for missing omegaWallFunction in the boundary conditions for simpleFoam.

## 18.01.0 (2018-01-01)

- Fixed dependencies for the package.

## 17.12.0 (2017-12-14)

- [solvers] Updated boundary types model.
- [schemes, solvers] Simple and expert view for discretization schemes.
- [turbulence] Start of the implementation for better turbulence fields.
- [Shared, solvers] Improved turbulence model treatment.
- [FoamResults] Addition of paraview option for results visualization in a seperate thread.
- [snappyHexMesh, simpleFoam] Fixes for renaming boundary names.
- [simpleFoam] Option to rename functionObjects.
- [simpleFoam] Addition of the postProcess utitlity after simpleFoam task to calculate mag(U) instead of calculation in vtk.
- [FoamResults] Addition of statistics, bounds information and loading button for results.
- [snappyHexMesh] Multiple fixes for refinement objects and additional functions for surface refinement for refinement object.
- [simpleFoam] Added working MRFZone selection.
- [solvers] Better convection scheme selection.
- [simpleFoam] Added automatic update of controlDict during run time.
- [solvers] Added more controls for runView (Relaxation Factory, Write controls, ...).
- [snappyHexMesh] Added multiple refinementObjects.
- [simpleFoam] Added `slip` boundary condition.
- [all] Port to new DiceComponents in DICE.
- [all] Refactoring of multiple qml components.
- [build] Fixed build dependencies on linux and windows.
