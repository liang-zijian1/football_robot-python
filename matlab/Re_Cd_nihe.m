clear all
clc
subplot(1,1,1);
Reex=[10 15 20 25 30 40 50 60 70 80 90 100 125 150 175 200];  %表格雷诺数
Rein=1./Reex;
Cdex=[4.3178 3.2805 2.7240 2.3700 2.1218 1.7917 1.5785 1.4272 1.3131 1.2233 1.1503 1.0895 0.97316 0.88887 0.82396 0.77176];  %表格阻力系数
Cdin=1 ./ Cdex;
Cdexp=log(Cdex-0.76);
plot(Reex,Cdex)  %蓝色原始数据
hold on
Cn1=polyfit((Reex-6),Cdexp,1);  %指数函数拟合，前段不准
Cn2=polyfit(Rein.^0.9,Cdex,1);  %幂函数拟合，后段不准
Reex=10:1:200;
Cdnh1=exp(Cn1(1).*Reex+Cn1(2))+0.76;
Cdnh2=Cn2(1)./Reex.^0.9+Cn2(2);
%plot(Reex,Cdnh1)
%plot(Reex,Cdnh2)
Cdnh=(atan((exp(Reex)-exp(25))./exp(24))./1.5708+1)./2.*Cdnh1+(1-(atan((exp(Reex)-exp(25))./exp(24))./1.5708+1)./2).*Cdnh2;
plot(Reex,Cdnh)