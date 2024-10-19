clear all;  % 清除所有变量
clc;        % 清空命令窗口

% 初始条件
v0 = 22;          % 初速度 (m/s)
pitch = 20;       % 俯仰角 (度)
yaw = -80;        % 偏航角 (度) 向 y 轴负方向发射
x1 = 0;           % 初始 x 坐标 (m)
y1 = 10;          % 初始 y 坐标 (m)
z1 = 0;           % 初始 z 坐标 (m)
g = 9.8;         % 重力加速度 (m/s^2)
rho = 1.225;      % 空气密度 (kg/m^3)
d = 0.22;         % 足球直径 (m)
m = 0.220;        % 足球质量 (kg)
mu = 1.81e-5;     % 空气动力粘度 (Pa.s)
Cn1 = [-0.0206, 0.9286]; % Cdnh1系数
Cn2 = [1.5, 0.4]; % Cdnh2系数

% 将角度转换为弧度
pitch = deg2rad(pitch);
yaw = deg2rad(yaw);

% 计算初始速度的分量
v0x = v0 * cos(pitch) * cos(yaw);  % 水平分量 x
v0y = v0 * cos(pitch) * sin(yaw);  % 水平分量 y
v0z = v0 * sin(pitch);             % 垂直分量 z

% 初始状态向量 [x0, y0, z0, vx0, vy0, vz0]
initial_conditions = [x1; y1; z1; v0x; v0y; v0z];

% 时间范围
tspan = [0 10];

% 使用 ode45 求解微分方程
[t, state] = ode45(@(t, state) projectile(t, state, rho, d, mu, m, g, Cn1, Cn2), tspan, initial_conditions);

% 计算位置
x = state(:, 1);
y = state(:, 2);
z = state(:, 3);

% 找到足球与球门所在平面的交点 (y = 0)
y_position = state(:, 2);
crossing_index = find(y_position < 0, 1);

% 绘制运动轨迹
figure;
plot3(x, y, z, 'b-', 'LineWidth', 2);
hold on;

if isempty(crossing_index)
    disp('足球未能到达球门平面');
else
    % 确保轨迹不超过 xz 平面
    x_hit = x(crossing_index);
    z_hit = z(crossing_index);
    fprintf('足球打在球门平面上的位置：x = %.2f m, z = %.2f m\n', x_hit, z_hit);
    
    % 检查是否在球门范围内
    goal_width = 7.32;
    goal_height = 2.44;
    if abs(z_hit) <= goal_height / 2 && abs(x_hit) <= goal_width / 2
        disp('足球进门了！');
    else
        disp('足球未进门');
    end
    
    % 标记球打在球门平面上的位置
    plot3(x_hit, 0, z_hit, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
end

xlabel('水平距离 x (m)');
ylabel('水平距离 y (m)');
zlabel('垂直距离 z (m)');
title('运动轨迹');
grid on;
zlim([0, inf]); % 只显示 z >= 0 的部分

% 定义微分方程
function dstate = projectile(~, state, rho, d, mu, m, g, Cn1, Cn2)
    x = state(1);
    y = state(2);
    z = state(3);
    vx = state(4);
    vy = state(5);
    vz = state(6);
    
    speed = sqrt(vx^2 + vy^2 + vz^2);
    
    % 计算雷诺数
    Re = (rho * speed * d) / mu;
    
    % 计算阻力系数 Cdnh
    Cdnh1 = exp(Cn1(1) * Re + Cn1(2)) + 0.76;
    Cdnh2 = Cn2(1) / Re + Cn2(2);
    Cdnh = (atan((exp(Re) - exp(25)) / exp(24)) / 1.5708 + 1) / 2 * Cdnh1 + ...
           (1 - (atan((exp(Re) - exp(25)) / exp(24)) / 1.5708 + 1) / 2) * Cdnh2;
    
    % 计算迎风面积 A
    A = pi * (d / 2)^2;
    
    % 计算空气阻力 Fd
    Fd = 0.5 * rho * speed^2 * A * Cdnh;
    
    % 将空气阻力加速度分解到三个方向
    ax_drag = -Fd / m * (vx / speed);
    ay_drag = -Fd / m * (vy / speed);
    az_drag = -Fd / m * (vz / speed);
    
    % 计算加速度
    dvxdt = ax_drag;
    dvydt = ay_drag;
    dvzdt = -g + az_drag;
    
    % 状态导数 [dx, dy, dz, dvx, dvy, dvz]
    dstate = [vx; vy; vz; dvxdt; dvydt; dvzdt];
end
