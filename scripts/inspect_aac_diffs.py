#!/usr/bin/env python3
"""Compare indexed AAC packets by SHA256 content; a packet difference is NOT a decoded clue."""
import argparse,csv,json,subprocess
from pathlib import Path


def audio_packet_hashes(video):
    out=subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_packets',
         '-show_entries','packet=pts_time,size,data_hash','-show_data_hash','sha256','-of','json',str(video)],text=True)
    data=json.loads(out)
    return [(x.get('pts_time',''),x.get('size',''),x.get('data_hash','')) for x in data['packets']]


def run():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--part1',type=Path,required=True)
    p.add_argument('--part2',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    p1=audio_packet_hashes(args.part1);p2=audio_packet_hashes(args.part2)
    with args.output.open('w',newline='') as fp:
        w=csv.writer(fp);w.writerow(['packet_index','part1_pts','part2_pts','part1_size','part2_size','identical_hash'])
        for i in range(max(len(p1),len(p2))):
            a=p1[i] if i<len(p1) else ('','','')
            b=p2[i] if i<len(p2) else ('','','')
            w.writerow([i,a[0],b[0],a[1],b[1],a[2]==b[2] if a[2] and b[2] else False])
    print('Packet counts:',len(p1),len(p2),'identical indexed hashes:',sum(a[2]==b[2] for a,b in zip(p1,p2)))
    print('Saved',args.output)

if __name__=='__main__':run()
