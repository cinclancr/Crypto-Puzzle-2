#!/usr/bin/env python3
"""Reconstruct proposed Puzzle 2 video part2 C/A layers from original frames.

Segmentation is HYPOTHESIS-CONDITIONED; this script does not prove a key or font.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

PART1_ANCHORS=[1219,1221,1224,1226,1229,1231,1234,1237,1239,1242]
A_FRAMES=[1554,1578,1600]
C_FRAMES=[1568,1590,1611]


def video_frame(cap, index):
    import cv2
    cap.set(cv2.CAP_PROP_POS_FRAMES,index)
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError(f'Cannot decode zero-based frame {index}')
    return frame


def run():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--part2',type=Path,required=True)
    parser.add_argument('--part1',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--threshold',type=int,default=190)
    parser.add_argument('--pitch',type=int,default=75)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    import cv2
    import numpy as np
    from PIL import Image,ImageDraw
    cap=cv2.VideoCapture(str(args.part2))
    def get(n):
        f=video_frame(cap,n)
        return (cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)[115:605,620:664]>args.threshold).astype(np.uint8)
    aa=np.stack([get(i) for i in A_FRAMES]);cc=np.stack([get(i) for i in C_FRAMES]);cap.release()
    a=(aa.sum(axis=0)>=2).astype(np.uint8)
    c=(cc.sum(axis=0)>=2).astype(np.uint8)
    pixel_match={'A':[float((img==a).mean()) for img in aa], 'C':[float((img==c).mean()) for img in cc]}
    cv2.imwrite(str(args.output/'part2_layer_A.png'), a*255)
    cv2.imwrite(str(args.output/'part2_layer_C.png'), c*255)
    variants={'C_plus_A':np.concatenate([c,a],axis=1),'A_plus_C':np.concatenate([a,c],axis=1),
              'mirrorC_plus_A':np.concatenate([np.fliplr(c),a],axis=1),'C_plus_mirrorA':np.concatenate([c,np.fliplr(a)],axis=1)}
    for key,arr in variants.items(): cv2.imwrite(str(args.output/f'part2_{key}.png'),arr*255)
    raw=Image.fromarray(variants['C_plus_A']*255).convert('RGB')
    board=Image.new('RGB',(6*200,250),(20,25,35));d=ImageDraw.Draw(board)
    windows=[]
    for idx in range(6):
        y0=idx*args.pitch;y1=min(raw.height,y0+116)
        windows.append([y0,y1])
        patch=raw.crop((0,y0,raw.width,y1))
        if y0<raw.height and y1>y0:
            board.paste(patch.resize((176,205)),(idx*200+12,30))
        d.text((idx*200+12,7),f'Position {idx+1}',fill='white')
    board.save(args.output/'part2_six_windows_HYPOTHESIS.png')
    report={'part2_video':args.part2.name,'frames_A':A_FRAMES,'frames_C':C_FRAMES,'crop_yx':'gray[115:605,620:664]',
            'threshold':args.threshold,'pitch':args.pitch,'segmentation_hypothesis':'six glyphs/116px height',
            'pixel_agreement':pixel_match,'windows':[{'i':i+1,'y0':v[0],'y1':v[1]} for i,v in enumerate(windows)],
            'note':'No OCR/characters asserted or target tested; output supports blind visual inspection.'}
    if args.part1:
        ca=cv2.VideoCapture(str(args.part1))
        seam=Image.new('RGB',(10*200,450),(19,24,32))
        for i,n in enumerate(PART1_ANCHORS):
            f1=video_frame(ca,n);f2=video_frame(ca,n+19)
            right=f1[:,-180:];left=f2[:,:180]
            glyph=cv2.rotate(np.concatenate([right,left],axis=1),cv2.ROTATE_90_CLOCKWISE)
            patch=Image.fromarray(cv2.cvtColor(glyph,cv2.COLOR_BGR2RGB)).resize((180,360))
            seam.paste(patch,(i*200+10,35))
        ca.release();seam.save(args.output/'part1_edge_composite_lag19_HYPOTHESIS.png')
        report['part1_anchors']=PART1_ANCHORS;report['part1_lag']=19
    (args.output/'reconstruction_metadata.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('Wrote raw layers and alternative reconstructions to',args.output)


if __name__=='__main__':run()
