需安装的第三方库：
pip install PyQT5
pip install ephem
pip install re

程序中世纪列表提供前13世纪至30世纪，因为ephem库在计算BC13世纪至BC30世纪间的平均误差达2小时，导致确定农历月份容易出错。
在早于BC30世纪前，误差更大。虽然在30世纪以后的较长时间内，ephem库的误差还很小，但也并非一般所需的功能。
同时，对于特殊需求，程序中的年列表控件也开放了输入任意年份的功能。
如有需要，可自行在Data.py文件中修改startCentury和endCentury变量，无需再到相关函数中修改。

节日公历只录入了法定节假日，农历录入了常用农历。如需添加，可自行在Data.py文件中按格式添加节日。
其中公历节日存储在scfestivals列表中，农历节日存储在lcfestivals列表中。
格式为[月，日，节日]，其中公历月日为数字，农历月日为字符串，节日皆为字符串。
由于清明节日期不定，已单独处理，勿在列表中添加。
程序中已处理设置节日，无需另行处理。

程序加了搜索农历节日，如果无需可自行删除相关代码。包括：
QtUI文件中self.cblFindFestival相关
PerpetualCalendar文件中jumpLCF函数及ui.cblFindFestival相关

