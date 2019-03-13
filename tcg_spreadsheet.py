import csv
from bs4 import BeautifulSoup as BS
from requests import get
import datetime

def open_file():
	while True:
		try:
			return open(input("Filename: "))
		except FileNotFoundError:
			print("Not found")

def parse_set_name(set_name):
	#checks for core set abriviations
	if set_name[0].lower() == "m" and set_name[1:].isdigit():
		return "core-set-20"+set_name[1:]
	#checks for modern masters 2013 abriviations
	elif set_name[0:2].lower() == "mm" and \
		(set_name[2:] == "1" or set_name[2:] == "13"):
		return "modern-masters"
	#checks for modern masters 2015 abriviations
	elif set_name[0:2].lower() == "mm" and \
		(set_name[2:] == "2" or set_name[2:] == "15"):
		return "modern-masters-2015"
	#checks for modern masters 2017 abriviations
	elif set_name[0:2].lower() == "mm" and \
		(set_name[2:] == "3" or set_name[2:] == "17"):
		return "modern-masters-2017"
	else:
		return set_name.replace(" ", "-")

def parse_name(name):
	return name.replace(" ", "-")

def main():
	fp = open_file()
	csvfp = csv.reader(fp)
	#set_name = parse_set_name("m19")
	#name = "Crucible of Worlds"
	#foil = 'F'
	#url = "http://shop.tcgplayer.com/magic/"+set_name+"/"+name.replace(" ", "-").lower()
	file_name = fp.name.split(".")[0]+" updated "+\
				str(datetime.datetime.now().day)+"-"+\
				str(datetime.datetime.now().month)+"-"+\
				str(datetime.datetime.now().year)+".csv"
	new_fp = open(file_name, "w")

	new_csvfp = csv.writer(new_fp)

	header = [x.lower().strip() for x in next(csvfp)]
	new_csvfp.writerow(header)
	for line in csvfp:
		if line[header.index("name")] == "" or line[header.index("set")] == "":
			continue
		set_name = parse_set_name(line[header.index("set")])
		name = parse_name(line[header.index("name")])
		url = "http://shop.tcgplayer.com/magic/"+set_name+"/"+name.replace(" ", "-").lower()
		print(url)
		if "foil" in header:
			#foil handling
			pass
		else:
			raw_html = get(url).content
			html = BS(raw_html, 'html.parser')
			price = html.findAll("td", {"class":"price-point__data"})[0].text.strip("$")
			line[header.index("price")] = price
		new_csvfp.writerow(line)
	new_fp.close()

	# raw_html = get(url).content
	# html = BS(raw_html, 'html.parser')
	# if foil.lower() == "f":
	# 	price = html.findAll("td", {"class":"price-point__data"})[1].text.strip("$")
	# else:
	# 	price = html.findAll("td", {"class":"price-point__data"})[0].text.strip("$")

	# print(price)







if __name__ == "__main__":
	main()