import json
from requests import get
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from datetime import timedelta
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import csv

import smtplib

def compose1(subj,fileToSend):
	msg = MIMEMultipart()
	msg["From"] = 'CryptoExchange'
	msg["To"] = 'peekin68@gmail.com'
	msg["Subject"] = subj
	msg.preamble = "Please see the attached file"
	
	ctype, encoding = mimetypes.guess_type(fileToSend)
	if ctype is None or encoding is not None:
		ctype = "application/octet-stream"

	maintype, subtype = ctype.split("/", 1)

	if maintype == "text":
		fp = open(fileToSend)
		attachment = MIMEText(fp.read(), _subtype=subtype)
		fp.close()
	elif maintype == "image":
		fp = open(fileToSend, "rb")
		attachment = MIMEImage(fp.read(), _subtype=subtype)
		fp.close()
	
	else:
		fp = open(fileToSend, "rb")
		attachment = MIMEBase(maintype, subtype)
		attachment.set_payload(fp.read())
		fp.close()
	encoders.encode_base64(attachment)
	attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
	msg.attach(attachment)
	print('sending compose1')
	return msg
	
def compose2(subj,data):
	msg = MIMEText(data)
	msg['from']="CryptoExchange"
	msg['Subject']=subj
	msg['to']="peekin68@gmail.com"
	print('sending compose2')
	return msg
	
def compose3(subj,file):
	with open(file) as htm:
		htm=htm.read()
		msg = MIMEText(htm,'html')
		msg['from']="CryptoExchange"
		msg['Subject']=subj
		msg['to']="peekin68@gmail.com"
		print('sending compose3')
		return msg

def sendEmail(template,file):
	if(1):
		msg=""
		if(template==1):
			msg=compose1('Market Volume Alert',file)
		elif(template==2):
			msg=compose2('Total Market Cap Changed',file)
		elif(template==3):
			msg=compose3('Lowest Volume Traded Alert',file)
			
		elif(template==4):
			msg=compose3('Highest Volume Traded Alert',file)
			
		elif(template==5):
			msg=compose3('Biggest Losers Alert',file)
			
		elif(template==6):
			msg=compose3('Biggest Gainers Alert',file)
			
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login("abhi68rajpura@gmail.com", "nikeshirt")
		server.sendmail("abhi68rajpura@gmail.com", "peekin68@gmail.com", msg.as_string())
		server.quit()

def parse(jsn):
	with open('./bin/ranks.json') as rr:
		rr=json.load(rr)
		tm=(datetime.now()).strftime('%m/%d/%y')
		for item in jsn['data']:
			item['id']=str(item['id'])
			try:
				tr=rr[item['id']]
			except Exception as e:
				
				rr[item['id']]={}
			rr[item['id']][tm]=item['cmc_rank']
			
		with open('./bin/ranks.json','w') as rw:
			rw.write(json.dumps(rr))
	
def getDates(tim):
	d1=(tim-timedelta(days=1)).strftime('%m/%d/%y')
	d3=(tim-timedelta(days=3)).strftime('%m/%d/%y')
	d7=(tim-timedelta(days=7)).strftime('%m/%d/%y')
	d14=(tim-timedelta(days=14)).strftime('%m/%d/%y')
	d28=(tim-timedelta(days=28)).strftime('%m/%d/%y')
	return (d1,d3,d7,d14,d28)
	
	
		
def diff():
	tm=datetime.now().strftime('%m/%d/%y')
	diff={}
	(d1,d3,d7,d14,d28)=getDates(datetime.now())
	print(d1,d3,d7,d14,d28)
	with open('./bin/ranks.json') as rr:
		rr=json.load(rr)
		keys=list(rr.keys())
		
				
		for key in keys:
			key=str(key)
			print('key',key)
			diff[key]={}
			try:
				df1=rr[key][tm]-rr[key][d1]
				diff[key]['d1']=df1
			except Exception as e:
				print('exception ',e)
				pass
			try:
				df3=rr[key][tm]-rr[key][d3]
				diff[key]['d3']=df1
			except:
				pass
			try:
				df7=rr[key][tm]-rr[key][d7]
				diff[key]['d7']=df1
			except:
				pass
			try:
				df14=rr[key][tm]-rr[key][d14]
				diff[key]['d14']=df1
			except:
				pass
				
			try:
				df28=rr[key][tm]-rr[key][d28]
				diff[key]['d28']=df1
			except:
				pass
				
		with open('./bin/diff.json','w') as dfw:
			dfw.write(json.dumps(diff))
			
			
