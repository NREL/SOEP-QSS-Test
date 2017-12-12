# SOEP-QSS-Test: QSS Solver Test Model Library

This is a library of test models and results for development of the JModelica QSS solver being developed as part of the "Spawn of EnergyPlus" project.
The library serves these purposes:
* Regresssion testing
* Results comparisons *vs* Dymola, JModelica, and Ptolemy
* Performance testing

Most models will be run as FMUs since the QSS solver is being built for integration into JModelica via the FMU interface.
Some simpler models may also be run as QSS "code-defined" models for results and performance comparison.

## Organization

The top-level repository directory contains these subdirectories:
```
  bin/
  mdl/
```

The `bin` directory contains scripts used in modeling.

The `mdl` directory contains the models and results with this (tentative) organization for each model:
```
ModelName/
  ModelName.txt     Notes
  ModelName.mo      Modelica file
  ModelName.fmu     FMU file
  Dymola/           Dymola model & results
  JModelica/        JModelica model & results
  Ptolemy/          Ptolemy model & results
  QSS/              QSS model & results
  out/              Comparison results between tools
```

Modeling tool and `out` sub-directories names may have .*RunType* suffixes that indicate the run variation in use, such as time span and tolerances or minor changes to the model structure. This can create large directory trees and complicates comparison between results so should be used with restraint.

Each modeling tool sub-directory has this structure:
```
ModelingTool/
  ModelName.txt                 Notes
  ModelName.mo                  Modelica file
  ModelName.fmu                 FMU file
  modelDescription.orig.xml     Original XML
  modelDescription.xml          Modified XML
  out/                          Results
```

### Notes

* The modeling tool directories may contain:
  * Custom versions of the .mo file
  * Custom versions of the .fmu file
* This repository may become large due to the size of results and comparisons. Since history isn't critical the repository may be reinitialized occasionally to control its size.

What about variations on a model? Allow small changes under the same ModelName directory

Results comparisons between modeling tools: `ModelName/out/ModelName.Tool1.Tool2.cmp`

## Models

## Tools

Notes on each of the modeling tools appear below.

### QSS

* The FMI/FMIL APIs do not currently expose full if/when conditional block information so QSS must be conservative and process all potential conditional events, which is inefficient.
* The FMI/FMIL APIs do not provide a mechanism to tell the FMU to process a conditional event at a specific time, so QSS advances the relevant variables a small time step beyond the potential conditional event in the hope that the FMU will then detect and process the event if an event actually occurs at that time. This is not robust: until a better mechanism is available it is possible for QSS solutions to miss some conditional events.

### Dymola

* Dymola FMUs have twice as many event indicators as expected. The QSS solver FMU simulation accounts for this when checking Dymola-generated FMUs.

### JModelica

* FMI/FMIL API extensions to better support QSS solvers are under development.

### Ptolemy
