model PID_Controller
  "Demonstrates the usage of a Continuous.LimPID controller"
  extends Modelica.Icons.Example;
  parameter Modelica.SIunits.Angle driveAngle=1.570796326794897 "Reference distance to move";
  Modelica.Blocks.Continuous.LimPID PI(
    k=100,
    Ti=0.1,
    yMax=12,
    Ni=0.1,
    initType=Modelica.Blocks.Types.Init.SteadyState,
    limitsAtInit=false,
    controllerType=Modelica.Blocks.Types.SimpleController.PI,
    Td=0.1);
  Modelica.Mechanics.Rotational.Components.Inertia inertia1(
   a(fixed=true),
   phi(fixed=true, start=0),
   J=1);

  Modelica.Mechanics.Rotational.Sources.Torque torque;
  Modelica.Mechanics.Rotational.Components.SpringDamper spring(
   c=1e4,
   d=100,
   stateSelect=StateSelect.prefer,
   w_rel(fixed=true));
  Modelica.Mechanics.Rotational.Components.Inertia inertia2(
   J=2);
  Modelica.Blocks.Sources.KinematicPTP kinematicPTP(
   startTime=0.5,
	deltaq={driveAngle},
   qd_max={1},
   qdd_max={1});
  Modelica.Blocks.Continuous.Integrator integrator(
   initType=Modelica.Blocks.Types.Init.InitialState);
  Modelica.Mechanics.Rotational.Sensors.SpeedSensor speedSensor;
  Modelica.Mechanics.Rotational.Sources.ConstantTorque loadTorque(
   tau_constant=10,
   useSupport=false);
initial equation
  der(spring.w_rel) = 0;
equation
  connect(spring.flange_b, inertia2.flange_a);
  connect(inertia1.flange_b, spring.flange_a);
  connect(torque.flange, inertia1.flange_a);
  connect(kinematicPTP.y[1], integrator.u);
  connect(speedSensor.flange, inertia1.flange_b);
  connect(loadTorque.flange, inertia2.flange_b);
  connect(PI.y, torque.tau);
  connect(speedSensor.w, PI.u_m);
  connect(integrator.y, PI.u_s);
end PID_Controller;