def remOld():
	tm=datetime.now()
	with open('./bin/ranks.json') as rr:
		rr=json.load(rr)
		keys=list(rr.keys())
		for key in keys:
			dts=list(rr[key].keys())
			for dt in dts:
				dt=datetime.strptime(dt,'%m/%d/%y')
				if(tm-dt>timedelta(days=30)):
					rr[key].pop(dt,None)
					
				
		with open('./bin/ranks.json','w') as rw:
			rw.write(json.dumps(rr))
			
			
def save(jsn):
	with open('./bin/today.json','w') as jw:
		jw.write(json.dumps(jsn))
		
def fetch():
	resp=get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=USD',headers={'X-CMC_PRO_API_KEY':'ee5b5d7b-c1a9-4aa2-b10a-189035ef2ddf'})
	jsn=json.loads(resp.text)
	
	save(jsn)
	#parse(jsn)
	#diff()

def begin():
	scheduler = BackgroundScheduler()
	scheduler.add_job(fetch, 'interval', hours=1)
	scheduler.start()
	
	
def read():
	with open('./bin/newData.json') as api:
		api=json.load(api)
		
		parse(api)
		

def mrktVolAlert():
	with open('./bin/data.json') as jsn:
		jsn=json.load(jsn)
		ar=[]
		for item in jsn['data']:
			try:
				vol=item['quote']['USD']['volume_24h']
				cap=item['quote']['USD']['market_cap']
				fract=15*cap/100
				if(vol>fract):
					ar.append(item)
			except Exception as e:
				#print(e)
				pass
				
		print(len(ar))
		if(len(ar)>0):
			with open('./bin/marketVol.csv','w',newline="") as mv:
				writer=csv.writer(mv,delimiter=",")
				writer.writerow(list(ar[0].keys()))
				
				for item in ar:
					writer.writerow(list(item.values()))
					
				
				sendEmail(1,'./bin/marketVol.csv')
		
		
def totalCapChangeAlert():
	with open('./bin/data.json') as jsn:
		jsn=json.load(jsn)
		send=False
		newCap=0
		for item in jsn['data']:
			newCap=newCap+item['quote']['USD']['market_cap']
		
		print(newCap)
		
		with open('./bin/totalCap.json') as tc:
			tc=json.load(tc)
			key=list(tc.keys())[0]
			oldCap=tc[key]
			key=datetime.strptime(key,'%m/%d/%y')
			tm=datetime.now()
			if(tm-key>=timedelta(days=1)):
				diff=newCap-oldCap
				fract=oldCap/10
				if(diff>fract):
					send=True
			now=datetime.now().strftime('%m/%d/%y')
			obj={}
			obj[now]=newCap
			with open('./bin/totalCap.json','w') as tw:
				tw.write(json.dumps(obj))

		if(send==True):
			msg="New Market Cap has risen more than 10% from old market cap \n New Market Cap "+str(newCap)+"\n Old Market Cap "+str(oldCap)
			sendEmail(2,msg)
		
def chunks(lst):
	ar=[]
	cnt=0
	chk=[]
	for item in lst:
		chk.append(item)
		cnt+=1
		if(cnt==100):
			ar.append(chk)
			chk=[]
			cnt=0
			
	return ar
		
def gainerLoserAlert():
	table=""
	row=""
	body=""
	with open('./bin/body1.html') as body:
		body=body.read()
	with open('./bin/row2.html') as row:
		row=row.read()
	with open('./bin/table2.html') as table:
		table=table.read()
		
	with open('./bin/diff.json') as diff:
		diff=json.load(diff)
		with open('./bin/data.json') as jsn:
			jsn=json.load(jsn)
			
			ar=chunks(jsn['data'])
			
			big1=""
			big2=""
			for lst in ar:
				heading=str(lst[0]['cmc_rank'])+" - "+str(lst[0]['cmc_rank']+100)
				
				nlst=[]
				for item in lst:
					try:
						change=diff[str(item['id'])]['d1']
						item['change']=change
						nlst.append(item)
					except Exception as e:
						#print(e)
						pass
					
				nlst.sort(key=lambda x:x['change'])
				tab1=table
				tab1=tab1.replace('replace_header_here',heading)
				tab2=table
				tab2=tab2.replace('replace_header_here',heading)
				
				sp1=""
				for item in nlst[-4:]:
					ro=row
					ro=ro.replace('{name}',item['name'])
					ro=ro.replace('{change}',str(item['change']))
					ro=ro.replace('{cap}',str(item['quote']['USD']['market_cap']))
					ro=ro.replace('{price}',str(item['quote']['USD']['price']))
					ro=ro.replace('{volume}',str(item['quote']['USD']['volume_24h']))
					ro=ro.replace('{supply}',str(item['circulating_supply']))
					sp1=sp1+''+ro	
					
				tab1=tab1.replace('replace_rows_here',sp1)
					
				
				sp2=""
				for item in nlst[:4]:
					ro=row
					ro=ro.replace('{name}',item['name'])
					ro=ro.replace('{change}',str(item['change']))
					ro=ro.replace('{cap}',str(item['quote']['USD']['market_cap']))
					ro=ro.replace('{price}',str(item['quote']['USD']['price']))
					ro=ro.replace('{volume}',str(item['quote']['USD']['volume_24h']))
					ro=ro.replace('{supply}',str(item['circulating_supply']))
					sp2=sp2+''+ro	
					
				
				tab2=tab2.replace('replace_rows_here',sp2)
				
				big1=big1+"<br><br>"+tab1
				big2=big2+"<br><br>"+tab2				
				
					
			
			
			bod1=body
			bod1=bod1.replace('replace_body_here',big1)
				
			with open('./bin/gainers.html','w') as gn:
				gn.write(bod1)
				
			
			bod2=body
			bod2=bod2.replace('replace_body_here',big2)
				
			with open('./bin/losers.html','w') as gn:
				gn.write(bod2)
				
			sendEmail(5,'./bin/losers.html')
			sendEmail(6,'./bin/gainers.html')

			
				
				
			
		
