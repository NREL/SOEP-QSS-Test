# QSS Solver Test Repository Status Dashboard

## General

### OCT Version

Unless otherwise indicated the findings below are based on this OCT version: 2020.1-1.18 with the OCT-r28312_JM-r14295 update.

#### OCT Update OCT-master-7245bce03ab2ebdfdaaf0805d75209efaa009c67

1. Previously missing dependencies in [DepTest5](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/DepTest5) are now present but some unneeded dependencies are present ([#26](https://github.com/NREL/SOEP-QSS-Test/issues/26#issuecomment-1279827972)).

#### OCT Update OCT-r28312_JM-r14295

Summary of some changes observed and not yet explained/addressed:
1. The [ACControl10](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/ACControl10) model (with all the when blocks) now builds and runs correctly with PyFMI but has issues for QSS (described below).
2. The [TwoFloor_TwoZone](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/TwoFloor_TwoZone) CVode run now aborts if the FMU is built with generate_ode_jacobian but during simulation, not initialization. It gives the message "Simulation failed: 'The right-hand side function had repeated recoverable errors. At time 188479.249406.'"

### Buildings Library Version

The contained models and notes should be valid with the Buildings Library repository from Tue May 4 2021 with hash 9c37781 (9c37781c84e1f72f557ffdb150fe08f174b3682e).
* Some models pull an earlier Buildings Library revision to run against.
* Automatic configuration of the Buildings Library revision when building FMUs is planned but not yet implemented.
* Regression testing support has been extended with YAML report files from comparison runs and a script to compare these results between runs.

### Building and Running Models

Unless otherwise noted here or in a GitHub Issue the models can be run as described in the README and below.

Notes:
* Some scripts in `bin` import Python packages not included in most distributions: they can be obtained via `pip`
* OCT on Windows uses its own Python environment so scripts that depend on particular Python packages may not work from a console configured for OCT

#### Building FMUs with OCT
* Run the `set_OCT` script in `bin` (or a custom version adapted for your system) in a console:
  * Linux: `source bin/set_OCT`
  * Windows: `bin\set_OCT.bat`
* From the `OCT` subdirectory of the model's directory under `mdl` you normally run `bld`, which will run the custom `bld.py` build script in that `OCT` directory or, if not present, the default `bld.py` script in `bin`.
  * To see the options for building the FMU you can run `bld --help`.
  * The default is to build the FMU with QSS support, which enables event indicator variables and directional derivative support (used only for the event indicators currently)
    * Some models don't currently work with the directional derivative support included with the QSS options, in which case the custom `bld.py` will use the `--no-dd` option
    * Earlier QSS versions could run without directional derivative support but zero-crossing accuracy/reliability was degraded
    * The current QSS version that uses the new Dependencies section drops support for simulation without directional derivatives
  * To get a "normal" FMU you can use the `--no-qss` option or its equivalent `--pyfmi`
  * Some models/issues might require building the "normal" FMU for PyFMI runs and then building the FMU with QSS options for QSS runs

#### Running Models with PyFMI
* From a console configured with `set_OCT` and from the model's `OCT` directory or a subdirectory of it you can do the default PyFMI (CVode) simulation with the `run` command
* The `run` command can run a local custom `run.py` or default to the `run.py` in `bin`
* If there is a `run.py` in the model's `OCT` directory that is normally the best choice for a default run as it may have options needed/useful for that model
* The `run.py` scripts will call the `run_PyFMI.py` script in `bin` when under an `OCT` directory
* To see the supported PyFMI options use the command `run_PyFMI --help`
* Options allow the choice of solver, method order, tolerances, and outputs
* `run_PyFMI` generates separate two-column (time and value) ASCII output files for each variable
* If a model_name`.var` file is present in the model's root directory it is used as a filter to limit the variables PyFMI outputs

#### Running Models with QSS
* Get the latest QSS from https://github.com/NREL/SOEP-QSS and build it as described in its README
* Run the `set_QSS` script in `bin` (or a custom version adapted for your system) in a console configured for the QSS build:
  * Linux: `source bin/set_QSS`
  * Windows: `bin\set_QSS.bat`
* The `run` command can run a local custom `run.py` or default to the `run.py` in `bin`
* If there is a `run.py` in the model's `QSS` (sub)directory that is normally the best choice for a default run as it may have options needed/useful for that model
* The `run.py` scripts will call the `run_QSS.py` script in `bin` when under a `QSS` directory
* To see the `run_QSS` options use the command `run_QSS --help`
  * `run_QSS` also passes QSS options along to QSS
  * To see the QSS options run `QSS --help`
* `QSS` generates separate two-column (time and value) ASCII output files for each variable
* If a model_name`.var` file is present in the model's root directory it is used as a filter to limit the variables QSS outputs

#### Plotting Variable Output Signals
* There are various plotting tools that can handle the 2-column ASCII signal files
* ObjexxPlot handles these signals and can be provided by Objexx for Windows or Ubuntu upon request

### Main Issues

Currently the main issue categories with OCT+QSS simulations are:
1. Derivatives for some Buildings models are sensitive to the standard QSS approach of propagating somewhat "stale" quantized trajectories ([#1](https://github.com/NREL/SOEP-QSS-Test/issues/1))
2. Directional Derivatives:
   * Directional derivatives have proven important to the QSS+FMU zero-crossing protocol and could be used to provide state variable 2nd derivatives if efficiency obstacles are overcome
   * Directional derivative support doesn't work with PyFMI and/or QSS for some models, failing during FMU initialization or causing very slow PyFMI and QSS progress ([#2](https://github.com/NREL/SOEP-QSS-Test/issues/2))
3. Event Indicators:
   * Surprisingly many event indicators are generated for some models ([#12](https://github.com/NREL/SOEP-QSS-Test/issues/12))
   * Event indicator reverse dependency refinements ([BouncingBall](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/BouncingBall), [EventIndicator2](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/EventIndicator2))
4. Numerical differentiation can inject significant noise into QSS derivatives (worse with QSS3 than QSS2) causing excess requantizations and simulation inaccuracy ([#4](https://github.com/NREL/SOEP-QSS-Test/issues/4))
   * Automatic optimal ND step selection is under development and will help with this but since a uniform step is needed for efficiency it can't be optimal for all variables
5. Buildings Library issues ([#6](https://github.com/NREL/SOEP-QSS-Test/issues/6)):
   * Buildings library changes can alter or remove models making stable testing challenging
   * OCT gives warnings when building FMUs for many of Buildings models that should probably be reviewed and addressed

"Clearinghouse" Issues for some of these were created but items within these can also be tracked in separate Issues as needed.

## Models

### [ACControl10](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/ACControl10): 10-Room/AC Model from Paper
* Based on a model from the paper "On the Efficiency of Quantization–Based Integration Methods for Building Simulation" https://usuarios.fceia.unr.edu.ar/~kofman/files/buildings_qss.pdf
* Due to the issues noted here QSS cannot correctly simulate this model yet (other than by forcing frequent requantizations by using a small dtMax)
* Although the results don't match yet QSS does appear to significantly outperform CVode for this model as expected from the paper
* Once these issues are fixed larger models from the paper will be added and should show an even larger performance advantage for QSS
* The event indicators that depend on the `th[]` variables are missing those dependencies
* Because the when blocks are in the algorithms section they have mostly uniform dependencies that include dependencies from the sets of similar event indicators rather than just those for the specific event indicator. The unnecessary reverse dependencies are a performance/scalability problem. This has been added to issue [#10](https://github.com/NREL/SOEP-QSS-Test/issues/10).

### [Achilles](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Achilles): Simple 2-State System
* No problems

### [Achilles1-2](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Achilles1-2): Multiple-FMU Demo
* No problems

### [Achilles1](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Achilles1): Part 1 of Split/Connected Achilles
* No problems

### [Achilles2](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Achilles2): Part 2 of Split/Connected Achilles
* No problems

### [ASHRAE2006](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/ASHRAE2006)
* The PyFMI CVode run gives chattering warnings
* The QSS runs drift off track without a small dtMax and show self-observer derivative sensitivity: Under investigation
* The flo.cor.air.p_start variable start value/specs from the FMIL API calls and the modelDescription.xml file are inconsistent: Modelon is investigating
* The model has 173 der(.) variables, each showing a `derivative=` entry in the xml file but the FMIL API only shows 168 derivatives, which breaks the QSS simulation. These are the derivatives not included:
  - der(flo.cor.air.vol.dynBal.m)
  - der(flo.eas.air.vol.dynBal.m)
  - der(flo.nor.air.vol.dynBal.m)
  - der(flo.wes.air.vol.dynBal.m)
  - der(flo.portsWes[1].p)

### [BIDR](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/BIDR)
* Demo of the various uses of non-state variables that QSS must support and can better support using the `<Dependencies>` information
* Shows scenario where event indicator annotation distinguishing `if` from `when` blocks can help QSS performance

### [BouncingBall](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/BouncingBall)
* The event indicator reverse dependency on der(v) and der(h) works but causes extra requantizations of h when observer update would suffice
* QSS3 takes very large steps between bounces as expected since the height in quadratic in time
  * The default --zMul and --dtZMax options suffice with directional derivative support to give accurate/robust zero-crossing detection

### [Case600](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Case600)
* OCT is currently generating 5 event indicators with no reverse dependencies
* The room temperature variable, TRooAir.T, is not set up in the FMU as an output variable so QSS runs must use the inefficient local output support
* The simulation has almost no zero-crossing events
* Some event indicators have very large magnitudes (1e60 and DBL_MAX) that are problematic wrt overflows
  * It would be good if this and other affected models can be revised to avoid such event indicators
  * The numerical differentiation formulas were revised to avoid overflow but this still requires building with the slower "precise" floating point model to avoid overflows
    * Do we need to keep this safety net in production?
    * Or just detect/report magnitude issues and overflows?
* QSS3 runs are very slow, at least partially due to these event indicator magnitudes giving very large ND 3rd derivatives and thus tiny QSS steps

### [Case600FF](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Case600FF)
* Deactivation (--dtInf) control is needed for some of the QSS runs due to deactivation of the roo.air.vol.dynBal.mXi[1] variable that has no observers other than itself
* Earlier QSS runs started generating large second derivatives at ~400000 s, causing progress to stall
* Runs with the latest OCT and QSS will be performed soon

### [CoupledSystem](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/CoupledSystem): Simple 3-State Model
* No problems

### [DataCenterContinuousTimeControl](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/DataCenterContinuousTimeControl)
* Directional derivative support causes the PyFMI and QSS runs to abort during initialization with no error message
* The QSS runs (without directional derivative based event indicators) track fairly well but display some noise/slowness
* The time range starts at a large value which causes some small steps to be non-advancing in PyFMI simulations ("t + h = t on the next step")

### [DataCenterDiscreteTimeControl](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/DataCenterDiscreteTimeControl)
* Directional derivative support causes the PyFMI and QSS runs to abort during initialization with no error message
* The QSS runs (without directional derivative based event indicators) track fairly well but display some noise/slowness
* The time range starts at a large value which causes some small steps to be non-advancing in PyFMI simulations ("t + h = t on the next step")

### [DepTest](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/DepTest): QSS Dependency Issue Test
* Issue with QSS event indicator dependencies was resolved by moving when blocks from `algorithm` to `equation`

### [DepTest4](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/DepTest4): QSS Dependency Issue Test
* Demonstrates issues with QSS event indicator dependencies when using the `integer()` event-generating function

### [DepTest5](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/DepTest5): QSS Dependency Issue Test
* Demonstrates issues with missing event indicator dependencies

### [DepTest6](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/DepTest6): QSS Dependency Bypass Demo
* Demonstrates scenario of QSS performance hit from short-circuiting discrete variable from dependencies

### [DiscreteObserver](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/DiscreteObserver)
* No problems

### [EventIndicator1](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/EventIndicator1): Event Indicator Feature Test
* With exact math QSS2 and QSS3 wouldn't do any requantizations since the state trajectory is linear between zero-crossing events and in these runs the numerical derivatives are accurate enough for no requantizations to occur
* QSS zero crossing success for this model is sensitive to the dtND numerical differentiation time step
* With a earlier run the zero-crossing protocol could fail with the FMU indicating a zero crossing was detected but not flipping the discrete variable (and thus the derivative): Unclear what was going on in the FMU that could allow this: Needs investigation

### [EventIndicator2](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/EventIndicator2): Event Indicator Feature Test
* The OCT event indicator reverse dependency is on der(x) but it would be clearer if it were on x and in the future QSS could exploit that distinction for better efficiency
* QSS run event indicator requantizations are reduced using QSS options to avoid having them unnecessarily dominate the run times
* Due to numerical differentiation noise QSS3 does not achieve the target accuracy without a much tighter tolerance

### [EventIndicator3](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/EventIndicator3): Event Indicator Feature Test
* With exact math QSS2 and QSS3 wouldn't do any requantizations since the state trajectory is linear between zero-crossing events and in these runs the numerical derivatives are accurate enough for no requantizations to occur
* QSS zero crossing success for this model is sensitive to the numerical differentiation time step
* The QSS+FMU zero crossing coordination was not working in some cases: Needs investigation: Might be better now with new controls
* With a earlier run the zero-crossing protocol could fail with the FMU indicating a zero crossing was detected but not flipping the discrete variable (and thus the derivative): Unclear what was going on in the FMU that could allow this: Needs investigation

### [EventIndicator4](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/EventIndicator4): Event Indicator Feature Test
* The zero-crossing functions are a sinusoid that crosses zero (rather than functions that "bounce" off zero) to check that the QSS+FMU zero-crossing approach works in this (easier) case
* The sinusoids cause deactivation issues so the --dtInf control is used

### [EventIndicator5](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/EventIndicator5): Event Indicator Feature Test
* OCT generates 4 event indicators for the 2 sampler clauses, 2 of which move between -.2 and -.1, never reaching zero
  * Eliminating those extra event indicators will improve QSS efficiency
* The QSS+FMU zero crossing coordination was not working in some cases: Needs investigation: Might be better now with new controls
* The event indicator requantizations are triggered by discontinuities at the sample times that cause large numerical derivatives
* The QSS3 run is sensitive to the numerical differentiation time step to get the zero-crossings detected

### [FloorOpenLoop](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/FloorOpenLoop)
* This model has been removed from the Buildings library and is not yet set up to run from an earlier Buildings revision
* OCT builds this model on Windows but it fails at PyFMI run time with an "Initialization failed" error (after a number of warnings)

### [Guideline36](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Guideline36)
* The FMU has a large number of event indicators with many dependencies
* QSS runs progress slowly: At least partly due to the event indicators: Investigating
* The model has 176 der(.) variables only 171 are state derivatives: QSS needs updating to support this

### [Guideline36Spring](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Guideline36Spring)
* PyFMI runs of OCT FMU built with generate_ode_jacobian progress very slowly
* The FMU has a large number of event indicators with many dependencies
* QSS runs progress slowly: At least partly due to the event indicators: Needs investigation

### [HeatingCoolingHotWater3Clusters](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/HeatingCoolingHotWater3Clusters)
* The QSS2 run matches well but is slower than CVode (without tolerance matching or binning)

### [HeatingCoolingHotWaterSmall](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/HeatingCoolingHotWaterSmall)
* The QSS2 run matches well but is slower than CVode (without tolerance matching or binning)

### [InputFunction](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/InputFunction): 1-State System with Input Function Derivative
* No problems

### [IntegratorWithLimiter](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/IntegratorWithLimiter)
* No problems

### [mLIQSS_1](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/mLIQSS_1): 2-State System from Improving LIQSS Paper
* No problems

### [Observers](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Observers): Scalable Non-Sparse Observer Graph System
* No problems

### [OnOffController](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/OnOffController): Simple Room + Controller System
* This model is adapted for local use from the OnOffController model in https://github.com/lbl-srg/soep/tree/master/models/modelica_for_qss/QSS/Specific/Events
* The adapted model built with OCT is not running correctly with PyFMI or QSS: The FMU is not detecting zero crossings: Possible OCT issue
* The original model built with Dymola runs corrctly with PyFMI and QSS with QSS capturing the zero crossings more accurately
* Needs "observer" QSS outputs to show the temperature accurately (without sampled outputs) since it depends only on conQSS.y and so doesn't requantize often

### [PID_Controller](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/PID_Controller): Modelica PID Controller Example
* QSS runs are sensitive to the numerical differentiation time step and zero crossing bump multiplier

### [Quadratic](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/Quadratic): Simple 1-State System with Quadratic Trajectory
* No problems

### [SimpleHouse](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/SimpleHouse)
* The OCT FMU built with generate_ode_jacobian aborts under PyFMI and QSS during initialization with no error message
* Without directional derivatives the QSS simulations run very slowly due to excessive requantizations caused by event indicator numerical differentiation noise
* Despite the noise without directional derivatives runs with binning are competitive with CVode for the same accuracy, largely because the zero crossings are more accurate

### [SimpleHouseDiscreteTime](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/SimpleHouseDiscreteTime)
* This model is a variant of SimpleHouse with a discrete time controller for which QSS is more advantageous
* This model was removed from the Buildings library and is set up to clone a specific revision of the Buildings library: it would be better to update it and re-add it to the library
* The OCT FMU built with generate_ode_jacobian aborts under PyFMI and QSS during initialization with no error message
* The normal and "reference" PyFMI (CVode) runs do not have the same zero crossing behavior so the model is not very numerically stable
* The QSS simulation accuracy is hurt by numeric differentiation and the lack of directional derivatives such that zero-crossing events can be missed: This may be better with the new zero-crossing controls
* Some variables of interest are (non-state) local FMU variables that require a very inefficient process to extract from a QSS run (due to the lack of dependency information)

### [sinusoid](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/sinusoid): Simple System with Fast and Slow Dynamics
* No problems

### [sinusoidZ](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/sinusoidZ): Event Indicator Torture Test
* This model is a zero-crossing "torture test" with a high-frequency sinusoidal zero-crossing function and difficult "touch" crossings
* This was used to help design the dtZMax control that inserts a requantization close before a predicted zero crossing as needed to assure an accurate crossing time
* Depending on how close to a true one-point "touch" the zero crossings are PyFMI won't detect some crossings: This is not a flaw but the designed tolerance behavior

### [StateEvent6](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/StateEvent6): 3-State Model With Conditional
* The QSS2 runs use the --dtInf control to avoid deactivation at startup due to the second derivative of x1 being sine(Constant*time)

### [TimeTest](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/TimeTest)
* This model demonstrates a problem with short-circuiting discrete variables out of the dependencies
* This model has the same event indicator as ACControl10 but in this case the directional derivative of the time-based event indicator is correct

### [TimeTestCross](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/TimeTestCross)
* This model expands on TimeTest to demonstrate that it isn't sufficient to fix the discrete variable dependency short-circuiting issue for event indicator variables to do a QSS update after their own condition "handler" runs

### [TwoFloor_TwoZone](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/TwoFloor_TwoZone)
* The OCT-r23206_JM-r14295 FMU built with generate_ode_jacobian aborts in the PyFMI CVode run giving a number of errors before failing with: Evaluating the derivatives failed at <value name="t"> 1.1052023186606659E+005
* Standard QSS shows derivative sensitivity of some self-observer variables causing solution noise/drift
  * The experimental QSS variant that propagates the current continuous trajectory improves the behavior but drift still occurs
  * Under investigation
* The FMU built without any QSS options is almost 2x faster than the FMU built with QSS options except for generate_ode_jacobian so PyFMI may have a surprising overhead for the presence of event indicators.

### [UpstreamSampler](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/UpstreamSampler): Simple Sampler for Event Indicator Feature
* The OCT-generated FMU event indicators have no reverse dependencies so QSS cannot simulate it correctly

### [ZCBoolean2](https://github.com/NREL/SOEP-QSS-Test/tree/main/mdl/ZCBoolean2): Simple 1-State System with Conditional
* The QSS2 runs use the --dtInf control to avoid deactivation of u=sin(t) at startup (where its 2nd derivative is zero)
* The QSS2 runs use a larger-than-default --zMul control for zero crossing detection
