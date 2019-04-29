%Spectrogram
Spectra = dsp.SpectrumAnalyzer('SampleRate',Fs,'PlotAsTwoSidedSpectrum',false,...
                               'SpectralAverages',20,'FrequencyScale','Log');
%Time Scope - 2 channels                          
scope=dsp.TimeScope('SampleRate',Fs,'NumInputPorts',2,'TimeSpan',30,'BufferLength',2.4e6,'YLimits',[-1.5 1.5])                           

freq_in_co=8000/Fs*200;
freq_in_min=8000/Fs*50;
Nb=3;
max_time=5;
min_power=11;

Tval=19.7;
Tval_diff=3;
Tval_diff_d=-3;
time_iter=N/Fs;

err_sig=[];
CurrentState='wait1';
code=[];
code_out=[];

iter=0;
loop=0;
LastTime=0;
CurrentTime=0;
code=zeros(1,3);

lastValue1=0;
lastValue2=0;
lastValue3=0;

CurrentTime=0;
freq_out=[];
power_last=0;

place_holder=[];
e=0;

last_in_1=-2;
last_in_2=-2;
last_in_3=-2;

while ~isDone(afr)
    iter=iter+1;
    audioIn=afr();
    [in_max,power_out,freqn_out]=freqcheck(audioIn,freq_in_min,freq_in_co);
    err_sig=[err_sig,power_out];
    freq_out=[freq_out freqn_out];
    power_diff=power_out-power_last;
    if(power_out>=Tval)&&(in_max~=-1)
        e=ones(size(audioIn));
        place_holder=[place_holder 100];
    else
        e=zeros(size(audioIn));
        place_holder=[place_holder 0];
    end
    power_last=power_out;

    switch CurrentState
        case 'wait1'
           
            if e==0
                LastTime=CurrentTime;
                CurrentState='wait1';
            else
                LastTime=iter*time_iter;
                if (in_max==-1)
                    CurrentState='wait1';
                    e=zeroes(size(audioIn));
                else
                CurrentState='one';
                code(1)=in_max;
                end
            end
            
            
        case 'one'
            if e==0
                if(power_out< min_power)||(in_max==-1)
                CurrentState='wait2';
                LastTime=iter*time_iter;
                lastValue1=0;
                last_in_1=-2;
                else
                    e=ones(size(audioIn));
                end
            else 
                last_in_1=in_max;
                if (lastValue1<power_out)
                    lastValue1=power_out;
                    code(1)=in_max;
                else
                    CurrentState='one';
                end
            end     
            
        case 'wait2'
            if e==0
                CurrentState='wait2';
            else
                if(in_max==-1)
                    CurrentState='wait2';
                    e=zeros(size(audioIn));
                else
                CurrentState='two';
                code(2)=in_max;
                end
            end
            
            
        case 'two'
            if e==0
                if (power_out<min_power)||(in_max==-1)
                CurrentState='wait3';
                LastTime=iter*time_iter;
                lastValue2=0;
                last_in_2=-2;
                else
                e=ones(size(audioIn));
                end
            else
                last_in_2=in_max;
                if lastValue2<power_out;
                    lastValue2=power_out;
                    code(2)=in_max;
                else
                    CurrentState='two';
                end
            end
        case 'wait3'
            if e==0
                CurrentState='wait3';
            else 
                LastTime=iter*time_iter;
                if(in_max==-1)
                    CurrentState='wait3';
                    e=zeros(size(audioIn));
                else
                    CurrentState='three';
                    code(3)=in_max;
                end
            end
         case 'three'
             if e==0
                if (power_out<min_power)||(in_max==-1)
                CurrentState='wait1';
                code_transfer=convert2bin(code);
                code_out=[code_out code_transfer];
                code=zeros(1,3);
                LastTime=iter*time_iter;
                lastValue3=0;
                last_in_3=-2;
            else
                e=ones(size(audioIn));
            end
          else 
                last_in_3=in_max;
                if(lastValue3<power_out)
                    lastValue3=power_out;
                    code(3)=in_max;
                else
                    CurrentState='three';
                end
            end
    end
    CurrentTime=iter*time_iter;
    if(max_time<CurrentTime-LastTime)&&(~strcmp(CurrentState,'wait1'))
        CurrentState='wait1';
        code=zeros(1,3);
        err_state='TIMED OUT HERE';
    end
    scope(audioIn,e);
end

code_out


function [y f freq_n]=freqcheck(x,freq_in_min,freq_in_co)

    X=fft(x);
    [yy kk]=max(abs(X(1:512)));
    freq_n=kk;
    f=yy;
    if kk<freq_in_min;
        y=-1;
    elseif (kk<freq_in_co)&&(kk>freq_in_min)
        y=0;
    else
        y=1;
    end
    
end

function y=convert2bin(code)
    code=flip(code);
    values=0;
    code_length=length(code);
 for n=0:code_length-1
        if code(n+1)==1
            values=values+2^n;
        end
    end
    y=values;
end
