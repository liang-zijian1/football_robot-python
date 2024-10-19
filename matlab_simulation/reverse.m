function reverse()
    % 初始条件
    goal_position = [10, 2]; % 球门平面上的目标位置 (x, z)
    v0 = 50; % 初速度大小
    w = 5; % 角速度大小 (已知)
    
    % 初始猜测 (俯仰角, 偏航角, 角速度俯仰角, 角速度偏航角)
    initial_guess = [45; 45; 45; 45];  % 示例初始猜测
    
    % 设定 fsolve 选项
    options = optimoptions('fsolve', 'Display', 'iter', 'MaxFunctionEvaluations', 5000);
    
    % 调用 fsolve 反解
    solution = fsolve(@objective_function, initial_guess, options);
    
    % 输出结果
    fprintf('初始速度方向 - 俯仰角: %.4f\n', solution(1));
    fprintf('初始速度方向 - 偏航角: %.4f\n', solution(2));
    fprintf('初始角速度方向 - 俯仰角: %.4f\n', solution(3));
    fprintf('初始角速度方向 - 偏航角: %.4f\n', solution(4));
    
    function F = objective_function(vars)
        % 提取变量
        pitch = deg2rad(vars(1));  % 初始速度方向 - 俯仰角 (degree to radian)
        yaw = deg2rad(vars(2));    % 初始速度方向 - 偏航角 (degree to radian)
        spin_pitch = deg2rad(vars(3));  % 初始角速度方向 - 俯仰角 (degree to radian)
        spin_yaw = deg2rad(vars(4));    % 初始角速度方向 - 偏航角 (degree to radian)
        
        % 计算初始速度的分量
        v0x = v0 * cos(pitch) * cos(yaw);  % 水平分量 x
        v0y = v0 * cos(pitch) * sin(yaw);  % 水平分量 y
        v0z = v0 * sin(pitch);             % 垂直分量 z
        
        % 初始角速度分量
        omega_x = w * cos(spin_pitch) * cos(spin_yaw);
        omega_y = w * cos(spin_pitch) * sin(spin_yaw);
        omega_z = w * sin(spin_pitch);
        
        % 初始状态向量 [x0, y0, z0, vx0, vy0, vz0, wx, wy, wz]
        initial_state = [0; 0; 0; v0x; v0y; v0z; omega_x; omega_y; omega_z];
        
        % 时间范围
        tspan = [0 10];
        
        % 使用 ode45 求解微分方程
        [~, state] = ode45(@(t, state) projectile(t, state), tspan, initial_state);
        
        % 计算位置
        x = state(:, 1);
        y = state(:, 2);
        z = state(:, 3);
        
        % 找到足球与球门所在平面的交点 (y = 10)
        y_position = state(:, 2);
        crossing_index = find(y_position > 10, 1);
        
        if isempty(crossing_index)
            F = [inf; inf];  % 没有找到交点，返回无限大错误
        else
            % 确保轨迹不超过 xz 平面
            x_hit = x(crossing_index);
            z_hit = z(crossing_index);
            
            % 计算与目标位置的差异
            F = [x_hit - goal_position(1); z_hit - goal_position(2)];
        end
    end
    
    function dstate = projectile(~, state)
        % 提取状态变量
        vx = state(4);
        vy = state(5);
        vz = state(6);
        omega = state(7:9);
        
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
        dstate(7) = 0;         % omega_x 恒定
        dstate(8) = 0;         % omega_y 恒定
        dstate(9) = 0;         % omega_z 恒定
    end
end
