function untitled3
   % 初始化初始条件
    initial_conditions = struct('v0', 22, 'pitch', 10, 'yaw', 90, 'roll', 0, 'w', 0);
    
    % 创建图形窗口
    fig = figure('Name', '足球轨迹模拟', 'NumberTitle', 'off');
    
    % 创建表格，并在图形上显示初始条件
    uit = create_initial_conditions_table(fig, initial_conditions);
    
    % 首次绘制足球轨迹
    plot_soccer_trajectory(fig, initial_conditions);
    
    % 表格创建函数
    function uit = create_initial_conditions_table(fig, initial_conditions)
        uit = uitable(fig, 'Data', struct2cell(initial_conditions), ...
            'ColumnName', {'Value'}, ...
            'RowName', fieldnames(initial_conditions), ...
            'Position', [20, 350, 150, 130], ...
            'ColumnEditable', true, ...
            'CellEditCallback', @(src, event) update_initial_conditions(src, event));
    end

    % 更新初始条件的回调函数
    function update_initial_conditions(~, event)
        field = event.Source.Data{event.Indices(1), 1};  % 获取字段名
        new_data = event.NewData;
        
        % 尝试将输入数据转换为数值
        if ischar(new_data)
            new_data = str2double(new_data);
        end
        
        % 检查是否成功转换为数值
        if isnan(new_data)
            % 如果无法转换为数值，可能是字符串或其他非法输入，直接赋值
            initial_conditions.(field) = new_data;
        else
            % 成功转换为数值，更新结构体字段
            initial_conditions.(field) = new_data;
        end
        
        % 重新绘制足球轨迹
        plot_soccer_trajectory(fig, initial_conditions);
    end

    % 绘制足球轨迹函数
    function plot_soccer_trajectory(fig, initial_conditions)
        % 清除旧图形
        clf(fig);
        
        % 参数转换和计算
        v0 = initial_conditions.v0;
        pitch = deg2rad(initial_conditions.pitch);
        yaw = deg2rad(initial_conditions.yaw);
        roll = deg2rad(initial_conditions.roll);
        w = initial_conditions.w
        
        % 计算初始速度的分量
        v0x = v0 * cos(pitch) * cos(yaw);  % 水平分量 x
        v0y = v0 * cos(pitch) * sin(yaw);  % 水平分量 y
        v0z = v0 * sin(pitch);             % 垂直分量 z
        
        % 计算初始速度的单位方向向量
        v0_mag = sqrt(v0x^2 + v0y^2 + v0z^2);
        if v0_mag == 0
            v0_mag = eps;  % 防止除以零
        end
        v0_unit = [v0x; v0y; v0z] / v0_mag;
        
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
        crossing_index = find(y_position > 10, 1);
        
        % 绘制运动轨迹
        plot3(x, y, z, 'b-', 'LineWidth', 2);
        hold on;
        
        % 绘制出射点
        scatter3(0, 0, 0, 100, 'filled', 'k');
        
        % 绘制初始速度箭头
        quiver3(0, 0, 0, v0x, v0y, v0z, 'r', 'LineWidth', 2,'AutoScale','on');
        
        % 绘制自旋角速度箭头
        quiver3(0, 0, 0, omega(1), omega(2), omega(3), 'g', 'LineWidth', 2,'AutoScale','on');
       
        % 绘制球门
        goal_width = 7.32;  % 标准球门宽度 (m)
        goal_height = 2.44; % 标准球门高度 (m)
        goal_y = 10;
        
        % 定义球门的角点
        goal_x1 = -goal_width / 2;
        goal_x2 = goal_width / 2;
        goal_z1 = 0;
        goal_z2 = goal_height;
        
        % 绘制球门矩形
        plot3([goal_x1, goal_x2, goal_x2, goal_x1, goal_x1], ...
              [goal_y, goal_y, goal_y, goal_y, goal_y], ...
              [goal_z1, goal_z1, goal_z2, goal_z2, goal_z1], 'r-', 'LineWidth', 2);
        
        % 绘制大禁区
        penalty_area_width = 40.3;  % 大禁区宽度 (m)
        penalty_area_depth = 16.5;  % 大禁区深度 (m)
        penalty_x1 = -penalty_area_width / 2;
        penalty_x2 = penalty_area_width / 2;
        penalty_y = goal_y - penalty_area_depth;
        
        plot3([penalty_x1, penalty_x2, penalty_x2, penalty_x1, penalty_x1], ...
              [goal_y, goal_y, penalty_y, penalty_y, goal_y], ...
              [0, 0, 0, 0, 0], 'k-', 'LineWidth', 1.5);
        
        % 绘制小禁区
        goal_area_width = 18.32;  % 小禁区宽度 (m)
        goal_area_depth = 5.5;    % 小禁区深度 (m)
        goal_x1 = -goal_area_width / 2;
        goal_x2 = goal_area_width / 2;
        goal_area_y = goal_y - goal_area_depth;
        
        plot3([goal_x1, goal_x2, goal_x2, goal_x1, goal_x1], ...
              [goal_y, goal_y, goal_area_y, goal_area_y, goal_y], ...
              [0, 0, 0, 0, 0], 'k-', 'LineWidth', 1.5);
        
        if isempty(crossing_index)
            disp('足球未能到达球门平面');
        else
            % 确保轨迹不超过 xz 平面
            x_hit = x(crossing_index);
            z_hit = z(crossing_index);
            fprintf('足球打在球门平面上的位置：x = %.2f m, z = %.2f m\n', x_hit, z_hit);
            
            % 检查是否在球门范围内
            if abs(z_hit) <= goal_height && abs(x_hit) <= goal_width / 2
                disp('足球进门了！');
            else
                disp('足球未进门');
            end
            
            % 标记球打在球门平面上的位置
            plot3(x_hit, goal_y, z_hit, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
        end
        
        xlabel('水平距离 x (m)');
        ylabel('水平距离 y (m)');
        zlabel('垂直距离 z (m)');
        title('足球运动轨迹');
        grid on;
        axis equal;  % 调整坐标轴比例，使 x, y, z 间距合理
        xlim([-penalty_area_width, penalty_area_width]);
        ylim([0, 1.5*goal_y]);
        zlim([0, goal_height * 2]);

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
   
                Fm = Cl * 0.5 * rho * A * cross(omega, velocity) ;
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
     uit = create_initial_conditions_table(fig, initial_conditions);
    end
end
