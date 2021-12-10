model BIDR
  discrete output Real d1( start=0.0, fixed=true );
  discrete output Real d2( start=0.0, fixed=true );
  output Real r1( start=0.0, fixed=true );
  output Real r2( start=0.0, fixed=true );
  output Real r3;
equation
  d1 = integer(time); // integer() is event generating so get EIs and d1 is updated by an EI handler => QSS can safely get value from variable cached value
  d2 = d1; // This isn't event generating. When d1 updates d2 will get observer update => QSS can safely get value from variable cached value
  r1 = time^2; // This isn't event generating so QSS needs a (non-constant) trajectory to track r1?
  when time < 1 then // r2 has an event but is constant between events so doesn't need a trajectory
    r2 = time;
  elsewhen time >= 1 then
    r2 = time^2;
  end when;
  if time < 1 then // r3 has an event but is not constant between events so needs a trajectory. OCT doesn't indicate an if vs when event indicator so QSS can't exploit this
    r3 = time;
  else
    r3 = time^2;
  end if;
annotation( experiment( StartTime=0, StopTime=3, Tolerance=1e-4 ) );
end BIDR;
