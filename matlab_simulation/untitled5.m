% 初始条件
initial_speed = 50;
roll_angle = 180;
spin_speed = 5;
target_position = [0, 10, 2];  % 目标位置，例子中的坐标
pitch_range = linspace(0, 60, 300);  % 在0到60度之间分成200份
yaw_range = linspace(45, 135, 300);  % 在45到135度之间分成200份

% 球门参数
goal_width = 7.32;  % 标准球门宽度 (m)
goal_height = 2.44; % 标准球门高度 (m)

% 初始化误差和对应的角度数组
errors = [];
pitch_yaw_pairs = [];

% 初始化计数器
counter = 0;
error_values = []; % 记录每次遍历的误差值

% 记录开始时间
tic;

% 遍历所有 pitch 和 yaw 的组合
for i = 1:length(pitch_range)
    for j = 1:length(yaw_range)
        pitch = pitch_range(i);
        yaw = yaw_range(j);
        
        % 计算当前组合下的误差和击中位置
        [error, hit_position] = compute_trajectory_error_with_position([pitch, yaw], target_position, initial_speed, spin_speed, roll_angle);
        
        % 记录误差值
        error_values = [error_values; error];
        
        % 检查是否在球门范围内
        if abs(hit_position(1)) <= goal_width / 2 && hit_position(3) <= goal_height
            errors = [errors; error];
            pitch_yaw_pairs = [pitch_yaw_pairs; pitch, yaw];
        end
        
        % 增加计数器并输出
        counter = counter + 1;
        fprintf('已遍历组合数量：%d, 当前误差：%.4f\n', counter, error);
    end
end

% 记录结束时间并计算总时间
elapsed_time = toc;
fprintf('Total elapsed time: %.2f seconds\n', elapsed_time);

% 选择误差最小的组合
[min_error, min_index] = min(errors);
optimal_angles = pitch_yaw_pairs(min_index, :);

fprintf('Optimal Pitch Angle: %.2f degrees\n', optimal_angles(1));
fprintf('Optimal Yaw Angle: %.2f degrees\n', optimal_angles(2));
fprintf('Minimum Error: %.6f\n', min_error);

% 计算误差分布
edges = linspace(min(error_values), max(error_values), 50);
counts = histcounts(error_values, edges);

% 绘制误差分布的直方图
figure;
h = histogram(error_values, edges, 'FaceColor', 'blue', 'EdgeColor', 'black');
xlabel('Error');
ylabel('Frequency');
title('Distribution of Errors');

% 在直方图上添加最小误差值
text(mean(edges), max(counts)*0.9, sprintf('Min Error: %.6f', min_error), 'FontSize', 12, 'Color', 'red', 'FontWeight', 'bold', 'HorizontalAlignment', 'center');

grid on;

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
    
    % 选择一个任意向量 a，不平行于 v0_unit
    a = [1; 0; 0];
    if dot(a, v0_unit) == 1  % 如果 a 平行于 v0_unit，则选择另一个向量
        a = [0; 1; 0];
    end
    
    % 通过叉乘得到一个垂直于 v0_unit 的向量 b
    b = cross(v0_unit, a);
    b_unit = b / norm(b);
    
    % 通过叉乘 v0_unit 和 b_unit，得到辅助坐标系的 y' 轴方向向量
    c = cross(v0_unit, b_unit);
    c_unit = c / norm(c);
    
    % 计算 omega 在辅助坐标系 x' 和 y' 轴上的分量
    omega_x_prime = w * cos(roll);
    omega_y_prime = w * sin(roll);
    
    % 将 omega 分量转换回原始坐标系
    omega = omega_x_prime * b_unit + omega_y_prime * c_unit;
    
    % 初始状态向量 [x0, y0, z0, vx0, vy0, vz0, wx, wy, wz]
    initial_state = [0; 0; 0; v0x; v0y; v0z; omega(1); omega(2); omega(3)];
    
    % 时间范围
    tspan = [0 10];
    
    % 使用 ode45 求解微分方程
    [t, state] = ode45(@(t, state) projectile(t, state, omega), tspan, initial_state);
    
    % 计算位置
    x = state(:, 1);
    y = state(:, 2);
    z = state(:, 3);
    
    % 找到足球与球门所在平面的交点 (y = 10)
    y_position = state(:, 2);
    crossing_index = find(y_position >= 10, 1);
    
    if isempty(crossing_index)
        % 如果足球未能到达球门平面，则将误差设置为一个大值
        error = inf;
        hit_position = [inf, inf, inf];
    else
        % 确保轨迹不超过 xz 平面
        x_hit = x(crossing_index);
        z_hit = z(crossing_index);
        hit_position = [x_hit, 10, z_hit];
        
        % 计算与目标位置的误差
        error = norm(hit_position - target_position);
    end
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
    rho = 1.225;        % 空气密度 (kg/m^3)
    d = 0.22;           % 足球直径 (m)
    m = 0.220;          % 足球质量 (kg)
    g = 9.8;            % 重力加速度 (m/s^2)
    
    % 计算速度和速度大小
    velocity = [vx; vy; vz];
    speed = norm(velocity);
    
    % 计算阻力系数 Cd
    mu = 1.81e-5;  % 空气动力粘度 (Pa.s)
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
    dstate(1) = vx;        % x 方向速度
    dstate(2) = vy;        % y 方向速度
    dstate(3) = vz;        % z 方向速度
    dstate(4) = acceleration(1);  % x 方向加速度
    dstate(5) = acceleration(2);  % y 方向加速度
    dstate(6) = acceleration(3);  % z 方向加速度
    dstate(7) = 0;         % 角速度 wx 不变
    dstate(8) = 0;         % 角速度 wy 不变
    dstate(9) = 0;         % 角速度 wz 不变
end
