import math, ephem
from Data import *


def JD2date(JD, ut=0):
	return ephem.Date(JD + ut/24 - 2415020)


def EquinoxSolsticeJD(year, angle):
	if 0 <= angle < 90:
		date = ephem.next_vernal_equinox(year)
	elif 90 <= angle < 180:
		date = ephem.next_summer_solstice(year)
	elif 180 <= angle < 270:
		date = ephem.next_autumn_equinox(year)
	else:
		date = ephem.next_winter_solstice(year)
	JD = ephem.julian_date(date)
	return JD


# 计算二十四节气
def SolarLongitube(JD):
	date = JD2date(JD)
	s = ephem.Sun(date)  # date应为UT时间
	sa = ephem.Equatorial(s.ra, s.dec, epoch=date)
	se = ephem.Ecliptic(sa)
	L = se.lon / ephem.degree / 180 * math.pi
	return L

def SolarTerms(year, angle, year0=''):  # year0：欲求值
	JD = EquinoxSolsticeJD(str(year), angle)  # 初值
	year1 = JD2date(JD, 8).triple()[0]
	if year0 != '' and year1 != year0:  # 非该年值，从另一个节气迭代
		JD = EquinoxSolsticeJD(str(year0), (angle + 90) % 360)
	JD1 = JD
	while True:
		JD2 = JD1
		L = SolarLongitube(JD2)
		JD1 += math.sin(angle * math.pi / 180 - L) / math.pi * 180
		if abs(JD1 - JD2) < 0.00001:
			break  # 精度小于1 second
	return JD1  # UT


def DateDiffer(JD1, JD2):
	return math.floor(JD1 + 8 / 24 + 0.5) - math.floor(JD2 + 8 / 24 + 0.5)


def DateCompare(JD1, JD2): # 输入ut，返回ut+8的比较结果
	if DateDiffer(JD1, JD2) >= 0: return True  # JD1 >= JD 2
	else: return False


def findSZY(JD, shuoJD):  # 查找JD所在的农历月份
	szy = -1
	for i in range(len(shuoJD)):
		if DateCompare(JD, shuoJD[i]):
			szy += 1  # date所在的阴历月序，起冬至朔
	return szy


def findDZS(year): # 寻找年前冬至月朔日
	if year == 1: year -= 1  # 公元元年前冬至在公元前1年
	dz = ephem.next_solstice((year - 1, 12)) # 年前冬至
	jd = ephem.julian_date(dz)
	# 可能的三种朔日
	date1 = ephem.next_new_moon(JD2date(jd - 0))
	jd1 = ephem.julian_date(date1)
	date2 = ephem.next_new_moon(JD2date(jd - 29))
	jd2 = ephem.julian_date(date2)
	date3 = ephem.next_new_moon(JD2date(jd - 31))
	jd3 = ephem.julian_date(date3)
	if DateCompare(jd, jd1): # 冬至合朔在同一日或下月
		return date1
	elif DateCompare(jd, jd2) and (not DateCompare(jd, jd1)):
		return date2
	elif DateCompare(jd, jd3): # 冬至在上月
		return date3


def LunarCalendar(nian, type=1):   # type=1时截止到次年冬至朔，=0时截止到次年冬至朔次月
	dzs = findDZS(nian)
	shuo = dzs  # 计算用朔，date格式
	shuoJD = [ephem.julian_date(dzs)]  # 存储ut+8 JD，起冬至朔
	next_dzsJD = ephem.julian_date(findDZS(nian + 1))  # 次年冬至朔
	i = -1  # 中气序，从0起计
	j = -1  # 计算连续两个冬至月中的合朔次数，从0起计
	zry = 0
	flag = False
	# 查找所在月及判断置闰
	while not DateCompare(shuoJD[j+type], next_dzsJD):  # 从冬至月起查找，截止到次年冬至朔
		i += 1
		j += 1
		shuo = ephem.next_new_moon(shuo)  # 次月朔
		shuoJD.append(ephem.julian_date(shuo))
		# 查找本月中气，若无则置闰
		if j == 0: continue  # 冬至月一定含中气，从次月开始查找
		angle = (-90 + 30 * i) % 360  # 本月应含中气，起冬至
		qJD = SolarTerms(nian, angle)
		# 不判断气在上月而后气在后月的情况，该月起的合朔次数不超过气数，可省去
		if DateCompare(qJD, shuoJD[j+1]) and flag == False:  # 中气在次月，则本月无中气
				zry = j + 1  # 置闰月
				i -= 1
				flag = True  # 仅第一个无中气月置闰
	# 生成农历月序表
	ymb = []
	for k in range(len(shuoJD)):
		ymb.append(yuefen[(k - 2) % 12])  # 默认月序
		if j + type == 13:  # 仅12次合朔不闰，有闰时修改月名
			if k + 1 == zry:
				ymb[k] = '闰' + yuefen[(k-1 - 2) % 12]
			elif k + 1 > zry:
				ymb[k] = yuefen[(k-1 - 2) % 12]
	return ymb, shuoJD   # 月名表，合朔JD日期表
