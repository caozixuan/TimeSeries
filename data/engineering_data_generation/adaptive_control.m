
f = [-3:0.01:3];
s = size(f);
R = 1.3*ones(1,s(2));
h = f.^2-R.^2;
k = 0.05;
w1 = 1-((min(0,(min(0,h)).^4-((k*R).^2-R.^2).^4)).^4)./((k*R).^2-R.^2).^16;
k = 0.9;
w2 = 1-((min(0,(min(0,h)).^4-((k*R).^2-R.^2).^4)).^4)./((k*R).^2-R.^2).^16;

plot(f,w1,f,w2);
legend('k=0.05','k=0.9');