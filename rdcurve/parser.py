import os
import sys
import subprocess 

video = sys.argv[1]
mode = sys.argv[2]
bitrate = ["1Mbps", "2Mbps", "4Mbps", "8Mbps", "16Mbps"]

if mode == "TR":
    for i in range(1, 2):
        for b in range(0, len(bitrate)):
            filename = "psnr_" + video + "_" + bitrate[b] + "_" + mode + ".csv"
            if os.path.isfile(filename):
                os.remove(filename)
            for j in range(1, 29):
                #cat PSNR/TR/psnr_coaster_user01_*_1Mbps_TR.csv | head -n 112 | tail -n 1 >> psnr_coaster_1Mbps_TR.csv
                if j == 28:
                    command1 = "cat ./PSNR/" + mode + "/psnr_" + video + "_user" + str(i).zfill(2) + "_" + str(j) + "_" + bitrate[b] + "_" + mode + ".csv" + " | head -n 120 | tail -n 1 >> " + filename
                else:
                    command1 = "cat ./PSNR/" + mode + "/psnr_" + video + "_user" + str(i).zfill(2) + "_" + str(j) + "_" + bitrate[b] + "_" + mode + ".csv" + " | head -n 112 | tail -n 1 >> " + filename
                print(command1)
                subprocess.call(command1, shell=True)

    for i in range(1, 2):
        for b in range(0, len(bitrate)):
            for j in range(1, 29):
                filename = "psnr_" + video + "_" + bitrate[b] + "_" + mode + ".csv"
                command2 = "cat ./PSNR/" + mode + "/psnr_" + video + "_user" + str(i).zfill(2) + "_" + str(j) + "_" + bitrate[b] + "_" + mode + ".csv" + " | tail -n 1 | awk '{print $2}' >> " + filename
                subprocess.call(command2, shell=True)

    for b in range(0, len(bitrate)):
        filename = "psnr_" + video + "_" + bitrate[b] + "_" + mode + ".csv"
        f = open(filename, "r")

        own = []
        psnr = []
        spsnr_nn = []
        spsnr_i = []
        wspsnr = []
        for i in range(0, 56):
            line = f.readline().strip().split('  | ')
            if i < 28:
                psnr.append(float(line[0][:7]))
                spsnr_nn.append(float(line[1][:7]))
                wspsnr.append(float(line[2][:7]))
                spsnr_i.append(float(line[3][:7]))
            else:
                own.append(float(line[0]))

        own_psnr = sum(own) / len(own)
        avg_psnr = sum(psnr) / len(psnr)
        avg_spsnr_nn = sum(spsnr_nn) / len(spsnr_nn)
        avg_wspsnr = sum(wspsnr) / len(wspsnr)
        avg_spsnr_i = sum(spsnr_i) / len(spsnr_i)

        out = open(filename, "a")
        out.write("\nown_psnr: %0.4f" % own_psnr)
        out.write("\navg_psnr: %0.4f" % avg_psnr)
        out.write("\navg_spsnr_nn: %0.4f" % avg_spsnr_nn)
        out.write("\navg_wspsnr: %0.4f" % avg_wspsnr)
        out.write("\navg_spsnr_i: %0.4f" % avg_spsnr_i)

        f1 = open("matlab_" + "PSNR_" + video + "_" + mode + ".csv", "a")
        f1.write("%0.4f\n" % avg_psnr)

        f2 = open("matlab_" + "SPSNRNN_" + video + "_" + mode + ".csv", "a")
        f2.write("%0.4f\n" % avg_spsnr_nn)

        f3 = open("matlab_" + "WSPSNR_" + video + "_" + mode + ".csv", "a")
        f3.write("%0.4f\n" % avg_wspsnr)

        f4 = open("matlab_" + "SPSNRI_" + video + "_" + mode + ".csv", "a")
        f4.write("%0.4f\n" % avg_spsnr_i)

        f5 = open("matlab_" + "OWNPSNR_" + video + "_" + mode + ".csv", "a")
        f5.write("%0.4f\n" % own_psnr)


if mode == "VPR":
    for i in range(1, 2):
        for b in range(0, len(bitrate)):
            filename = "psnr_" + video + "_" + bitrate[b] + "_" + mode + ".csv"
            if os.path.isfile(filename):
                os.remove(filename)
            for j in range(1, 29):
                if j == 28:
                    command1 = "cat ./PSNR/" + mode + "/psnr_" + video + "_user" + str(i).zfill(2) + "_" + str(j) + "_" + bitrate[b] + "_" + mode + ".csv" + " | head -n 81 | tail -n 1 >> " + filename
                else:
                    command1 = "cat ./PSNR/" + mode + "/psnr_" + video + "_user" + str(i).zfill(2) + "_" + str(j) + "_" + bitrate[b] + "_" + mode + ".csv" + " | head -n 73 | tail -n 1 >> " + filename
                print(command1)
                subprocess.call(command1, shell=True)

    for i in range(1, 2):
        for b in range(0, len(bitrate)):
            for j in range(1, 29):
                filename = "psnr_" + video + "_" + bitrate[b] + "_" + mode + ".csv"
                command2 = "cat ./PSNR/" + mode + "/psnr_" + video + "_user" + str(i).zfill(2) + "_" + str(j) + "_" + bitrate[b] + "_" + mode + ".csv" + " | tail -n 1 | awk '{print $2}' >> " + filename
                subprocess.call(command2, shell=True)

    for b in range(0, len(bitrate)):
        filename = "psnr_" + video + "_" + bitrate[b] + "_" + mode + ".csv"
        f = open(filename, "r")

        own = []
        vpsnr = []
        for i in range(0, 56):
            line = f.readline().strip()
            if i < 28:
                subline = line[line.find('Y'):]
                Y = float(subline[2:subline.find('U')])
                U = float(subline[subline.find('U')+2:subline.find('V')])
                V = float(subline[subline.find('V')+2:])
                vpsnr.append((Y+U+V)/3)
            else:
                own.append(float(line))

        own_psnr = sum(own) / len(own)
        avg_vpsnr = sum(vpsnr) / len(vpsnr)

        out = open(filename, "a")
        out.write("\nown_psnr: %0.4f" % own_psnr)
        out.write("\navg_psnr: %0.4f" % avg_vpsnr)

        f1 = open("matlab_" + "PSNR_" + video + "_" + mode + ".csv", "a")
        f1.write("%0.4f\n" % own_psnr)

        f2 = open("matlab_" + "VPSNR_" + video + "_" + mode + ".csv", "a")
        f2.write("%0.4f\n" % avg_vpsnr)
