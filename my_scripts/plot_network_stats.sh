#!/bin/bash
# Author: jseefive
# Create Date: 2021/4/24
# Discription: Scripts to plot network stats of mesh_3D synthetic traffic simulation.
# Usage: running ./my_scripts/graduation_proj/plot_network_stats.sh under the gem5 directory.

# traffic pattern list
traffic_pattern=(' ' 'uniform_random' 'tornado' 'bit_complement' 'bit_reverse' 'bit_rotation' 'neighbor' 'shuffle' 'transpose')
topology=(' ' 'NoI_ButterDonut_X' 'NoI_FoldedTorus_X' 'NoI_DoubleButterfly_X' 'NoI_FoldedTorus_X' 'NoI_KiteSmall' 'NoI_Mesh')
#echo "${traffic_pattern[i]}"

pre_process(){

# create injection rate file
# three topology 
for h in `seq 1 1`
do
	inj_rate=0
	interval=0.02
	for i in `seq 1 15`
	do
		if [ "$i" -gt "20" ]; then
			interval=0.02
		fi
		# injection rate
		inj_rate=$(echo "$inj_rate+$interval"|bc)
		echo "$inj_rate" >> m5out/${topology[h]}/stats/injection_rate.txt
	done
done


for h in `seq 1 1`
do
	mkdir m5out/${topology[h]}/stats/throughput_plot
	mkdir m5out/${topology[h]}/stats/hops_plot
	mkdir m5out/${topology[h]}/stats/latency_plot
done

for h in `seq 1 1`
do
	# pre-process
	# calculate throughput
	for j in `seq 1 1`
	# traffic pattern from 1 'uniform_random' to 8 'transpose'
	do
		for k in `seq 2 2`
		do
			for line in `cat  m5out/${topology[h]}/stats/${traffic_pattern[j]}/flits_received_exp_$k.txt`
			do
				throughput=$(echo "scale=4; $line" | bc)
				echo $throughput >> m5out/${topology[h]}/stats/${traffic_pattern[j]}/throughput_exp_$k.txt
			done

			for line in `cat  m5out/${topology[h]}/stats/${traffic_pattern[j]}/latency_exp_$k.txt`
			do
				latency=$(echo "scale=4; $line / 5" | bc)
				echo $latency >> m5out/${topology[h]}/stats/${traffic_pattern[j]}/cycles_exp_$k.txt
			done
		done
	done
done

for h in `seq 1 1`
do	
	# merge data file
	for j in `seq 1 1`
	# traffic pattern from 1 'uniform_random' to 8 'transpose'
	do
		for k in `seq 2 2`
		do
			paste m5out/${topology[h]}/stats/injection_rate.txt m5out/${topology[h]}/stats/${traffic_pattern[j]}/throughput_exp_$k.txt > m5out/${topology[h]}/stats/throughput_plot/${traffic_pattern[j]}.txt	
			paste m5out/${topology[h]}/stats/injection_rate.txt m5out/${topology[h]}/stats/${traffic_pattern[j]}/hops_exp_$k.txt > m5out/${topology[h]}/stats/hops_plot/${traffic_pattern[j]}.txt
			paste m5out/${topology[h]}/stats/injection_rate.txt m5out/${topology[h]}/stats/${traffic_pattern[j]}/cycles_exp_$k.txt > m5out/${topology[h]}/stats/latency_plot/${traffic_pattern[j]}.txt
		done
	done
done

}

plot_throughput(){

# plot and save the throughput graph
#   \"m5out/NoI_ButterDonut_X/stats/throughput_plot/uniform_random.txt\" smooth unique with linespoints linecolor 2 linewidth 1.5 pointtype 2 pointsize 2 title \"tornado\", \
#     \"m5out/NoI_KiteSmall/stats/throughput_plot/uniform_random.txt\" smooth unique with linespoints linecolor 3 linewidth 1.5 pointtype 3 pointsize 2 title \"bit complement\", \
echo "
set term pngcairo font \",18\"
set title \"Throughput - Injection Rate\"
set xlabel \"Injection rate(flits/node/cycle)\"
set ylabel \"Throughput(flits/node/cycle)\"
set title font ',25'
set xlabel font ',22'
set ylabel font ',22'
set tics font ',18'
set key font ',16'
set grid
set key box
set key top left
set terminal pngcairo size 1280, 720
set output \"m5out/NoI_ButterDonut_X/stats/throughput.png\"

plot \"m5out/NoI_ButterDonut_X/stats/throughput_plot/uniform_random.txt\" smooth unique with linespoints linecolor 1 linewidth 1.5 pointtype 1 pointsize 2 title \"uniform random\", \
" | gnuplot
}

plot_hops(){

# plot and save the hops graph
#     \"m5out/NoI_ButterDonut_X/stats/hops_plot/uniform_random.txt\" smooth unique with linespoints linecolor 2 linewidth 1.5 pointtype 2 pointsize 2 title \"tornado\", \
#     \"m5out/NoI_KiteSmall/stats/hops_plot/uniform_random.txt\" smooth unique with linespoints linecolor 3 linewidth 1.5 pointtype 3 pointsize 2 title \"bit complement\", \     
echo "
set term pngcairo font \",18\"
set title \"Hops - Injection Rate\"
set xlabel \"Injection rate(flits/node/cycle)\"
set ylabel \"Hops\"
set title font ',25'
set xlabel font ',22'
set ylabel font ',22'
set tics font ',18'
set key font ',16'
set grid
set key box
set key top left
set terminal pngcairo size 1280, 720
set output \"m5out/NoI_Mesh/stats/hops.png\"

plot \"m5out/NoI_Mesh/stats/hops_plot/uniform_random.txt\" smooth unique with linespoints linecolor 1 linewidth 1.5 pointtype 1 pointsize 2 title \"uniform random\", \

" | gnuplot
}

plot_latency(){

# plot and save the latency graph
#     \"m5out/NoI_ButterDonut_X/stats/latency_plot/uniform_random.txt\" smooth unique with linespoints linecolor 2 linewidth 1.5 pointtype 2 pointsize 2 title \"tornado\", \
#     \"m5out/NoI_KiteSmall/stats/latency_plot/uniform_random.txt\" smooth unique with linespoints linecolor 3 linewidth 1.5 pointtype 3 pointsize 2 title \"bit complement\", \    
   
echo "
set term pngcairo font \",18\"
set title \"Average Packet Latency - Injection Rate\"
set xlabel \"Injection rate(flits/node/cycle)\"
set ylabel \"Average packet latency(cycle)\"
set title font ',25'
set xlabel font ',22'
set ylabel font ',22'
set tics font ',18'
set key font ',16'
set grid
set key box
set key top left
set terminal pngcairo size 1280, 720
set output \"m5out/NoI_ButterDonut_X/stats/latency.png\"


plot \"m5out/NoI_ButterDonut_X/stats/latency_plot/uniform_random.txt\" smooth unique with linespoints linecolor 1 linewidth 1.5 pointtype 1 pointsize 2 title \"uniform random\", \
" | gnuplot
}

#pre_process
plot_throughput
#plot_hops
plot_latency
exit 0
