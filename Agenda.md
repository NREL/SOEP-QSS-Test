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
