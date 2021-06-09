model ACControl10
// Based on the Case Study I model used in and provided by the authors of the paper:
//  On the Efficiency of Quantization–Based Integration Methods for Building Simulation
//  https://usuarios.fceia.unr.edu.ar/~kofman/files/buildings_qss.pdf
  constant Integer N = 10;
  parameter Real AirCap0 = 1012;
  parameter Real BrickConductivity = 0.89;
  parameter Real RoomLength = 3;
  parameter Real RoomHeight = 3;
  parameter Real RoomWide = 3;
  parameter Real WallLength = 0.3;
  parameter Real WallHeatTransferArea = 2 * RoomLength * RoomHeight + 2 * RoomWide * RoomHeight;
  parameter Real WallResistance = WallLength / WallHeatTransferArea / BrickConductivity;
  parameter Real AirWeight = 35;
  parameter Real AirCap = AirWeight * AirCap0;
  parameter Real ACPower = 1000;
  parameter Real InitialTemp = 22;
  parameter Real CAP[N] = {38912.3, 37169.3, 40325.4, 39966.2, 41771.7, 37570.8, 38970.4, 37352.7, 38041.4, 44033.9};
  parameter Real RES[N] = {0.0111964, 0.010148, 0.0104808, 0.0115923, 0.00969476, 0.00968453, 0.00966711, 0.010564, 0.0108557, 0.010048};
  parameter Real POT[N] = {1199.61, 1192.06, 1157.22, 1229.05, 1151.74, 1201.04, 1027.2, 1209.78, 1131.07, 1192.84};
  parameter Real THA = 32, pmax = sum(POT), Kp = 1, Ki = 1, tref = 20;
  Real th[N](each fixed = true, start = {26.621, 27.0141, 23.5278, 24.0063, 25.4964, 22.0897, 22.8617, 27.4941, 25.3695, 24.7147});
  discrete Real ierr(fixed = true, start = 0);
  discrete Real ptotal(start = 0);
  discrete Real on[N](each fixed = false);
  discrete Real dtref(fixed = true, start = 0.0), pref(fixed = true, start = 0.5);
  discrete Real nextSample(start = 1, fixed = true);
initial equation
  for i in 1:N loop
    if th[i] > tref then
      on[i] = 1;
    else
      on[i] = 0;
    end if;
  end for;
  ptotal = on * POT;
equation
  for i in 1:N loop
    der(th[i]) = ( THA - th[i] ) / ( RES[i] * CAP[i] ) - ( POT[i] * on[i] ) / CAP[i];
  end for;
algorithm
    when th[1] > tref + dtref + 0.5 then
      on[1] := 1;
    elsewhen th[1] < tref + dtref - 0.5 then
      if time > 0 then
        on[1] := 0;
      end if;
    end when;
    when th[2] > tref + dtref + 0.5 then
      on[2] := 1;
    elsewhen th[2] < tref + dtref - 0.5 then
      if time > 0 then
        on[2] := 0;
      end if;
    end when;
    when th[3] > tref + dtref + 0.5 then
      on[3] := 1;
    elsewhen th[3] < tref + dtref - 0.5 then
      if time > 0 then
        on[3] := 0;
      end if;
    end when;
    when th[4] > tref + dtref + 0.5 then
      on[4] := 1;
    elsewhen th[4] < tref + dtref - 0.5 then
      if time > 0 then
        on[4] := 0;
      end if;
    end when;
    when th[5] > tref + dtref + 0.5 then
      on[5] := 1;
    elsewhen th[5] < tref + dtref - 0.5 then
      if time > 0 then
        on[5] := 0;
      end if;
    end when;
    when th[6] > tref + dtref + 0.5 then
      on[6] := 1;
    elsewhen th[6] < tref + dtref - 0.5 then
      if time > 0 then
        on[6] := 0;
      end if;
    end when;
    when th[7] > tref + dtref + 0.5 then
      on[7] := 1;
    elsewhen th[7] < tref + dtref - 0.5 then
      if time > 0 then
        on[7] := 0;
      end if;
    end when;
    when th[8] > tref + dtref + 0.5 then
      on[8] := 1;
    elsewhen th[8] < tref + dtref - 0.5 then
      if time > 0 then
        on[8] := 0;
      end if;
    end when;
    when th[9] > tref + dtref + 0.5 then
      on[9] := 1;
    elsewhen th[9] < tref + dtref - 0.5 then
      if time > 0 then
        on[9] := 0;
      end if;
    end when;
    when th[10] > tref + dtref + 0.5 then
      on[10] := 1;
    elsewhen th[10] < tref + dtref - 0.5 then
      if time > 0 then
        on[10] := 0;
      end if;
    end when;

  when time > 1000 then
    pref := 0.4;
  elsewhen time > 2000 then
    pref := 0.5;
  end when;

  when time > nextSample then
    nextSample := nextSample + 1;
    ptotal := on * POT;
    ierr := ierr + pref - ptotal / pmax;
    dtref := Kp * (ptotal / pmax - pref) - Ki * ierr;
  end when;
  annotation(experiment(StartTime = 0, StopTime = 3600, Tolerance = 0.001, Interval = 0.72));
end ACControl10;
