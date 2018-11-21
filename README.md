# Hesai-lidar-pcap-file-read-as-pointset
read pcap files (Hesai lidar device) as point cloud.

#read target pcap file
pcap_packet_data = PcapFileReadAsPointset(targetfilepath)
#The point cloud is separated, 360 degrees, angular resolution =1 degrees.
radar_frame_set  = Radar_data_split(pcap_packet_data)
