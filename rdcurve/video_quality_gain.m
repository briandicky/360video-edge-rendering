close all; clear all;
bitrate = [1;2;4;8;16];

tr = csvread('matlab_SPSNRI_coaster_TR.csv');
vpr = csvread('matlab_VPSNR_coaster_VPR.csv');

figure;
gain=vpr-tr;
load census;
%TR
[g, g_gof] = fit(bitrate, gain, 'poly2');
plot(g, bitrate, gain, 'o');
%plot(bitrate, gain);
hold on;
%plot(bitrate, gain, 'b-o');


axis([0 17 0 6]);
set(gca, 'xtick', [0:4:19], 'ytick', [0:2:6]);
xlabel('Bitrate (Mbps)');
ylabel('Video Quality Gain');
legend('Sample (R-Square=0.9549)' ,'Fitted Curve');


 % for 3-column figures
set(gca,'FontSize',20)
set(gca, 'FontName', 'Times New Roman');
set(gca,'TickDir','out')
set(get(gca, 'xlabel'), 'interpreter', 'latex');
set(get(gca, 'xlabel'), 'FontName', 'Times New Roman');
set(get(gca, 'xlabel'), 'FontSize', 20);
set(get(gca, 'ylabel'), 'interpreter', 'latex');
set(get(gca, 'ylabel'), 'FontName', 'Times New Roman');
set(get(gca, 'ylabel'), 'FontSize', 20);
set(legend(), 'interpreter', 'latex');
set(legend(), 'FontName', 'Times New Roman');
set(legend(), 'FontSize', 20);
set(gcf, 'WindowStyle', 'normal');
set(gca, 'Unit', 'inches');
set(gca, 'Position', [.65 .65 4.6 3.125]);
set(gcf, 'Unit', 'inches');
set(gcf, 'Position', [0.25 2.5 5.5 4.05]);

 % for 3-column figures
set(gca,'FontSize',20)
set(gca, 'FontName', 'Times New Roman');
set(gca,'TickDir','out')
set(get(gca, 'xlabel'), 'interpreter', 'latex');
set(get(gca, 'xlabel'), 'FontName', 'Times New Roman');
set(get(gca, 'xlabel'), 'FontSize', 20);
set(get(gca, 'ylabel'), 'interpreter', 'latex');
set(get(gca, 'ylabel'), 'FontName', 'Times New Roman');
set(get(gca, 'ylabel'), 'FontSize', 20);
set(legend(), 'interpreter', 'latex');
set(legend(), 'FontName', 'Times New Roman');
set(legend(), 'FontSize', 20);
set(gcf, 'WindowStyle', 'normal');
set(gca, 'Unit', 'inches');
set(gca, 'Position', [.65 .65 4.6 3.125]);
set(gcf, 'Unit', 'inches');
set(gcf, 'Position', [0.25 2.5 5.5 4.05]);