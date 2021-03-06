tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
gz = [''] * 60  # 六十甲子表
for i in range(60):
	gz[i] = tiangan[i % 10] + dizhi[i % 12]
zodiac = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪', ]
jieqi = ["冬至","小寒","大寒","立春","雨水","惊蛰","春分","清明","谷雨","立夏","小满","芒种","夏至","小暑","大暑","立秋","处暑","白露","秋分","寒露","霜降","立冬","小雪","大雪"]
yuefen =["正月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
nlrq = ["初一","初二","初三","初四","初五","初六","初七","初八","初九","初十","十一","十二","十三","十四","十五","十六","十七","十八","十九","二十","廿一","廿二","廿三","廿四","廿五","廿六","廿七","廿八","廿九","三十"]
# 添加节日：节日表[[月，日, 节日] * n]，sc公历节日，lc农历节日
scfestivals = [[1, 1, "元旦"], [5, 1, "劳动节"], [10, 1, "国庆"]]
lcfestivals = [['十二月', '三十', '除夕'], ['正月', '初一', "春节"], ['正月', '十五', "元宵"], ['五月', '初五', "端午"],
               ["七月", "初七", "七夕"], ['七月', '十五', "中元"], ['八月', '十五', "中秋"], ['九月', '初九', '重阳'],
               ['十二月', '初八', '腊八']]
weeks = ['一', '二', '三', '四', '五', '六', '日']
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
dateInfo = [[]] * 42
selected = None
setYear = ''
startCentury = -13
endCentury = 30
start_century = startCentury if startCentury <= 0 else startCentury - 1

def gyjn(year): # 给定年份年转公元纪年
	if year == 0:
		return "无公元0年"
	if year < 0:
		return "公元前" + str(-year) + "年"
	elif year == 1:
		return "公元元年"
	elif year > 0:
		return "公元" + str(year) + "年"


def font(text, size=12, color="gray", bold="normal"):
	text = "<font style='font-size:" + str(size) + "px; text-align:center; color:" + color + ";font-weight:" + str(bold) + ";'>" + str(text) + "</font><br/>"
	return text