## Agenda: 2023/6/20
- Testing
  - Set up for Scalable model testing at different sizes.
  - Performance of Buildings models including Scalable are much improved with relaxation but not competitive with CVode (to varying degrees)
- Development.
  - Could explore multipoint smoothing to improve relaxation but it isn't trivial to combine with QSS.
  - Focusing on requantization "clustering" first to see if that can help with sensitivity. Trying self-dependency loops as the first idea.
  - Next will be directional second derivatives to enable QSS3 (larger steps).
- Papers of Interest
  - QSS researchers are writing about QSS modifications that show they are hitting models where it doesn't perform well also.
  - [Mixed–Mode State–Time Discretization in ODE Numerical Integration](https://www.researchgate.net/publication/340495790_Mixed-mode_state-time_discretization_in_ODE_numerical_integration): Combining LIQSS with CVode
    - "The proposed mixed–mode scheme consists of splitting an ODE, using QSS algorithms where they perform better than classic algorithms (i.e., in presence of frequent discontinuities or stiﬀness under certain particular sparse structures) and using classic algorithms where they are a better choice"
  - [DEVS Simulation of Marginally Stable Systems](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.61.5329&rep=rep1&type=pdf)

## Agenda: 2023/6/2
- Relaxation Development
  - Relaxed LIQSS2 (rLIQSS2)
    - Completed and tested a few variations including with and without $\ddot{x}$ relaxation
    - Performance is not as good as relaxed QSS2
    - Investigating stiffness structure to see if off-diagonal contributions are large in Buildings models
- Testing
  - Case600 and ASHRAE2006 relaxation trials and analysis run to look for candidates for additional performance gains
  - Seeing solution mis-tracking in ASHRAE2006 that may be due to sensitivity to the slightly stale trajectories of non-requantizing variables or possibly missing dependencies
- OCT
  - Time frame for OCT update with reinit/pre dependency support?
  - Ideas for non-event-generating operations (min/max/...) and calls within function (FunctionTest)?
- Next
  - rLIQSS2 variations/testing
  - Stiffness structure analysis to see if that explains rLIQSS2 performance
  - Guideline36 and scalable model testing with best rQSS2 variant
  - State $\ddot{x}$ directional derivatives development and [r]LI/QSS3 development exploiting this

## Agenda: 2023/5/22
- Development
  - Refined relaxed rQSS2 for performance: sensitivity detection and relaxation enabling, time step controls (inflection points, growth damping), $\ddot{x}$ relaxation, ...
  - Reenabled xQSS variants and added rxQSS2
  - Experimented with "convergence" controls to reduce steps once relaxation trajectory converges on precise trajectory: nothing clean enough that works well found yet: will give it more thought
- Testing
  - Case600
    - Comparing RMS-matched (QSS is more accurate with the same `rTol`) 1-day runs
    - Current rQSS2 and/or rxQSS2 are approaching 3X faster than stock QSS2 but still 4+X slower than CVode (ncp=0) runs
    - Hope to further reduce steps after trajectory "convergence"
    - Not large or sparse enough model for QSS to shine but can probably get to ~2X CVode speed after next phase
- Next
  - Complete rLIQSS2 and do basic performance comparison
  - Performance testing rQSS2 and rLIQSS2 on larger/scalable Buildings models to see where we are at
  - Revamp with state $\ddot{x}$ directional derivatives
    - Reduce QSS order dependencies
    - Reduce trajectory noise causing extra steps
    - Enable practical QSS3
    - Fairly involved change: will take at least a few days to complete
    - Test standard and relaxed QSS2 and QSS3
  - "Clustering" support to reduce QSS sensitivity and experiment with logic for automating minimal clustering
  - Performance:
    - Profiling/tuning
    - Parallelization
    - Output logic revamp to handle local variables (with or without dependencies) more efficiently
    - Option for full in-memory output buffering to minimize i/o during simulation
- OCT
  - Dependency problems in Issues that have no work-around and may impact Buildings model testing
    - reinit: https://github.com/NREL/SOEP-QSS-Test/issues/30#issuecomment-1536951802
    - `<Dependencies>` missing and short-circuited dependencies (include local variables)
      - Harvesting dependencies from `<ModelStructure>` as work-around
      - Can't experiment with "active" signaling variables that are short-circuited for update "firewalling"
  - Start value issues (email discussion)
  - Think about providing event indicator derivative variables so they track with states

## Agenda: 2023/5/3
- Relaxation:
  - Coordinated (geometric) $\dot{x}$ and $\ddot{x}$ relaxation can be done but is complex and expensive.
  - Experimented with a simple approach: inflection point time step shortening and damped time step lengthening. This doesn't require yo-yo detection and could be fast enough to leave on all the time in unified QSS variable types.
    - Inflection points can add more steps when not needed so may not be viable without yo-yo detection/enabling
    - Inflection point control seems to be needed to avoid near-zero steps: _e.g._, skip inflection point if time step would be < 1% of the natural QSS time step
  - Time step growth relaxation: Only apply if no inflection point used?
  - Experimented with $\ddot{x}$ relaxation: using half the QSS $\ddot{x}$ value (and keeping the QSS $\dot{x}$) has the trajectory hitting the halway point between the $x$ and $q$ trajectories at the next QSS time step, which is about where the precise trajectory typically sits when sensitive yo-yoing occurs. This is effective and allows longer steps during convergence to precise trajectory but still benefits from inflection point time step shortening. Given that it requires yo-yoing detection (and could give a bad trajectory if detection was wrong) sticking with time step only relaxation seems safer and probably more efficient overall.
  - Case600:
    - Time step + $\ddot{x}$ relaxation looks like a good approach for `dp`: start to get large time steps.
    - `T_degC` (self-dependent) still has high step count with this relaxation.
      - Suspect sensitivity to use of trajectory values from other non-requantizing observee variables.
      - Continuous (instead of quantized) trajectory propagation reduces sensitivity noise.
      - Fixed time step QSS runs (dtMin==dtMax==2) clean this up.
      - Concept of a requantization variable bin could be key. Needs to happen automatically and bins need to be minimal to avoid losing QSS sparsity benefits.
  - Impact of continuous trajectory propagation.
- Performance:
  - Assessment: Metrics _vs._ reference solution is tricky:
    - Same CVode and QSS tolerances don't give same solution accuracy so we need to tune the tolerance of one of them to compare time steps and run time.
    - Non-uniform time sampling of PyFMI (to prevent forcing extra integration points):
      - QSS runs can add sampling points without causing integration steps but we want a comparable metric.
      - Need very high sampling rate in reference solution or metric can be dominated by interpolation "error".
      - Need to measure "error" only at non-reference points to avoid large interpolation "errors" (simdiff --coarse).
      - Should we be weighting the diffs by the time step size for a uniform metric?
- Other:
  - Build system revamp: Drop `64` directory level, refine compiler options, ...
  - Linux (Ubuntu) testing/updates, build FMIL 2.4.1 and migrate
  - OpenMP experiments with new Clang-based Intel oneAPI C++

## Agenda: 2023/4/4
- Relaxation Development:
  - Time step based relaxation is workable and fairly efficient.
    - Derivative relaxation adds a lot of logic complexity/hueristics and overhead (I am still experimenting with this further to be sure).
  - Best approach so far uses a 3-level logic when relaxation is needed:
    1. Limit time step to the $x$ inflection ($\dot{x} == 0$ in QSS2) point if one is present at a positive step. In QSS2 this is also the point where the $x$ trajectory change from the requantization value is half the $q$ trajectory change.
    2. Otherwise limit the time step to the point where the $x$ derivative equals the estimated boundary derivative at the requantization point ($\tilde{\dot{x}} = ( \dot{x}^- + \dot{x}^+ )/2$) if such a point exists at a positive time step.
    3. Otherwise, if small "yo-yoing" metric indicates likely close to precise trajectory, limit time step to a growth factor from prior step. This allows time step to grow flexibly while staying close to the precise trajectory without needing a `dtInf` or `dtMax` control.
  - This may be automatable and efficient enough to allow its use in default state variable types but for now developing them as option-enabled alternative types
- Relaxation Testing:
  - ConservationEquationStep: Pulls QSS2 trajectory in to reference trajectory efficiently and then enables large steps.
    - Converged behavior can probably be improved, possibly with derivative relaxation.
  - Case600: Need to enable yo-yo metric detection to avoid slowing non-yo-yoing variables.
- Next Steps:
  - Finalize QSS2 relaxation and see if it is fast and automatic enough to merge into primary state variable types.
  - Develop QSS3 relaxation on analogous principles.
  - Profile/tune/parallelize.
  - Performance testing.

## Agenda: 2023/3/27
- QSS Development
  - Time step history output added: Actual steps at requantizations (not initial predicted and not observer steps. Informative for variables that dominate the requantizations.
  - Dependency management fixes.
  - Added --dot option to request Graphviz dot output files: These get too large to be practical for other than fairly small models.
  - Support .var file entries overriding default output filtering (so, e.g., you can get time signal output)
  - Made Computational Observers/Observees listing on all the time.
  - Changed dependency harvesting from `<ModelStructure>` to skip `<InitialUnknowns>`: Initialization dependencies shouldn't matter for QSS.
  - Support --out+<flags> and --out-<flags> to simplify output selection/overrides.
  - OCT 1.4.0 install/testing
    - Small differences from previous OCT update.
    - SimpleHouseDiscreteTime:
      - time initial value issue remains.
      - Number of event indicators went from 13 back to 12.
  - FMIL 2.4.1 build/mig/test. Posted two GitHub issues.
  - gtest 1.13.0 build/mig/test.
- SimpleHouseDiscreteTime Study
  - Newer revisions that add dependencies from `<ModelStructure>` catch a number of missing dependencies in `<Dependencies>`.
    The prior simulation was generally OK but some event indicators had no/missing dependencies so were wrong.
    Enough added dependencies to slow simulation => Important to eliminate extraneous dependencies.
  - time variable initialization issue noted in email: Added temporary work-around to use XML initial time value when they disagree.
- Relaxation
  - Michael is thinking about a small model that would demonstrate the dynBal.m sensitivity
  - Michael suggests looking at analytical derivative expression if the derivative approx is contributing to the sensitivity. I suspect that QSS is getting pretty good derivatives and the analytical would be similar but there is some extra noise due to ND that analytical or directional derivative should eliminate.
  - Did a deeper analysis of the relaxation metrics, estimates, and algorithms that gives good direction for the next round of refinements:
    - Idea for geometric approach to relaxing $\dot{x}$ and $\ddot{x}$ together that should avoid issues with derivative sign changes without requiring conditional logic.
    - Will also be trying a cleaner method for time step only relaxation since this could have a number of simplicity and performance advantages.
    - Should have both of these working within a few days and will report on progress.

## Agenda: 2023/3/13
- Relaxation QSS: Theory/Framework Development
  - Want simplest possible approach that is robust and self-controlling => Not too many independent controls
  - Relationship between $\dot{x}$ and $\ddot{x}$ relaxation and time step relaxation
  - Relaxation by magnitude _vs_ toward estimates
  - Moving average estimates to avoid chasing noise _vs_ gradual relaxation changes and relaxation limits
- Status
  - $\dot{x}$ relaxation along with $\ddot{x}$ and time step relaxation => Improves efficiency of converging on precise trajectory
  - conHea.I.y and conCoo.I.y are now driving more requantizations than roo.air.vol.dynBal.m: Look into making relaxation work better for them
- Plans
  - Try refinements of relaxation factor control logic
  - Try moving average $\dot{x}$ and $\ddot{x}$ trajectory boundary based estimates (to damp noise and distortion of trajectory convergence)
  - Use $\dot{x}$ nominal value instead of estimate for sensitivity metric to avoid need for both relative and absolute criteria to handle estimate approaching zero

## Agenda: 2023/2/27
- Relaxation/Multistep QSS Development
  - Goals
    - Efficient QSS algorithm adaptation that brings trajectories close enough to precise trajectory to allow safe large steps
    - Gradual and automatic trajectory correction
    - Ideally, fast enough that no user option required
  - Metrics for detecting/measuring variable sensitivity
    - Multistep $\dot{x}$ and $\ddot{x}$ estimates across requantization points
    - $\dot{x}$ and $\ddot{x}$ estimates from average of incoming and outgoing $\dot{x}$ at requantizations
    - ???
  - QSS2 algorithm adaptations evaluated
    - Shorten ("relax") time step to stop trajectory from traveling back out to Q-tolerance away from precise trajectory
      - Gradual relaxation so metrics are good enough
      - This can bring trajectory close to precise but $\dot{x}$ and $\ddot{x}$ remain large enough to limit step size
      - Got just modest step count reductions
    - Added $\ddot{x}$ relaxation
      - Improvement but $\dot{x}$ relaxation is still needed near precise trajectory to get to large steps
  - Conclusions
    - Don't yet have a clear best algorithm
    - Complex due to multiple, interacting relaxation factors
    - Adding $\dot{x}$ relaxation should get us the desired large steps

## Agenda: 2023/1/30
- Development
  - Harvest additional dependencies from `<ModelStructure>` to work around `<Dependencies>` issues
  - Special time variable that never requantizes to enable QSS1 testing without time requantizing and more efficiency for QSS2/3
  - Archive deferred-updating variable experiment due to poor performance
- Testing: Case600 roo.air.vol.dynBal.m is a good demo for the key performance issue for QSS on Buildings models
  - Self-dependent variable based on small differences between large values
  - Derivative gets very large at small offsets from exact solution => QSS2 solution "yo-yos" between Q-tolerance bracket around solution
    - The solver trajectory must quickly converge toward the exact solution to get close to its actual derivatives and allow large steps
    - Pure QSS trajectories evaluate at Q-tolerance boundary so they can't do this
  - Models may also be stiff but LIQSS alone doesn't overcome small step behavior caused by this derivative sensitivity
  - IBPSASync_issue1412_stateSelect_Tp Buildings branch is numerically better but doesn't eliminate the issue: QSS2 tracks the reference solution 3X better but still yo-yos
- Relaxation/Multistep QSS
  - Experimented with $\dot{x}$ and $\ddot{x}$ relaxation: Can increase step but not smooth convergence with this alone due to requantization still happening at Q-tolerance border
  - Inflection point option shows desired behavior on constant sections
  - Now looking at approaches to blending previous 3|4-point based $\dot{x}$ and $\ddot{x}$ with QSS 1-point values
  - Goal: efficient and smooth blend of QSS and multi-step trajectories to bring trajectory to exact solution
  - Develop a rationale for shortening these long steps to keep requantizations near enough to exact solution

## Agenda: 2022/12/15
- Development
  - Self-dependent event indicator variable fix to prevent resetting the zero-crossing event time on detected crossings
  - Continuous state variable deferred requantization and handler updates to remove ND-caused order dependency in QSS2+ in non-simultaneous events with self-dependency
  - LIQSS updates in progress to streamline code and eliminate more ND-caused order dependency
  - Initialization changes being evaluated to bootstrap initial state without ND-caused order dependencies and using refinement to get accurate higher order coefficients
- Testing
  - Guideline36: Behavior is believed to be representative of issues seen with other Buildings models
    - Early mis-tracking traced to event indicators with the same C1_flow * C2_flow we have run into before
      - C2_flow is mis-tracking -> states such as hvac.cooCoi.heaCooHum_u.vol.dynBal.m that are self-dependent and have tiny changes in early phase
      - QSS gets off track slightly and then worse => Probable numerical/stiffness issues
      - With dtMax=1e-4 QSS tracks well
    - PyFMI Testing: Looked at early behavior with different solvers: Conclusion = Stiff solver needed
      - CVode
        - BDF (stiff): Tracks well
        - Adams (non-stiff): Mis-tracks
      - ExplicitEuler: Mis-tracks until `h` reduced to 1e-4
      - RungeKutta34: Mis-tracks
      - Dopri5: Mis-tracks until step reduced to 1e-3
      - Radau5ODE: Tracks well
      - LSODAR: Tracks well
    - QSS Testing: QSS2 for now: Will run LIQSS2 after in-progress changes
      - ND time step affects results but doesn't correct tracking for non-LIQSS methods
      - Adding --dep changes solution => May have missing dependency issues
- Next
  - Do LIQSS methods fix tracking? If stiffness is primarily "diagonal" then it should and we see issues with self-dependent states
  - If EI requantizations remain dominant consider smarter and more automated approaches to reducing them than `--zFac`
  - Get performance results once tracking is OK

## Agenda: 2022/12/08
- General
  - Added computational observer/observee Graphviz graph generation to the direct dependency graph (helpful for debugging)
  - Computational observer intialization sequencing bug fixed
  - Functions for deferred update ND use fixed
  - QSS set for now to do some things differently than before
    - Simultaneous updates of interdependent states do deferred updates rather than trying to use evolving new trajectories
      - ND time steps and LIQSS make doing this in a pure, order-independent way impossible short of requiring and exploiting a triangularizable dependency matrix
      - Other variable types (EIs and BIDR) could update after states and also use new trajectories but for now they don't for some notion of consistency: Easy to switch
      - Deferred updating => order independence at each phase => parallelizable: Not exploited yet
    - Continuous states propagate continuous (not quantized) representations to their observers unlike traditional ODE QSS
      - Other variable types naturally want continuous representations (observees appear in their value, not derivative) so this is more consistent and can enable greater operation pooling for efficiency
      - Could readily make switchable to quantized and compare behavior later
      - This separates the function of the quantized rep for choosing when to requantize from its use as the external representation
- Testing
  - Many of the smaller models tested and behavior verified
  - Added an ObserverGraph model to demo/test computational observers/observees
  - UpstreamSampler switch behavior resolved by QSS bug fix
  - Case600 & Case600FF: Buildings 9 versions give wrong QSS results: Non-SI units present: Investigating
  - Guideline36 & ASHRAE2006: Some event indicator 2nd derivatives are off: Investigating to isolate cause: Non-SI units present
  - Can non-SI units be a problem for QSS?
    - Are directional derivative seeds assumed to be in their own units or SI units or the target variable's units?
    - Can a continuous state and its derivative used inconsistent or SI and non-SI units? Does integrator have to convert?

## Agenda: 2022/11/30
- Revised QSS is working as hoped
  - Observees (for setting variable values in FMU) are short-circuited to states and inputs
  - Observers (for signaling updates) short-circuit around passive variables
  - Passive variables can be output via sampled output times
  - Event indicators can depend on other event indicators to handle passive variable short-circuiting (but prefer Dependencies not to s-c): OCT generates some of these
  - Discrete intermediate variables can be active (firewall) or passive (short-circuited via --passive): Can test to see whether active is worth it in most models
  - Updates flow through intermediate variables immediately for consistency
  - Working with current OCT dependencies (at some reduced efficiency)
  - Not performance optimized yet: A number of efficiency updates deferred
- Results
  - Feature test models are working with current OCT dependencies as planned: Can be more efficient with dependency changes
  - UpstreamSampler: QSS run seems OK (was broken with previous QSS) but CVode run doesn't show sampler activity! (Doesn't work with Buildings 9) No reference solution to check against
  - Need to change observer advance cascade calls to deal with circular dependencies to get larger models running efficiently
  - Don't know if (non-event-generating) min/max are an issue for some models
  - Need to look at handling of non-state real variables with associated derivative variables
- Issues
  - Event indicator to event indicator dependencies in modelDescription.xml are used in two different situations, which interferes with QSS's ability to patch around the lack of direct dependencies:
    1. An intermediate "signaling" variable modified in on EI block that appears in the other EI expression has been short-circuited out
    2. The EIs share an expression or dependencies
    - QSS temporary work-around: Adds dependencies for both meanings: inefficient
  - Simultaneous events prevent consistent (order-independent) updating with ND
    - Doing deferred updating of states for now to avoid this but is that ideal?
    - Event handler blocks are tricky:
      - State handlers with interdependencies: Capture FMU post-event states in deferred values before overwriting them to do QSS updates/ND
      - See my DepTestR_ss
      - ZC "handlers" are really conditional observers due to s-c, not handlers, so they should be using updated handler values
      - BIDR handlers could be processed after state handlers do deferred updates but should they?
    - Does FMU/PyFMI do sequential updating in such blocks? Depends on "triangular" dependency structure (excluding pre())?
      - If QSS needs to do this it would need to know what dependencies are from pre()
  - Trying x-based observee values for states
    - A bit more accurate but may cause more ND noise
    - Enables simpler/faster code since BIDR and ZC variables are naturally X based: Can fully exploit this if we decide to stay with X-based
  - Zero crossing protocol
    - Need to set handler observee state before FMU event processing to make sure it sees correct pre() values ?
    - If ZC event fires FMU actually sets handler state at t_bump, not tZ: Add post-event correction for this ? Pass t_bump also and have it back correct x_0_ to ZC(tZ) ?
- Proposed OCT/spec changes
  - Dependencies
    - Direct dependencies only: No short-circuiting. Handler dependencies don't "look through" event indicators to their dependencies
    - No extra dependencies (see Issues)
    - Include those for local variables if practical
