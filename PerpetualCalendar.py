from DateCalc import *
import re
import time


def borderDate(ui, month, day):  # 选中后加框
	firstDate = int(re.findall(r'(\d+)</font>', ui.labs[0][0].text())[0])
	if firstDate == 1:
		idx = - firstDate + day
	else:
		idx = days[month - 1] - firstDate + day
	global selected
	selected = ui.labs[idx // 7][idx % 7]
	selected.setStyleSheet("QLabel{border:3px solid; border-radius: 5px; border-color:#1E90FF}")


def yearItems(ui):
	century = ui.cblCentury.currentIndex() + start_century + 1
	ui.cblYear.clear()
	for i in range(100):
		if century == 1 and i == 0: continue
		if century <= 0:
			ui.cblYear.addItem('BC' + str(abs(century) * 100 + 100 - i) + '年')
		else:
			ui.cblYear.addItem(str((century-1) * 100 + i) + '年')
	ui.cblYear.setCurrentIndex(0)


def lastYear(ui):
	idx = ui.cblYear.currentIndex()
	if idx == 0:
		century = ui.cblCentury.currentIndex()
		ui.cblCentury.setCurrentIndex(century - 1)
		ui.cblYear.setCurrentIndex(ui.cblYear.count()-1)
	elif idx == -1:
		getYearMonth(ui, wheel=-1)
	else:
		ui.cblYear.setCurrentIndex(idx - 1)


def nextYear(ui):
	idx = ui.cblYear.currentIndex()
	century = ui.cblCentury.currentIndex()
	if idx == -1 or century == endCentury - start_century - 1:
		getYearMonth(ui, wheel=1)
	elif ui.cblYear.count() > 0 and idx == ui.cblYear.count() - 1:
		ui.cblCentury.setCurrentIndex(century + 1)
	else:
		ui.cblYear.setCurrentIndex(idx + 1)


def jumpYear(ui):  # 本世纪首年或末年时跳转上世纪或下世纪
	idx = ui.cblYear.currentIndex()
	century = ui.cblCentury.currentIndex()
	if idx == 0:
		if century == 0: pass
		else:
			ui.cblCentury.setCurrentIndex(century - 1)
			ui.cblYear.setCurrentIndex(ui.cblYear.count()-1)
	elif idx != -1 and idx == ui.cblYear.count() - 1:
		if century == endCentury - start_century - 1: pass
		else: ui.cblCentury.setCurrentIndex(century + 1)
	displayDate(ui)


def lastMonth(ui):
	idx = ui.cblMonth.currentIndex()
	if idx == 0:
		lastYear(ui)
		ui.cblMonth.setCurrentIndex(11)
	else:
		ui.cblMonth.setCurrentIndex(idx - 1)


def nextMonth(ui):
	idx = ui.cblMonth.currentIndex()
	if idx == 11:
		nextYear(ui)
		ui.cblMonth.setCurrentIndex(0)
	else:
		ui.cblMonth.setCurrentIndex(idx + 1)


def jumpMonth(ui):
	idx = ui.cblMonth.currentIndex()
	if idx == 0:
		lastYear(ui)
		ui.cblMonth.setCurrentIndex(11)
	elif idx == 11:
		nextYear(ui)
		ui.cblMonth.setCurrentIndex(0)
	displayDate(ui)


def getSolorTerms(year):
	jqb = [[i] for i in range(12)]  # [月序，[日序， 节气序] * n]
	for i in range(24):
		jq = JD2date(SolarTerms(year, i * 15, year), 8)
		jqn, jqy, jqr = jq.triple()
		if jqn != year:
			jq = JD2date(SolarTerms(year + (year - jqn), i * 15, year), 8)
			jqn, jqy, jqr = jq.triple()
		if jqn == year:  # 部分年无某节气，如BC1243年无冬至
			jqb[jqy-1].append([int(jqr), (i + 6) % 24])  # 按月存储
	for j in range(len(jqb)): jqb[j].pop(0)
	return jqb  # [[日序， 节气序] * n]


def setNYE(festival, ymb, shuoJD):  # 重设节日日期
	yx = ymb.index(festival[0])
	if DateDiffer(shuoJD[yx + 1], shuoJD[yx]) == 29:
		festival[1] = '廿九'
	else:
		festival[1] = '三十'
	return festival


def jumpLCF(currentFes, ymb, shuoJD):  # 节日农历月转公历月
	for festival in lcfestivals:
		if currentFes == festival[2]:
			if festival[2] == '除夕': festival = setNYE(festival, ymb, shuoJD)
			month2 = ymb.index(festival[0])
			shuo = shuoJD[month2]
			month, day = JD2date(shuo, 8).triple()[1:]
			if int(day) + nlrq.index(festival[1]) <= days[month-1]: month -= 1
			if month > 11: month -= 12
			return month


def getYearMonth(ui, wheel=0): # 根据输入重设年月
	edit = ui.cblYear.currentText()
	try:
		year = int(re.search(r'-?\d+', edit).group())
	except:
		return 0, 0  # 异常输入
	if year == 0: return 0, 0
	if 'BC' in ui.cblYear.currentText() or 'bc' in edit:
		year = -year
	year += wheel
	century = year // 100
	if start_century * 100 <= year < endCentury * 100:
		ui.cblCentury.setCurrentIndex(century - start_century)
		if century == 0: ui.cblYear.setCurrentIndex(year % 100 - 1)
		else: ui.cblYear.setCurrentIndex(year % 100)
	else:
		ui.cblCentury.setCurrentIndex(-1)
		ui.cblYear.clear()
		if wheel == 0: ui.cblYear.setCurrentText(edit)
		else: ui.cblYear.setCurrentText(str(year))
	if ui.sender() == ui.cblFindFestival: month = -1
	else: month = ui.cblMonth.currentIndex()
	global setYear
	if year != setYear or setYear == '':
		setYear = year
		updateYear()
	return year, month


def updateYear():
	global yearYMB, yearSJD, yearST
	yearYMB, yearSJD = LunarCalendar(setYear, 0)
	yearST = getSolorTerms(setYear)


def displayMonth(ui):
	year, month = getYearMonth(ui)
	if year == 0: return 0, 0, 0
	ymb, shuoJD, jqb = yearYMB, yearSJD, yearST
	if DateCompare(ephem.julian_date((year, 12, 31)), shuoJD[-2] + 29):
		ymb1, shuoJD1 = LunarCalendar(year + 1)
		ymb = ymb[:-2] + ymb1[:2]
		shuoJD = shuoJD[:-2] + shuoJD1[:3]
	currentFes, fesDay = '', 0
	if ui.sender() == ui.cblFindFestival:
		currentFes = ui.cblFindFestival.currentText()
		month = jumpLCF(currentFes, ymb, shuoJD)
		ui.cblMonth.setCurrentIndex(month)
	days[1] = 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28
	if year < 1582 and year % 4 == 0: days[1] = 29
	i = month
	ysJD = ephem.julian_date((year, i + 1))
	szy = findSZY(ysJD, shuoJD)  # 每月1日对应的农历月
	ysRQ = DateDiffer(ysJD, shuoJD[szy])  # 每月1日的农历日期
	yue0 = DateDiffer(shuoJD[szy + 1], shuoJD[szy])
	yue1 = DateDiffer(shuoJD[szy + 2], shuoJD[szy + 1])
	blank = int((ysJD + 0.5) % 7)
	for j in range(6):
		for k in range(7):
			# 计算日期
			day = j * 7 + k - blank + 1
			rqx = ysRQ + (j+1) * 7 - 7 + k - blank
			if rqx < 0:  # 月首日所在农历月上月
				yue = DateDiffer(shuoJD[szy], shuoJD[szy - 1])
				rq = nlrq[rqx % yue]
				yx = szy - 1
			elif 0 <= rqx < yue0:
				rq = nlrq[rqx]
				yx = szy
			elif yue0 <= rqx < yue0 + yue1:
				rq = nlrq[rqx - yue0]
				yx = szy + 1
			elif rqx >= yue0 + yue1:
				rq = nlrq[rqx - yue0 - yue1]
				yx = szy + 2
			if day == 1:
				yx1 = yx
				rq1 = rq
			if day == days[i]:
				yx2 = yx
				rq2 = rq
			dateInfo[j * 7 + k] = [day, ymb[yx], rq, ysJD+day-1, jqb[i]]
			if year == 1582 and i == 9: dateInfo[j * 7 + k][-1] = [jqb[i][0], jqb[i-1][1]]  # 该月无节气，月干支序从上月获取
			if rq == '初一': rq = ymb[yx]
			# 显示月历
			if j == 0 and k < blank:  # 上月
				ui.labs[j][k].setText(font(days[i-1]-blank+k+1, 20) + font(rq))
			else:  # 本月
				if day <= days[i]:
					if year == 1582 and i == 9 and day > 4:
						if day < 15: continue
						else: ui.labs[j+(k-10)//7][k-3].setText(font(day, 20, "black", 800) + font(rq))
					else:
						ui.labs[j][k].setText(font(day, 20, "black", 800) + font(rq))  # "500;font-family:微软雅黑"
				else:  # 次月
					if year == 1582 and i == 9:
						ui.labs[j+(k-10)//7][k-3].setText(font(day - days[i], 20) + font(rq))
						if day - days[i] == 11:
							for m in range(10): ui.labs[j-1+(m+k-2)//7][(m+k-2)%7].setText("")
					else: ui.labs[j][k].setText(font(day-days[i], 20) + font(rq))
	# 显示节日
	qmDay = 0
	for jq in jqb[i]:  # 节气
		jqrx = jq[0] + blank - 1
		if year == 1582 and i == 9: jqrx -= 10
		ui.labs[jqrx//7][jqrx%7].setText(font(jq[0], 20, "black", 800) + font(jieqi[jq[1]], 12, "red"))
		if jq[1] == 7: qmDay = jq[0]
	if year >= 1949:  # 公历节日起始年
		if qmDay: ui.labs[(qmDay+blank-1)//7][(qmDay+blank-1)%7].setText(font(qmDay, 20, "red", 800) + font("清明", 12, "red"))
		for fes in scfestivals:
			if fes[0] == month + 1:
				jqrx = fes[1] + blank - 1
				ui.labs[jqrx // 7][jqrx % 7].setText(font(fes[1], 20, "red", 800) + font(fes[2], 12, "red"))
	if year > 1911:  # 农历节日起始年
		rqx1 = nlrq.index(rq1)
		for fes in lcfestivals:
			if fes[2] == '除夕': fes = setNYE(fes, ymb, shuoJD)
			jqrx = nlrq.index(fes[1])
			if fes[0] == ymb[yx1] and jqrx >= rqx1:  # 该月农历首日
				jqrx += -rqx1 + blank
				ui.labs[jqrx // 7][jqrx % 7].setText(font(jqrx-blank+1, 20, "red", 800) + font(fes[2], 12, "red"))
			elif fes[0] == ymb[yx1+1] and jqrx <= nlrq.index(rq2):  # 该月农历末日
				jqrx += DateDiffer(shuoJD[yx1 + 1], shuoJD[yx1]) - rqx1 + blank
				ui.labs[jqrx // 7][jqrx % 7].setText(font(jqrx - blank + 1, 20, "red", 800) + font(fes[2], 12, "red"))
			elif yx2 - yx1 == 2 and fes[0] == ymb[yx2]:  # 跨2月
				jqrx += DateDiffer(shuoJD[yx1 + 2], shuoJD[yx1]) - rqx1 + blank
				if 0 < jqrx <= days[i] + blank: ui.labs[jqrx // 7][jqrx % 7].setText(font(jqrx - blank + 1, 20, "red", 800) + font(fes[2], 12, "red"))
			if fes[2] == currentFes: fesDay = jqrx - blank + 1
	return year, month, fesDay


def displayDate(ui):
	global selected
	try:
		selected.setStyleSheet("")
	except:
		pass
	if ui.sender() in [None, ui.btnToday]:  # 设为今日
		year, month, day = time.localtime(time.time())[0:3]
		month -= 1
		ui.cblCentury.setCurrentIndex(-start_century + year // 100)
		ui.cblYear.setCurrentIndex(year % 100)
		ui.cblMonth.setCurrentIndex(month % 12)
		displayMonth(ui)
		borderDate(ui, month, day)
	else:
		if ui.sender() in [ui.cblCentury, ui.cblYear, ui.cblMonth, ui.btnLastMonth, ui.btnNextMonth, ui.btnLastYear, ui.btnNextYear, ui.cblFindFestival]:  # 设为原公历日
			year, month, day = displayMonth(ui)
			if year == 0: return 0
			if ui.sender() != ui.cblFindFestival: day = int(re.findall(r'(\d+)</font>', ui.labInfo.text())[0])  # 公历日期
			if day > days[month]: day = days[month]  # 跳到上月底
			borderDate(ui, month, day)
		else:  # 点击日期跳转
			year, month = getYearMonth(ui)
			if year == 0: return 0
			selected = ui.sender()
			if selected.text() == "": return 0  # 1582年被删除的日期
			day = int(re.findall(r'(\d+)</font>', selected.text())[0])  # 公历日期
			if not re.search(r"<font style='font-size:20px; text-align:center; color:gray", selected.text()):  # 本月内
				ui.sender().setStyleSheet("QLabel{border:3px solid; border-radius: 5px; border-color:#1E90FF}")  # 1E90FF 9400D3
			else:   # 跳转前后月
				if day > 20: lastMonth(ui)
				else: nextMonth(ui)
				year, month = displayMonth(ui)[:2]  # 更新月历
				borderDate(ui, month, day)
	# 日期相关显示信息
	jdn = math.floor(ephem.julian_date((year, month + 1, day)) + 8/24 + 0.5)
	jdn0 = math.floor(ephem.julian_date(time.localtime(time.time())[0:3]) + 8 / 24 + 0.5)
	difference = jdn - jdn0
	if difference > 0: difference = '距今：' + str(abs(difference)) + '天后'
	elif difference == 0: difference = '今天'
	else: difference = '距今：' + str(abs(difference)) + '天前'
	week = weeks[math.floor(jdn % 7)]
	ym, rq, JD, jqrq = dateInfo[day-dateInfo[0][0]][1:]
	nian = year
	# count1 = count2 = len(jqrq)
	# for i in range(count1):
	# 	if jqrq[i][1] < 3: count1 -= 1
	# 	if jqrq[i][1] == 3 and day < jqrq[i][0]: count2 -= 1
	# if count1 == 0: nian -= 1  # 该月所有节气在立春前
	# elif count2 != len(jqrq): nian -= 1  # 立春所在月
	if month < 3 and yuefen.index(ym.split('闰')[-1]) >= 10: nian -= 1
	if nian < 0: ngz = gz[(nian - 3) % 60]
	else: ngz = gz[(nian - 4) % 60]
	nm = gyjn(year)
	sxm = zodiac[(nian - 4) % 12]
	if year < 0: year += 1
	jqr = 99
	for i in range(len(jqrq)):
		if jqrq[i][1] % 2 == 1: jqr = jqrq[i][0]
	if day >= jqr: ygz = gz[(year * 12 + 13 + month) % 60]
	else: ygz = gz[(year * 12 + 12 + month) % 60]
	rgz = gz[math.floor(JD + 8/24 + 0.5 + 49) % 60]
	# JDN、距今、年名、月、星期、日、农历月日、年干支、生肖名、月干支、日干支
	ui.labInfo.setText("<br/>JDN {}<br/>{}<br/>{}<br/>{}月 星期{}<br/>{}{}{}年 〖{}〗<br/>{}月 {}日<br/><br/>".format(
		jdn, font(difference, 12, "black"), nm, month+1, week, font(day, 50, "black"), font(ym+rq, 17, "black"), ngz, sxm, ygz, rgz))
