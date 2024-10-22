from wpilib import AddressableLED
class LED:
    def __init__(self):
        if not hasattr(self, 'led'):
            self.led = AddressableLED(0)  # 使用PWM端口0
            self.led_buffer = [AddressableLED.LEDData(0, 0, 0) for _ in range(60)]  
            self.led.setLength(len(self.led_buffer))
            self.led.setData(self.led_buffer)
            self.led.start()
            self.blink_state = False
            self.counter = 0
      
    def set_color(self, r: int, g: int, b: int, brightness: float = 1.0):
        """设置所有LED的颜色并调节亮度"""
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
    
        for i in range(len(self.led_buffer)):
            self.led_buffer[i].setRGB(r, g, b)
        self.led.setData(self.led_buffer)
    
    def blink(self,r: int, g: int, b: int, brightness: float = 1.0):
        """控制LED闪烁"""
        self.counter += 1
        if self.counter % 10 == 0:  # 控制闪烁频率
            self.blink_state = not self.blink_state
            if self.blink_state:
                self.set_color(r* brightness,g* brightness,b* brightness)  # 开启绿色
            else:
                self.set_color(0, 0, 0)  # 关闭