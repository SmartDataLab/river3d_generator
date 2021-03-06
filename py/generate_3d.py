# polygon是含有经纬度数组的列表，h是深度
import numpy as np

# polygon是含有经纬度数组的列表，h是深度
def river_p_obj(polygon, h):
    s = ""
    upper_points = [[p2d[1], 0, p2d[0]] for p2d in polygon]
    lower_points = [[p2d[1], -h, p2d[0]] for p2d in polygon]

    for i in range(len(polygon)):
        s += "\nv "
        for num in upper_points[i]:
            s += str(num)
            s += " "
        s += "\nv "
        for num in lower_points[i]:
            s += str(num)
            s += " "

    temp = np.array([1, 3, 4, 2])

    for i in range(len(polygon) - 1):
        s += "\nf "
        for p in temp:
            s += str(p) + " "
        temp += 2

    s += "\nf "
    temp -= 2
    temp[0] = temp[1]
    temp[3] = temp[2]
    temp[1] = 1
    temp[2] = 2
    for p in temp:
        s += str(p) + " "

    # 这个部分不适用与凹多边形，因为它不是用点的顺序控制绘制的顺序，而是直接取外轮廓
    # s+="\nf "
    # for i in range(len(polygon)):
    #     i+=1
    #     s+=str(i*2)+" "

    return s