def remVolNone(lst):
	nlst=[]
	for item in lst:
		try:
			a=item['quote']['USD']['volume_24h']
			if(a is not None):
				nlst.append(item)
		except:
			pass
			
	return nlst
			
def volumeAlert():
	table=""
	row=""
	body=""
	
	with open('./bin/body1.html') as body:
		body=body.read()
	with open('./bin/row1.html') as row:
		row=row.read()
	with open('./bin/table1.html') as table:
		table=table.read()
	
	with open('./bin/data.json') as jsn:
		jsn=json.load(jsn)
		
		ar=chunks(jsn['data'])
		report={}
		hbig=""
		lbig=""
		
		for lst in ar:
			lst=remVolNone(lst)
			
			print(len(lst))
			which=lst[0]['cmc_rank']
			heading=str(which)+" - "+str(which+100)
			htab=table
			ltab=table
			htab=htab.replace('replace_header_here',heading)
			ltab=ltab.replace('replace_header_here',heading)
			lst.sort(key=lambda x:x['quote']['USD']['volume_24h'])
			hsp=""
			for item in lst[-4:]:
				ro=row
				ro=ro.replace('{name}',item['name'])
				ro=ro.replace('{cap}',str(item['quote']['USD']['market_cap']))
				ro=ro.replace('{price}',str(item['quote']['USD']['price']))
				ro=ro.replace('{volume}',str(item['quote']['USD']['volume_24h']))
				ro=ro.replace('{supply}',str(item['circulating_supply']))
				hsp=hsp+'\n'+ro
				
			lsp=""
			for item in lst[:4]:
				ro=row
				ro=ro.replace('{name}',item['name'])
				ro=ro.replace('{cap}',str(item['quote']['USD']['market_cap']))
				ro=ro.replace('{price}',str(item['quote']['USD']['price']))
				ro=ro.replace('{volume}',str(item['quote']['USD']['volume_24h']))
				ro=ro.replace('{supply}',str(item['circulating_supply']))
				lsp=lsp+'\n'+ro
			
			htab=htab.replace('replace_rows_here',hsp)
			ltab=ltab.replace('replace_rows_here',lsp)
			hbig=hbig+'<br><br>'+htab
			lbig=lbig+'<br><br>'+ltab
			
		hbod=body
		hbod=hbod.replace('replace_body_here',hbig)
		lbod=body
		lbod=lbod.replace('replace_body_here',lbig)
			
		with open('./bin/hvolume.html','w') as volw:
			volw.write(hbod)
			
		with open('./bin/lvolume.html','w') as volw:
			volw.write(lbod)
			
		
		sendEmail(3,'./bin/lvolume.html')
		sendEmail(4,'./bin/hvolume.html')
		
gainerLoserAlert()		
		
def comp():
	with open('D:/mvi/kimono/cryptoui/public/apiData.json') as old:
		old=json.load(old)
		
		with open('D:/mvi/kimono/cryptoui/public/newData.json') as nu:
			nu=json.load(nu)
			
			oldObj={}
			newObj={}
			
			for item in old['data']:
				oldObj[item['id']]=item['cmc_rank']
				
			for item in nu['data']:
				newObj[item['id']]=item['cmc_rank']
				
			changeObj={}
			for key in oldObj:
				oldVal=oldObj[key]
				newVal=newObj[key]
				
				changeObj[key]=oldVal-newVal
				
				
			with open('D:/mvi/kimono/cryptoui/public/changeData.json','w') as chng:
				chng.write(json.dumps(changeObj))
				

				