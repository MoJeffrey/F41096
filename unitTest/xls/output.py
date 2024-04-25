import xlwt

# 创建一个新的工作簿和工作表
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('结果')

# 创建样式对象，设置文本对齐方式为居中和自动换行
style = xlwt.XFStyle()
style.alignment.wrap = 1  # 自动换行

# 写入数据
sheet.write(0, 0, "这是第一行\n这是第二行", style=style)
sheet.col(0).width = 256 * (len(str("这是第一行\n这是第二行")) + 4)
sheet.write(0, 1, 'Age')
sheet.write(0, 2, 'Gender')

sheet.write(1, 0, 'Alice')
sheet.write(1, 1, 25)
sheet.write(1, 2, 'Female')

sheet.write(2, 0, 'Bob')
sheet.write(2, 1, 30)
sheet.write(2, 2, 'Male')

sheet.write(3, 0, 'Carol')
sheet.write(3, 1, 35)
sheet.write(3, 2, 'Female')

# 保存工作簿到文件
workbook.save('output.xls')

sheet.write(4, 0, 'Jeffrey')
workbook.save('output.xls')