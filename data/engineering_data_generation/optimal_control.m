%Optimal Control

clear;

%Parameter
ks = 3.508; %Nm/degree
n = 160;  %reduction ratio
Im = 1.38e-5*n^2;   %kg*m^2
Il = 0.1384;   %kg*m^2
K = 0.0603*n; %Nm/A
cm = 1/(6000*3.04)*n^2; %Nm*s/degree
cl = 2.09e-6; %Nm*s/degree
Vmax = 3.12; %A   %Vmax is actually current

%State space of SEA&load
A = [0,1,0,0;-ks/Il,-cl/Il,ks/Il,0;0,0,0,1;ks/Im,0,-ks/Im,-cm/Im];
B = [0,0;0,1/Il;0,0;K/Im,0];
C = [0,0,1,0;1,0,0,0;-ks,0,ks,0];
D = zeros(3,2);


%-------------------Optimal Position Control---------------------------
%Set the cost function matrix
a = 0.1; b = 1; c = 100;
Q = [a*ks^2+b,0,-a*ks^2,0;0,0,0,0;-a*ks^2,0,a*ks^2+b,0;0,0,0,0];
R = c/Vmax^2;

%Calculate feedback matrix F
Kf = lqr(A,B(:,1),Q,R);

%Calculate G
G = -Im/K*(A-B(:,1)*Kf)/C(1:2,:)*[1;1];
G = G(4);