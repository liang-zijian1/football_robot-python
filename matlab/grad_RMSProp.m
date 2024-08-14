% 初始条件
initial_speed = 50;
roll_angle = 180;
spin_speed = 5;
target_position = [-2, 10, 1.5];  % 目标位置，例子中的坐标

% RMSProp优化参数
learning_rate = 0.035;
beta = 0.9;
epsilon = 1e-8;
num_iterations = 800;

% 初始化pitch和yaw
pitch = 30; % 固定初始pitch角度
yaw = 90;   % 固定初始yaw角度

% RMSProp优化变量
s_pitch = 0;
s_yaw = 0;

% 迭代更新pitch和yaw
for iter = 1:num_iterations
    % 计算当前组合下的误差和击中位置
    [error, hit_position] = compute_trajectory_error_with_position([pitch, yaw], target_position, initial_speed, spin_speed, roll_angle);
    
    % 打印当前迭代的信息
    fprintf('Iteration %d: pitch = %.4f, yaw = %.4f, error = %.6f\n', iter, pitch, yaw, error);
    
    % 计算梯度
    grad_pitch = compute_gradient_pitch(pitch, yaw, target_position, initial_speed, spin_speed, roll_angle);
    grad_yaw = compute_gradient_yaw(pitch, yaw, target_position, initial_speed, spin_speed, roll_angle);
    
    % 更新RMSProp优化变量
    s_pitch = beta * s_pitch + (1 - beta) * grad_pitch^2;
    s_yaw = beta * s_yaw + (1 - beta) * grad_yaw^2;
    
    % 更新pitch和yaw
    pitch = pitch - learning_rate * grad_pitch / (sqrt(s_pitch) + epsilon);
    yaw = yaw - learning_rate * grad_yaw / (sqrt(s_yaw) + epsilon);
end

fprintf('Optimal Pitch Angle: %.2f degrees\n', pitch);
fprintf('Optimal Yaw Angle: %.2f degrees\n', yaw);
fprintf('Minimum Error: %.2f\n', error);

% 计算轨迹误差和击中位置的函数
function [error, hit_position] = compute_trajectory_error_with_position(angles, target_position, initial_speed, spin_speed, roll_angle)
    pitch = deg2rad(angles(1));
    yaw = deg2rad(angles(2));
    roll = deg2rad(roll_angle);
    w = spin_speed;
    
    % 计算初始速度的分量
    v0x = initial_speed * cos(pitch) * cos(yaw);
    v0y = initial_speed * cos(pitch) * sin(yaw);
    v0z = initial_speed * sin(pitch);
    
    % 计算初始速度的单位方向向量
    v0_unit = [v0x; v0y; v0z] / norm([v0x; v0y; v0z]);
    
    % 选择一个任意向量a，不平行于v0_unit
    a = [1; 0; 0];
    if dot(a, v0_unit) == 1  % 如果a平行于v0_unit，则选择另一个向量
        a = [0; 1; 0];
    end
    
    % 通过叉乘得到一个垂直于v0_unit的向量b
    b = cross(v0_unit, a);
    b_unit = b / norm(b);
    
    % 通过叉乘v0_unit和b_unit，得到辅助坐标系的y'轴方向向量
    c = cross(v0_unit, b_unit);
    c_unit = c / norm(c);
    
    % 计算omega在辅助坐标系x'和y'轴上的分量
    omega_x_prime = w * cos(roll);
    omega_y_prime = w * sin(roll);
    
    % 将omega分量转换回原始坐标系
    omega = omega_x_prime * b_unit + omega_y_prime * c_unit;
    
    % 初始状态向量[x0, y0, z0, vx0, vy0, vz0, wx, wy, wz]
    initial_state = [0; 0; 0; v0x; v0y; v0z; omega(1); omega(2); omega(3)];
    
    % 时间范围
    tspan = [0 10];
    
    % 使用ode45求解微分方程
    [t, state] = ode45(@(t, state) projectile(t, state, omega), tspan, initial_state);
    
    % 计算位置
    x = state(:, 1);
    y = state(:, 2);
    z = state(:, 3);
    
    % 找到足球与球门所在平面的交点(y=10)
    y_position = state(:, 2);
    crossing_index = find(y_position >= 10, 1);
    
    if isempty(crossing_index)
        % 如果足球未能到达球门平面，则将误差设置为一个大值
        error = inf;
        hit_position = [inf, inf, inf];
    else
        % 确保轨迹不超过xz平面
        x_hit = x(crossing_index);
        z_hit = z(crossing_index);
        hit_position = [x_hit, 10, z_hit];
        
        % 计算与目标位置的误差
        error = norm(hit_position - target_position);
    end