def river_su(river_array, w, h, ratio_w=0.7, ratio_h=0.3):
    verticesOfRiver = []
    river_point_length = len(river_array)
    print(river_array)
    for i in range(river_point_length - 1):
        Xn = river_array[i][0]
        Xn1 = river_array[i + 1][0]
        Yn = river_array[i][1]
        Yn1 = river_array[i + 1][1]
        # 法向量未归一
        norm = np.sqrt((Xn - Xn1) ** 2 + (Yn - Yn1) ** 2)
        verticesOfRiver += [
            Xn + w * Yn1 / norm - w * Yn / norm,
            Yn + w * Xn / norm - w * Xn1 / norm,
            0,
            Xn + w * Yn / norm - w * Yn1 / norm,
            Yn + w * Xn1 / norm - w * Xn / norm,
            0,
        ]
        verticesOfRiver += [
            Xn + w * ratio_w * Yn1 / norm - w * ratio_w * Yn / norm,
            Yn + w * ratio_w * Xn / norm - w * ratio_w * Xn1 / norm,
            -h,
            Xn + w * ratio_w * Yn / norm - w * ratio_w * Yn1 / norm,
            Yn + w * ratio_w * Xn1 / norm - w * ratio_w * Xn / norm,
            -h,
        ]
        verticesOfRiver += [Xn, Yn, -h - h * ratio_h]
    Xn = river_array[river_point_length - 2][0]
    Xn1 = river_array[river_point_length - 1][0]
    Yn = river_array[river_point_length - 2][1]
    Yn1 = river_array[river_point_length - 1][1]
    Xend = river_array[river_point_length - 1][0]
    Yend = river_array[river_point_length - 1][1]
    norm = np.sqrt((Xn - Xn1) ** 2 + (Yn - Yn1) ** 2)
    verticesOfRiver += [
        Xend + w * Yn1 / norm - w * Yn / norm,
        Yend + w * Xn / norm - w * Xn1 / norm,
        0,
        Xend + w * Yn / norm - w * Yn1 / norm,
        Yend + w * Xn1 / norm - w * Xn / norm,
        0,
    ]
    verticesOfRiver += [
        Xend + w * ratio_w * Yn1 / norm - w * ratio_w * Yn / norm,
        Yend + w * ratio_w * Xn / norm - w * ratio_w * Xn1 / norm,
        -h,
        Xend + w * ratio_w * Yn / norm - w * ratio_w * Yn1 / norm,
        Yend + w * ratio_w * Xn1 / norm - w * ratio_w * Xn / norm,
        -h,
    ]
    verticesOfRiver += [Xend, Yend, -h - h * ratio_h]
    indicesOfRiverFaces = []
    # // 方向应该是朝内还是朝外的区别，比如顺时针朝上，逆时针朝下，左手法则
    for k in range(river_point_length - 1):
        indicesOfRiverFaces += [
            k * 5 + 1,
            k * 5,
            k * 5 + 5,
            k * 5 + 5,
            k * 5 + 6,
            k * 5 + 1,
        ]
        indicesOfRiverFaces += [
            k * 5 + 5,
            k * 5,
            k * 5 + 2,
            k * 5 + 2,
            k * 5 + 7,
            k * 5 + 5,
            k * 5 + 3,
            k * 5 + 1,
            k * 5 + 6,
            k * 5 + 6,
            k * 5 + 8,
            k * 5 + 3,
        ]
        indicesOfRiverFaces += [
            k * 5 + 7,
            k * 5 + 2,
            k * 5 + 4,
            k * 5 + 4,
            k * 5 + 9,
            k * 5 + 7,
            k * 5 + 4,
            k * 5 + 3,
            k * 5 + 8,
            k * 5 + 8,
            k * 5 + 9,
            k * 5 + 4,
        ]
    s = "mtllib demo.mtl\n"
    print(verticesOfRiver, indicesOfRiverFaces)
    for i in range(len(verticesOfRiver) // 3):
        s += "v %s %s %s\n" % (
            verticesOfRiver[i * 3],
            verticesOfRiver[i * 3 + 1],
            verticesOfRiver[i * 3 + 2],
        )
    s += "vt 0.0 0.0\nvt 1.0 0.0\nvt 0.0 1.0\nvt 1.0 1.0\nusemtl demo\n"
    for i in range(len(indicesOfRiverFaces) // 6):
        s += "f %s/1 %s/2 %s/3 %s/4\n" % (
            indicesOfRiverFaces[i * 6] + 1,
            indicesOfRiverFaces[i * 6 + 1] + 1,
            indicesOfRiverFaces[i * 6 + 2] + 1,
            indicesOfRiverFaces[i * 6 + 4] + 1,
        )
    print(s)

    return s


if __name__ == "__main__":
    p = [
        (116.26338923687605, 40.00363483739438),
        (116.26434637248975, 40.00373349981755),
        (116.26434637248975, 40.00326748860883),
        (116.26434637248975, 40.00281940090814),
        (116.26436429599778, 40.00228169566731),
        (116.26445391353792, 40.001779837442534),
    ]
    river_array = [
        [23922.0533443857, -57096.95589741133],
        [23922.0533443857, -57153.4504867848],
        [23922.0533443857, -57225.6375495391],
        [23925.29666624032, -57322.93232489377],
        [23935.026631804183, -57395.11815461703],
        [23938.26995365694, -57454.74953089841],
        [23938.26995365694, -57504.96514875349],
        [23947.999919220805, -57533.21132212225],
        [23977.189815910533, -57589.703427629545],
        [23996.64974703826, -57643.05678750947],
        [23996.64974703826, -57646.1952115139],
        [23999.89306889288, -57708.96348306537],
        [24012.866356309503, -57809.39189168997],
        [24089.185774022713, -58034.84155782405],
        [24171.535743314773, -58224.85403264873],
        [24234.881873538718, -58420.99212595634],
        [24336.235681900755, -58684.54658454377],
        [24412.251038173214, -58892.93352704495],
        [24500.935620484874, -59015.51203752402],
        [24576.950976757333, -59138.08903405536],
        [24652.966333026066, -59236.149541283026],
        [24716.312463251874, -59328.08038689196],
        [24772.31936637126, -59412.820631711744],
        [24817.155045621097, -59486.72334636282],
        [24866.972467008978, -59586.33048241865],
        [24923.026446292177, -59694.099546447396],
        [24972.324937032536, -59761.875273287296],
        [25026.812742585316, -59859.772728364915],
        [25086.489862954244, -59947.62859673798],
        [25130.59903888218, -60017.9127315497],
        [25192.87081665732, -60103.257083338685],
        [25231.79067776911, -60166.00981505029],
        [25275.89985369146, -60246.33273275476],
        [25317.41437220946, -60319.12481551152],
        [25369.307520357892, -60429.56695621088],
        [25418.606011096388, -60522.43780527171],
        [25431.579298134893, -60572.6379024582],
        [25454.931214798242, -60622.83774578851],
        [25488.879646904767, -60725.00116574485],
        [25540.742903523147, -60841.79032016825],
        [25573.901379065588, -60913.34355995059],
        [25607.910071929917, -60965.157653014176],
        [25679.13653502427, -61057.86353220511],
        [25762.165568141267, -61165.78760119807],
        [25850.383915832266, -61273.71049695555],
        [25930.81829166785, -61376.612630533054],
        [25985.30609465204, -61454.41597466823],
        [26032.009925780818, -61514.65040299762],
        [26057.956498630345, -61547.27723242249],
        [26107.25498704426, -61605.001360290684],
        [26125.417588042095, -61640.13762162626],
        [26143.580189036205, -61680.29319661111],
        [26177.310733739287, -61738.016551118344],
        [26208.446621160954, -61800.75894711632],
        [26236.938113924116, -61902.014220007695],
        [26249.9114013426, -61999.26316591725],
        [26275.857976177707, -62077.689041383564],
        [26324.507803995162, -62221.99103373848],
        [26373.157631810755, -62328.64768020902],
        [26415.06134943664, -62414.62523324229],
        [26442.045786814764, -62460.800531271845],
        [26462.803046334535, -62496.937571252696],
        [26502.24183942564, -62551.142884634435],
        [26537.529180612415, -62589.28718703985],
        [26572.816521801054, -62627.431342918426],
        [26612.255314890295, -62683.64351608697],
        [26653.769833933562, -62761.93851270992],
        [26697.360078930855, -62840.23289200477],
        [26731.8640662916, -62919.37471105717],
        [26751.323998333886, -62972.69943478145],
        [26770.783930376172, -63035.43403726444],
        [26790.243862422183, -63123.26181492396],
        [26799.97382844612, -63211.08881581202],
        [26809.703794468194, -63283.23184261285],
        [26822.677082497627, -63345.96448338404],
        [26855.110302569345, -63436.92610861361],
        [26877.813556622714, -63502.794351610355],
        [26913.490098703653, -63574.935259336606],
        [26952.40996279195, -63615.71032320149],
        [26991.329826880246, -63653.34869510215],
        [27023.76304695569, -63690.98692435864],
        [27082.142843089998, -63728.62501096632],
        [27117.8193851728, -63769.39944382943],
        [27159.98257126659, -63828.99254457373],
        [27228.548432029784, -63956.707592557184],
        [27277.84692509286, -64047.03634133749],
        [27324.550760628656, -64144.89155877475],
        [27381.633226282895, -64240.23674071953],
        [27420.553089231253, -64345.617192734964],
        [27454.28363711387, -64413.36117861513],
        [27488.01418500021, -64456.014562306926],
        [27537.31267806515, -64508.70378338825],
        [27560.66459583305, -64538.8117842339],
        [27604.773773837835, -64571.42868215591],
        [27667.04555455409, -64606.554452442564],
        [27726.722677737474, -64626.62626540661],
        [27824.377101808786, -64643.99573485181],
        [27898.973504461348, -64669.08539969288],
        [28002.759803801775, -64728.67309969384],
        [28096.8161375802, -64813.34974266682],
        [28174.65586208552, -64894.88953143172],
        [28265.468874009326, -64985.836967696436],
        [28369.25517335348, -65086.19179306179],
        [28456.8248634208, -65180.27352104802],
        [28534.664587929845, -65246.130200448446],
        [28617.762070616707, -65317.703231369145],
        [28699.697463123128, -65373.738089676015],
        [28795.346909383312, -65436.67829206772],
        [28948.12033048831, -65549.71275639348],
        [29047.75517034158, -65615.22077770531],
        [29115.506861440837, -65647.33239507861],
        [29159.34619097598, -65664.03039509337],
        [29195.214733323082, -65669.16823560372],
        [29269.60874707997, -65676.87499138899],
        [29346.127122551203, -65679.5842907941],
        [29429.156160637736, -65681.5912570348],
        [29545.396813958883, -65687.6121533243],
        [29630.501577999443, -65693.63304596767],
        [29678.243274897337, -65709.68874184228],
        [29678.243274897337, -65707.68178127706],
        [29709.37916418165, -65715.70962110441],
        [29767.499490842223, -65745.81396267936],
        [29798.635380124673, -65775.91821302474],
        [29842.225625121966, -65826.09176088031],
        [29892.04304797016, -65876.26505533047],
        [29925.254663206637, -65914.39658964425],
        [29970.92063415423, -65954.53488869406],
        [29995.829345582053, -65982.63160153665],
        [30006.207975339144, -65990.65921918396],
    ]
    river_array2 = [[0, 0], [3, 3], [10, 15]]
    f = open(r"../model/river.obj", mode="w")
    # f.write(river_p_obj(p,5 /111000,5/111000))
    f.write(river_su(river_array, 5, 5))
    # f.write(river_su(river_array2, 1, 1))
    f.close()