% 定义输入参数
target_position = [0, 10, 1];  % 球门中央，距起点10米高1.22米
initial_speed = 50;               % 初始速度 (m/s)
spin_speed = 5;                   % 自旋速度 (rad/s)
roll_angle = pi;              % Roll 角度 (radians)

% 调用逆向运动学求解函数
inverse_kinematics3(target_position, initial_speed, spin_speed, roll_angle);

