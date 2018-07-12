close all; clear all;
bitrate = [1;2;4;8;16];

coaster_tr = csvread('matlab_WSPSNR_coaster_TR.csv');
coaster_vpr = csvread('matlab_VPSNR_coaster_VPR.csv');
game_tr = csvread('matlab_WSPSNR_game_TR.csv');
game_vpr = csvread('matlab_VPSNR_game_VPR.csv');
panel_tr = csvread('matlab_WSPSNR_panel_TR.csv');
panel_vpr = csvread('matlab_VPSNR_panel_VPR.csv');

figure;
coaster_gain=coaster_vpr-coaster_tr;
game_gain=game_vpr-game_tr;
panel_gain=panel_vpr-panel_tr;
load census;
%TR
[cg, cg_gof] = fit(bitrate, coaster_gain, 'poly2');
[gg, gg_gof] = fit(bitrate, game_gain, 'poly2');
[pg, pg_gof] = fit(bitrate, panel_gain, 'poly2');
h1 = plot(cg, bitrate, coaster_gain, 'ro');
hold on;
h2 = plot(gg, bitrate, game_gain, 'b*');
hold on;
h3 = plot(pg, bitrate, panel_gain, 'g+');
grid on;

LH(1) = plot(nan, nan, 'ro');
L{1} = 'NI, fast-paced';
LH(2) = plot(nan, nan, 'b*');
L{2} = 'CG, fast-paced';
LH(3) = plot(nan, nan, 'g+');
L{3} = 'NI, slow-paced';
LH(4) = plot(nan, nan, 'r-');
L{4} = 'Fitted Curve';

axis([0 17 0 10]);
set(gca, 'xtick', (0:4:17), 'ytick', (0:2:10));
xlabel('Bitrate (Mbps)');
ylabel('Video Quality Gain');
legend(LH, L);

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