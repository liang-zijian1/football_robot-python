m = 2;                                    %质点质量kg
k = 0.50;                                 %空气阻力f = -k * v^2，国际单位
g = 9.8;                                  %重力加速度
theta1 = pi / 6;                           %出射仰角rad
theta2 = pi / 6;
v0 = 20;                                  %初速度大小
vx0 = v0 * cos(theta1);
vy0 = v0 * sin(theta1);
z0 = [vx0, vy0];                          %构造微分方程组
x0 = 0;
y0 = 0;
f = @(t,z) [-k * z(1) * sqrt(z(1)^2 + z(2)^2) / m; -k * z(2) * sqrt(z(1)^2 + z(2)^2) / m - g];
[T, Z] = ode45(f, [0, 1.5], z0);
vx = Z(:,1);
vy = Z(:,2);
x = x0;
y = y0;
for i = 1:length(T)-1                     %手动数值积分
    tempx =  x(i) + vx(i) * (T(i+1) - T(i));
    tempy =  y(i) + vy(i) * (T(i+1) - T(i));
    x = [x;tempx];
    y = [y;tempy];
end
plot(x, y)
