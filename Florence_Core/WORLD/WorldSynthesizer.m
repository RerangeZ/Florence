function [y,fs] = WorldSynthesizer(input_filename, output_filename, f0_param, spec_param, time_param)
% F0をシフト，スペクトルの伸縮，発話時間の伸縮を実施する関数
% 書式：WorldSynthesizer(input_filename, output_filename, f0_param, spec_param, time_param)
% 例題：WorldSynthesizer('vaiueo2d.wav', 'output.wav', 1, 1, 1);
% input_filename = 'vaiueo2d.wav';
% output_filename = 'output.wav';
% f0_param = 2;
% spec_param = 1;
% time_param = 1;

[x, fs] = audioread(input_filename);

f0_parameter = Harvest(x, fs);

spectrum_parameter = CheapTrick(x, fs, f0_parameter);
source_parameter = D4C(x, fs, f0_parameter);

% F0変更
source_parameter.f0 = ones(size(f0_parameter.f0))*f0_param;
% source_parameter.f0(1:100) = source_parameter.f0(1:100)*2;

% % 频谱伸縮
% fft_size = (size(spectrum_parameter.spectrogram, 1) - 1) * 2;
% w = (0 : fft_size - 1) * fs / fft_size;
% w2 = (0 : fft_size / 2) * fs / fft_size / spec_param;
% for i = 1 : size(spectrum_parameter.spectrogram, 2)
%   tmp = [spectrum_parameter.spectrogram(:, i); spectrum_parameter.spectrogram(end - 1 : -1 : 2, i)];
%   spectrum_parameter.spectrogram(:, i) = iterp1(w, tmp, w2, 'linear', 'extrap');
% end

% 発話時間の伸縮
rate = time_param / f0_parameter.temporal_positions(1,end);
source_parameter.temporal_positions = source_parameter.temporal_positions * rate;

y = Synthesis(source_parameter, spectrum_parameter);

max1 = max(y);
y = y./max1;

% audiowrite(output_filename, y, fs);