end

% 计算pitch梯度的函数
function grad_pitch = compute_gradient_pitch(pitch, yaw, target_position, initial_speed, spin_speed, roll_angle)
    epsilon = 1e-5;
    [error1, ~] = compute_trajectory_error_with_position([pitch + epsilon, yaw], target_position, initial_speed, spin_speed, roll_angle);
    [error2, ~] = compute_trajectory_error_with_position([pitch - epsilon, yaw], target_position, initial_speed, spin_speed, roll_angle);
    grad_pitch = (error1 - error2) / (2 * epsilon);
end

% 计算yaw梯度的函数
function grad_yaw = compute_gradient_yaw(pitch, yaw, target_position, initial_speed, spin_speed, roll_angle)
    epsilon = 1e-5;
    [error1, ~] = compute_trajectory_error_with_position([pitch, yaw + epsilon], target_position, initial_speed, spin_speed, roll_angle);
    [error2, ~] = compute_trajectory_error_with_position([pitch, yaw - epsilon], target_position, initial_speed, spin_speed, roll_angle);
    grad_yaw = (error1 - error2) / (2 * epsilon);
end

% 定义微分方程
function dstate = projectile(~, state, omega)
    % 提取状态变量
    x = state(1);
    y = state(2);
    z = state(3);
    vx = state(4);
    vy = state(5);
    vz = state(6);
    
    % 足球和空气参数
    rho = 1.225;        % 空气密度(kg/m^3)
    d = 0.22;           % 足球直径(m)
    m = 0.220;          % 足球质量(kg)
    g = 9.8;            % 重力加速度(m/s^2)
    
    % 计算速度和速度大小
    velocity = [vx; vy; vz];
    speed = norm(velocity);
    
    % 计算阻力系数Cd
    mu = 1.81e-5;  % 空气动力粘度(Pa.s)
    Re = (rho * speed * d) / mu;
    Cd = 0.5 * (1.5 + 0.4) + (atan((exp(Re) - exp(25)) / exp(24)) / 1.5708 + 1) / 2 * (exp(-0.0206 * Re + 0.9286) + 0.76 - 0.5 * (1.5 + 0.4));
    
    % 计算空气阻力
    A = pi * (d / 2)^2;  % 截面积
    Fd = 0.5 * rho * speed^2 * A * Cd;
    
    % 计算马格努斯力
    Cl = 1;  % 升力系数，取一个常数值
    if speed == 0
        Fm = [0; 0; 0];  % 避免速度为零时的除零错误
    else
        Fm = Cl * 0.5 * rho * A * cross(omega, velocity);
    end
    
    % 计算总加速度
    acceleration = (-Fd / m) * (velocity / speed) + Fm / m - [0; 0; g];
    
    % 更新状态导数
    dstate = zeros(9, 1);
    dstate(1) = vx;        % x方向速度
    dstate(2) = vy;        % y方向速度
    dstate(3) = vz;        % z方向速度
    dstate(4) = acceleration(1);  % x方向加速度
    dstate(5) = acceleration(2);  % y方向加速度
    dstate(6) = acceleration(3);  % z方向加速度
    dstate(7) = 0;  % 角速度x分量保持不变
    dstate(8) = 0;  % 角速度y分量保持不变
    dstate(9) = 0;  % 角速度z分量保持不变
end
