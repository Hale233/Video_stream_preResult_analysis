import csv
import random
def from_index_get_pcapname_test(index_path,record_path):
    index_file = open(index_path, mode='r', encoding='utf-8')
    csvfile = open(record_path, 'a')
    writer = csv.writer(csvfile)
    list=[]
    index_datas=index_file.read().split('\n')
    for index_data in index_datas:
        beg=index_data.find('"ACK_flag":')
        end=index_data.find(',"dst_SNI":')
        #list.append(index_data[beg+11:end])
        writer.writerow([index_data[beg+11:end]])
    #print(list)
    index_file.close()
    csvfile.close()

def SNI_data_analysis(index_path,record_path):
    video_finger_flie=open('./finger/video_finger.txt', mode='r', encoding='utf-8')
    nonvideo_finger_flie = open('./finger/no_video_finger.txt', mode='r', encoding='utf-8')
    index_file = open(index_path, mode='r', encoding='utf-8')
    csvfile = open(record_path+'all_SNI.csv', 'w')
    video_csv=open(record_path+'video_SNI.csv', 'w')
    non_video_csv = open(record_path + 'nonvideo_SNI.csv', 'w')
    unknow_csv=open(record_path + 'unknow_SNI.csv', 'w')

    next_analyxix_video_file=open('./next_video.txt', mode='w', encoding='utf-8')
    next_analyxix_nonvideo_file = open('./next_nonvideo.txt', mode='w', encoding='utf-8')

    unknow_SNI_writer=csv.writer(unknow_csv)
    video_SNI_writer=csv.writer(video_csv)
    nonvideo_SNI_writer = csv.writer(non_video_csv)
    all_SNI_writer = csv.writer(csvfile)

    list = []
    SNI=[]
    SNI_dict={}
    video_fingers=[]
    nonvideo_fingers=[]

    video_finger_datas=video_finger_flie.read().split('\n')
    nonvideo_finger_datas=nonvideo_finger_flie.read().split('\n')

    for video_finger_data in video_finger_datas:
        video_fingers.append(video_finger_data)
    #print(video_fingers)

    for nonvideo_finger_data in nonvideo_finger_datas:
        nonvideo_fingers.append(nonvideo_finger_data)
    #print(nonvideo_fingers)

    index_datas = index_file.read().split('\n')

    for index_data in index_datas:
        for video_finger in video_fingers:
            if index_data.find(video_finger)>0:
                next_analyxix_video_file.write(index_data)
                next_analyxix_video_file.write('\n')
                break
        for nonvideo_finger in nonvideo_fingers:
            if index_data.find(nonvideo_finger)>0:
                next_analyxix_nonvideo_file.write(index_data)
                next_analyxix_nonvideo_file.write('\n')
                break

    for index_data in index_datas:
        lines=index_data.split(',"')
        list.append(lines)
    for data in list:
        SNI.append(data[-1][data[-1].find(':')+1:-1])

    for key in SNI:
        SNI_dict[key]=SNI_dict.get(key,0)+1
    SNI_dict=sorted(SNI_dict.items(), key=lambda kv: (kv[1], kv[0]),reverse = True)
    for val in SNI_dict:
        all_SNI_writer.writerow([val[0],val[1]])
        video_flag=0
        nonvideo_flag=0
        for video_finger in video_fingers:
            if val[0].find(video_finger)>0:
                video_SNI_writer.writerow([val[0],val[1]])
                #print(val[0])
                video_flag=1
                break
        for nonvideo_finger in nonvideo_fingers:
            if val[0].find(nonvideo_finger)>0:
                nonvideo_SNI_writer.writerow([val[0],val[1]])
                nonvideo_flag=1
                break
        if video_flag==0 and nonvideo_flag==0:
            unknow_SNI_writer.writerow([val[0],val[1]])

    csvfile.close()
    video_csv.close()
    non_video_csv.close()
    unknow_csv.close()

    next_analyxix_video_file.close()
    next_analyxix_nonvideo_file.close()

    #print(SNI_dict)

def flag_data_analysis(index_path,record_path):
    index_file = open(index_path, mode='r', encoding='utf-8')
    #csvfile = open(record_path, 'w')
    #writer = csv.writer(csvfile)
    list = []
    SSL=[]
    ML=[]
    RULE=[]
    ACK=[]
    flag=[]
    SSL_dict={}
    ML_dict = {}
    RULE_dict = {}
    ACK_dict = {}

    count001=0
    count010 = 0
    count011 = 0
    count100 = 0
    count101 = 0
    count110 = 0
    count111 = 0

    index_datas = index_file.read().split('\n')
    for index_data in index_datas:
        lines=index_data.split(',"')
        list.append(lines)
    for data in list:
        SSL.append(data[-5][data[-5].find(':') + 1:])#SSL flag
        ML.append(data[-4][data[-4].find(':') + 1:])#ML flag
        RULE.append(data[-3][data[-3].find(':') + 1:])#RLUE flag
        ACK.append(data[-2][data[-2].find(':') + 1:])#ACK flag
        flag.append([int(data[-4][data[-4].find(':') + 1:]),int(data[-3][data[-3].find(':') + 1:]),int(data[-2][data[-2].find(':') + 1:])])

    for val in flag:
        if(val[0]==0 and val[1]==0 and val[2]!=0):
            count001 =count001+1
        if (val[0] == 0 and val[1] != 0 and val[2] == 0):
            count010 += 1
        if (val[0] == 0 and val[1] != 0 and val[2] != 0):
            count011 += 1
        if (val[0] != 0 and val[1] == 0 and val[2] == 0):
            count100 += 1
        if (val[0] != 0 and val[1] == 0 and val[2] != 0):
            count101 += 1
        if (val[0] != 0 and val[1] != 0 and val[2] == 0):
            count110 += 1
        if (val[0] != 0 and val[1] != 0 and val[2] != 0):
            count111 += 1
    print(count001,count010,count011,count100,count101,count110,count111)


    for key in SSL:
        SSL_dict[key]=SSL_dict.get(key,0)+1
    #SSL_dict=sorted(SSL_dict.items(), key=lambda kv: (kv[1], kv[0]),reverse = True)
    for key in ML:
        ML_dict[key]=ML_dict.get(key,0)+1
    #ML_dict=sorted(ML_dict.items(), key=lambda kv: (kv[1], kv[0]),reverse = True)
    for key in RULE:
        RULE_dict[key]=RULE_dict.get(key,0)+1
    #RULE_dict=sorted(RULE_dict.items(), key=lambda kv: (kv[1], kv[0]),reverse = True)
    for key in ACK:
        ACK_dict[key]=ACK_dict.get(key,0)+1
    ACK_dict=sorted(ACK_dict.items(), key=lambda kv: (kv[1], kv[0]),reverse = True)
    print('SSL{},ML{},RULE{},ACK{}'.format(SSL_dict,ML_dict,RULE_dict,ACK_dict))
    #for val in SNI_dict:
        #writer.writerow([val[0],val[1]])


if __name__ == '__main__':
    flag_data_analysis('./next_video.txt', './result/')
    #SNI_data_analysis('./temp.txt', './result/')