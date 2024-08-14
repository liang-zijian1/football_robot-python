function inverse_kinematics2(target_position, initial_speed, spin_speed, roll_angle)
    % 球门参数
    goal_width = 7.32;  % 球门宽度 (米)
    goal_height = 2.44; % 球门高度 (米)
    goal_y = 10;        % 球门在 y 方向的位置

    % 检查目标位置是否在球门区域内
    if target_position(2) ~= goal_y
        error('目标位置 y 应该为 %f 米', goal_y);
    end

    if target_position(1) < -goal_width/2 || target_position(1) > goal_width/2
        error('目标位置 x 应该在 [%f, %f] 范围内', -goal_width / 2, goal_width / 2);
    end

    if target_position(3) < 0 || target_position(3) > goal_height
        error('目标位置 z 应该在 [0, %f] 范围内', goal_height);
    end

    % 设定初始条件范围和优化参数
    pitch_range = [0, pi/2]; % 俯仰角范围
    yaw_range = [0, 2*pi];  % 偏航角范围

    % 优化目标函数
    objective_function = @(angles) compute_trajectory_error(angles, target_position, initial_speed, spin_speed, roll_angle);

    % 粒子群优化选项
    options = optimoptions('particleswarm', ...
        'Display', 'iter', ...
        'SwarmSize', 100, ...
        'MaxIterations', 15000, ...
        'FunctionTolerance', 1e-6, ...
        'HybridFcn', @fmincon);

    % 使用 particleswarm 进行优化求解
    [optimal_angles, error] = particleswarm(objective_function, 2, [pitch_range(1), yaw_range(1)], [pitch_range(2), yaw_range(2)], options);

    % 提取最优解
    optimal_pitch = optimal_angles(1);
    optimal_yaw = optimal_angles(2);

    % 显示结果
    fprintf('Optimal Pitch Angle: %.2f degrees\n', rad2deg(optimal_pitch));
    fprintf('Optimal Yaw Angle: %.2f degrees\n', rad2deg(optimal_yaw));
    fprintf('Error: %.2f\n', error);
end

function error = compute_trajectory_error(angles, target_position, initial_speed, spin_speed, roll_angle)
    % 提取角度
    pitch = angles(1);
    yaw = angles(2);

    % 初始速度分量
    v0x = initial_speed * cos(pitch) * cos(yaw);
    v0y = initial_speed * cos(pitch) * sin(yaw);
    v0z = initial_speed * sin(pitch);

    % 初始状态向量
    initial_state = [0; 0; 0; v0x; v0y; v0z; spin_speed * cos(roll_angle); spin_speed * sin(roll_angle); 0];

    % 时间范围
    tspan = [0 10];

    % 使用 ode45 求解微分方程
    [~, state] = ode45(@(t, state) projectile(t, state, spin_speed), tspan, initial_state);

    % 计算末端位置
    final_position = state(end, 1:3);

    % 计算误差
    error = norm(final_position - target_position);
end

function dstate = projectile(~, state, spin_speed)
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
        Fm = Cl * 0.5 * rho * A * cross([0; 0; spin_speed], velocity);
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
    dstate(7) = 0;         % omega_x 恒定
    dstate(8) = 0;         % omega_y 恒定
    dstate(9) = 0;         % omega_z 恒定
end
