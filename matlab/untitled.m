vz = 10; % velocity constant
a = -32; % acceleration constant         
t = 0:.1:1;
z = vz*t + 1/2*a*t.^2;

vx = 20;
x = vx*t;
 
vy = 30;
y = vy*t;

u = gradient(x);
v = gradient(y);
w = gradient(z);
scale = 0;
 
figure
quiver3(x,y,z,u,v,w,scale)
view([70,18])




%运动学正解：
%输入：v，θ，α（不考虑自旋）
%输出：（x，y）          f（t）=？

%运动学反解
%输入：（x，y）
%v定下来

