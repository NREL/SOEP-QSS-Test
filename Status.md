# QSS Solver Test Repository Status Dashboard

## General

### OCT Version

Unless otherwise indicated the findings below are based on this OCT version: 2020.1-1.18 with the OCT-stable-r19089_JM-r14295 update.

### Buildings Library Version

The contained models and notes should be valid with the Buildings Library repository from Tue May 4 2021 with hash 9c37781c84 (9c37781c84e1f72f557ffdb150fe08f174b3682e).
* Some models pull an earlier Buildings Library revision to run against.
* Automatic configuration of the Buildings Library revision when building FMUs is planned but not yet implemented.

### Main Issues

Currently the main issues with OCT+QSS simulations are:
* Derivatives for some Buildings models are sensitive to the standard QSS approach of propagating somewhat "stale" quantized trajectories ([#1](https://github.com/NREL/SOEP-QSS-Test/issues/1))
* Directional Derivatives ([#2](https://github.com/NREL/SOEP-QSS-Test/issues/2)):
  * Directional derivatives have proven important to the QSS+FMU zero-crossing protocol and could be used to provide state variable 2nd derivatives if efficiency obstacles are overcome
  * Directional derivative support doesn't work with PyFMI and/or QSS for some models, failing during FMU initialization or causing very slow PyFMI and QSS progress
* Event Indicators ([#3](https://github.com/NREL/SOEP-QSS-Test/issues/3)):
  * Surprisingly many event indicators are generated for some models (Guideline36, Guideline36Spring)
  * Event indicators missing all reverse dependencies (UpstreamSampler)
  * Event indicators aren't working correctly in some models
  * Extra event indicators (EventIndicator5)
  * Event indicator reverse dependency refinements (BouncingBall, EventIndicator2)
* Numerical differentiation can inject significant noise into QSS derivatives (worse with QSS3 than QSS2) causing excess requantizations and simulation inaccuracy
  * Automatic optimal ND step selection is under development and will help with this but since a uniform step is needed for efficiency it can't be optimal for all variables
* Buildings library changes can alter or remove models making stable testing challenging
* An OCT mechanism to tell the FMU compiler to treat specified (non-state) local variables as output variables would allow QSS to avoid a very inefficient process for getting those outputs
* OCT gives warnings when building FMUs for many of Buildings models that should probably be reviewed and addressed

GitHub Issues for these are pending.

## Models

### Achilles: Simple 2-State System
* No problems

### Achilles1: Part 1 of Split/Connected Achilles
* No problems

### Achilles1-2: Multiple-FMU Demo
* No problems

### Achilles2: Part 2 of Split/Connected Achilles
* No problems

### ASHRAE2006
* Directional derivative support breaks PyFMI
  * CVode: Simulation failed: The right-hand side function had repeated recoverable errors
* The PyFMI run gives warnings including out of bounds
* The QSS runs drift off track without a small dtMax and show self-observer derivative sensitivity: Under investigation

### BouncingBall
* The event indicator reverse dependency on der(v) and der(h) works but causes extra requantizations of h when observer update would suffice
* QSS3 takes very large steps between bounces as expected since the height in quadratic in time
  * The default --zMul and --dtZMax options suffice with directional derivative support to give accurate/robust zero-crossing detection

### Case600
* OCT is currently generating many event indicators with no reverse dependencies
* The room temperature variable, TRooAir.T, is not set up in the FMU as an output variable so QSS runs must use the inefficient local output support
* The simulation has almost no zero-crossing events
* Some event indicators have very large magnitudes (1e60 and DBL_MAX) that are problematic wrt overflows
  * It would be good if this and other affected models can be revised to avoid such event indicators
  * The numerical differentiation formulas were revised to avoid overflow but this still requires building with the slower "precise" floating point model to avoid overflows
    * Do we need to keep this safety net in production?
    * Or just detect/report magnitude issues and overflows?
* QSS3 runs are very slow, at least partially due to these event indicator magnitudes giving very large ND 3rd derivatives and thus tiny QSS steps

### Case600FF
* Deactivation (--dtInf) control is needed for some of the QSS runs due to deactivation of the roo.air.vol.dynBal.mXi[1] variable that has no observers other than itself
* Earlier QSS runs started generating large second derivatives at ~400000 s, causing progress to stall
* Runs with the latest OCT and QSS will be performed soon

### CoupledSystem: Simple 3-State Model
* No problems

### DataCenterContinuousTimeControl
* Directional derivative support causes the PyFMI and QSS runs to abort during initialization with no error message
* The QSS runs (without directional derivative based event indicators) track fairly well but display some noise/slowness
* The time range starts at a large value which causes some small steps to be non-advancing in PyFMI simulations ("t + h = t on the next step")

### DataCenterDiscreteTimeControl
* Directional derivative support causes the PyFMI and QSS runs to abort during initialization with no error message
* The QSS runs (without directional derivative based event indicators) track fairly well but display some noise/slowness
* The time range starts at a large value which causes some small steps to be non-advancing in PyFMI simulations ("t + h = t on the next step")

### EventIndicator1: Event Indicator Feature Test
* With exact math QSS2 and QSS3 wouldn't do any requantizations since the state trajectory is linear between zero-crossing events and in these runs the numerical derivatives are accurate enough for no requantizations to occur
* QSS zero crossing success for this model is sensitive to the dtND numerical differentiation time step
* With a earlier run the zero-crossing protocol could fail with the FMU indicating a zero crossing was detected but not flipping the discrete variable (and thus the derivative): Unclear what was going on in the FMU that could allow this: Needs investigation

### EventIndicator2: Event Indicator Feature Test
* The OCT event indicator reverse dependency is on der(x) but it would be clearer if it were on x and in the future QSS could exploit that distinction for better efficiency
* QSS run event indicator requantizations are reduced using QSS options to avoid having them unnecessarily dominate the run times
* Due to numerical differentiation noise QSS3 does not achieve the target accuracy without a much tighter tolerance

### EventIndicator3: Event Indicator Feature Test
* With exact math QSS2 and QSS3 wouldn't do any requantizations since the state trajectory is linear between zero-crossing events and in these runs the numerical derivatives are accurate enough for no requantizations to occur
* QSS zero crossing success for this model is sensitive to the numerical differentiation time step
* The QSS+FMU zero crossing coordination was not working in some cases: Needs investigation: Might be better now with new controls
* With a earlier run the zero-crossing protocol could fail with the FMU indicating a zero crossing was detected but not flipping the discrete variable (and thus the derivative): Unclear what was going on in the FMU that could allow this: Needs investigation

### EventIndicator4: Event Indicator Feature Test
* The zero-crossing functions are a sinusoid that crosses zero (rather than functions that "bounce" off zero) to check that the QSS+FMU zero-crossing approach works in this (easier) case
* The sinusoids cause deactivation issues so the --dtInf and --dtMax controls are used

### EventIndicator5: Event Indicator Feature Test
* OCT generates 4 event indicators for the 2 sampler clauses, 2 of which move between -.2 and -.1, never reaching zero
  * Eliminating those extra event indicators will improve QSS efficiency
* The QSS+FMU zero crossing coordination was not working in some cases: Needs investigation: Might be better now with new controls
* The event indicator requantizations are triggered by discontinuities at the sample times that cause large numerical derivatives
* The QSS3 run is sensitive to the numerical differentiation time step to get the zero-crossings detected

### FloorOpenLoop
* This model has been removed from the Buildings library and is not yet set up to run from an earlier Buildings revision
* OCT builds this model on Windows but it fails at PyFMI run time with an "Initialization failed" error (after a number of warnings)

### Guideline36
* PyFMI runs of OCT FMU built with generate_ode_jacobian progress very slowly
* The FMU has a large number of event indicators with many dependencies
* QSS runs progress slowly: At least partly due to the event indicators: Needs investigation

### Guideline36Spring
* PyFMI runs of OCT FMU built with generate_ode_jacobian progress very slowly
* The FMU has a large number of event indicators with many dependencies
* QSS runs progress slowly: At least partly due to the event indicators: Needs investigation

### HeatingCoolingHotWater3Clusters
* The QSS2 run matches well but is slower than CVode (without tolerance matching or binning)

### HeatingCoolingHotWaterSmall
* The QSS2 run matches well but is slower than CVode (without tolerance matching or binning)

### InputFunction: 1-State System with Input Function Derivative
* No problems

### IntegratorWithLimiter
* No problems

### mLIQSS_1: 2-State System from Improving LIQSS Paper
* No problems

### Observers: Scalable Non-Sparse Observer Graph System
* No problems

### OnOffController: Simple Room + Controller System
* This model is adapted for local use from the OnOffController model in https://github.com/lbl-srg/soep/tree/master/models/modelica_for_qss/QSS/Specific/Events
* The adapted model built with OCT is not running correctly with PyFMI or QSS: The FMU is not detecting zero crossings: Possible OCT issue
* The original model built with Dymola runs corrctly with PyFMI and QSS with QSS capturing the zero crossings more accurately
* Needs "observer" QSS outputs to show the temperature accurately (without sampled outputs) since it depends only on conQSS.y and so doesn't requantize often

### PID_Controller: Modelica PID Controller Example
* QSS runs are sensitive to the numerical differentiation time step

### Quadratic: Simple 1-State System with Quadratic Trajectory
* No problems

### SimpleHouse
* The OCT FMU built with the generate_ode_jacobian option aborts under PyFMI and QSS during initialization with no error message
* Without directional derivatives the QSS simulations run very slowly due to excessive requantizations caused by event indicator numerical differentiation noise
* Despite the noise without directional derivatives runs with binning are competitive with CVode for the same accuracy, largely because the zero crossings are more accurate

### SimpleHouseDiscreteTime
* This model is a variant of SimpleHouse with a discrete time controller for which QSS is more advantageous
* This model was removed from the Buildings library and is set up to clone a specific revision of the Buildings library: it would be better to update it and re-add it to the library
* The OCT FMU built with the generate_ode_jacobian option aborts under PyFMI and QSS during initialization with no error message
* The normal and "reference" PyFMI (CVode) runs do not have the same zero crossing behavior so the model is not very numerically stable
* The QSS simulation accuracy is hurt by numeric differentiation and the lack of directional derivatives such that zero-crossing events can be missed: This may be better with the new zero-crossing controls
* Some variables of interest are (non-state) local FMU variables that require a very inefficient process to extract from a QSS run (due to the lack of dependency information)

### sinusoid: Simple System with Fast and Slow Dynamics
* No problems

### sinusoidZ: Event Indicator Torture Test
* This model is a zero-crossing "torture test" with a high-frequency sinusoidal zero-crossing function and difficult "touch" crossings
* This was used to help design the dtZMax control that inserts a requantization close before a predicted zero crossing as needed to assure an accurate crossing time
* Depending on how close to a true one-point "touch" the zero crossings are PyFMI won't detect some crossings: This is not a flaw but the designed tolerance behavior
* QSS3 has more difficulty with this model than QSS2 due to numerical differentiation noise

### StateEvent6: 3-State Model With Conditional
* The QSS2 runs use the --dtInf control to avoid deactivation at startup due to the second derivative of x1 being sine(Constant*time)

### TwoFloor_TwoZone
* Standard QSS shows derivative sensitivity of some self-observer variables causing solution noise/drift
  * The experimental QSS variant that propagates the current continuous trajectory improves the behavior but drift still occurs
  * Under investigation

### UpstreamSampler: Simple Sampler for Event Indicator Feature
* The OCT-generated FMU event indicators have no reverse dependencies so QSS cannot simulate it correctly

### ZCBoolean2: Simple 1-State System with Conditional
* The QSS2 runs use the --dtInf control to avoid deactivation of u=sin(t) at startup (where its 2nd derivative is zero)
* The QSS2 runs use a larger-than-default --zMul control for zero crossing detection
