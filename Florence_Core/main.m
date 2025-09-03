path(path,'./WORLD');path(path,'./midi');
[x,fs] = audioread("res\一.wav");
output = zeros(1,ceil(result{end,end}*fs));
for i = 1:size(result,1)
    file = './res/'+result{i,1}+'.wav';
    [tmp,fs] = WorldSynthesizer(file,[],result{i,2},[],result{i,4}-result{i,3});
    sound(tmp,fs)
    pause(result{i,4}-result{i,3})
end
