%Mix Control

clear;

%Parameter
ks = 3.508; %Nm/degree
n = 160;  %reduction ratio
Im = 1.38e-5*n^2;   %kg*m^2
Il = 0.1384;   %kg*m^2
K = 0.0603*n; %Nm/A
cm = 1/(6000*3.04)*n^2; %Nm*s/degree
cl = 2.09e-6; %Nm*s/degree

%State space of SEA&load
A = [0,1,0,0;-ks/Il,-cl/Il,ks/Il,0;0,0,0,1;ks/Im,0,-ks/Im,-cm/Im];
B = [0,0;0,1/Il;0,0;K/Im,0];
C = [0,0,1,0;1,0,0,0;-ks,0,ks,0];
D = zeros(3,2);

%Transfer function between V and Ms
open_sys = tf(K*ks*[Il,cl],[Il*Im,Il*cm+Im*cl,Il*ks+Im*ks+cl*cm,cl*ks+cm*ks]);
open_sys_simple = tf(K*ks*[Il],[Il*Im,0,Il*ks+Im*ks]);
controller = zpk([-5],[],1);

%Calculate the PID parameters
ksai_torque = 0.707;
ts_torque = 1;
wn_torque = -(log(0.05)+log(sqrt(1-ksai_torque^2)))/(ksai_torque*ts_torque);
beta_torque = 5*ksai_torque*wn_torque;
den = K*ks/Im;
Kd = (2*ksai_torque*wn_torque+beta_torque)/den;
Ki = (beta_torque*wn_torque^2)/den;
Kp = ((2*ksai_torque*wn_torque*beta_torque+wn_torque^2-(Il+Im)*ks/Il/Im))/den;

%Calculate the target poles and F
ksai_pos = 0.9;
ts_pos = 1;
wn_pos = -(log(0.05)+log(sqrt(1-ksai_pos^2)))/(ksai_pos*ts_pos);
Target_Pole = [-ksai_pos*wn_pos+ksai_pos*wn_pos*1i,-ksai_pos*wn_pos-ksai_pos*wn_pos*1i,-8*ksai_pos*wn_pos,-10*ksai_pos*wn_pos];
Kf = acker(A,B(:,1),Target_Pole);

%Calculate G
G = -Im/K*(A-B(:,1)*Kf)/C(1:2,:)*[1;1];
G = G(4);

%-------------------Position Discrete Part---------------------------
sample_time = 0.01;
sysc = ss(A,B,C,D);
sysd = c2d(sysc,0.01);
Ad = sysd.A;
Bd = sysd.B;
Cd = sysd.C;
Dd = sysd.D;
Target_Pole_Discrete=exp(Target_Pole*sample_time);
Kfd = acker(Ad,Bd(:,1),Target_Pole_Discrete);
Gd = Kfd(1)+Kfd(3);