import png,time,os,json,socket

dig5x5   = [['000001','011101','011101','011101','000001','111111'],
			['110111','100111','010111','110111','000001','111111'],
			['000001','111101','000001','011111','000001','111111'],
			['000001','111101','110001','111101','000001','111111'],
			['011111','011101','000001','111101','111101','111111'],
			['000001','011111','000001','111101','000001','111111'],
			['000001','011111','000001','011101','000001','111111'],
			['000001','111101','111011','110111','110111','111111'],
			['000001','011101','000001','011101','000001','111111'],
			['000001','011101','000001','111101','000001','111111']]

dig3x5   = [['0001','0101','0101','0101','0001','1111'],
			['1011','0011','1011','1011','0001','1111'],
			['0001','1101','0001','0111','0001','1111'],
			['0001','1101','1011','1101','0001','1111'],
			['0111','0101','0001','1101','1101','1111'],
			['0001','0111','0001','1101','0001','1111'],
			['0001','0111','0001','0101','0001','1111'],
			['0001','1101','1101','1011','1011','1111'],
			['0001','0101','0001','0101','0001','1111'],
			['0001','0101','0001','1101','0001','1111']]

dig3x7   = [['1001','0101','0101','0101','0101','0101','0011','1111'],
			['1011','0011','1011','1011','1011','1011','0001','1111'],
			['0011','1101','1101','1011','0111','0111','0001','1111'],
			['1001','0101','1101','1011','1101','0101','0011','1111'],
			['0111','0101','0101','0001','1101','1101','1101','1111'],
			['0001','0111','0111','0011','1101','1101','0011','1111'],
			['1001','0111','0111','0001','0101','0101','0011','1111'],
			['0001','1101','1101','1101','1011','1011','1011','1111'],
			['1001','0101','0101','1011','0101','0101','0011','1111'],
			['1001','0101','0101','0001','1101','1101','0011','1111']]

MASK     = '%06d'
DIG      = dig3x5
IMG_NAME = 'counter.png'
CNT_NAME = 'counter.dat'
	   
def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

dir_name = os.environ['REQUEST_URI']

log_dir = '.log'

log_file_name = time.strftime('%Y%m%d.txt',time.localtime())

log_time  = time.strftime('%H:%M:%S',time.localtime())
log_ip    = unicode(os.environ['REMOTE_ADDR'])
try: log_ref   = unicode(os.environ['HTTP_REFERER'])
except: log_ref   = 'Direct connect'
log_agent = unicode(os.environ['HTTP_USER_AGENT'])

try: log_ip = '%s|%s' % (log_ip,socket.gethostbyaddr(log_ip)[0])
except: pass

lrec = '%s [%s] %s | %s\n' % (log_time,log_ip,log_agent,log_ref)

if not os.path.exists(log_dir): os.mkdir(log_dir)

fl = open('%s/%s' % (log_dir,log_file_name), 'a')
fl.write(lrec.encode('utf-8'))
fl.close()

try: cnt = json.loads(readfile(CNT_NAME))
except: cnt = {'total':0}
cnt['total'] += 1
cd = time.strftime('%Y%m%d',time.localtime())
if cnt.has_key(cd): cnt[cd] += 1
else: cnt[cd] = 1
writefile(CNT_NAME,json.dumps(cnt))

cnt_total = cnt['total']
cnt_day   = cnt[cd]
cnt_month = cnt_year = 0
cm = time.strftime('%Y%m',time.localtime())
cy = time.strftime('%Y',time.localtime())
for t in cnt.keys():
	if t.startswith(cm): cnt_month += cnt[t]
	if t.startswith(cy): cnt_year += cnt[t]

img = []
for r in range(0,len(DIG[0])):
	tans = ''
	for t in MASK % cnt_day:
		tans += DIG[int(t)][r]
	img.append(tans)

for r in range(0,len(DIG[0])):
	tans = ''
	for t in MASK % cnt_month:
		tans += DIG[int(t)][r]
	img.append(tans)

for r in range(0,len(DIG[0])):
	tans = ''
	for t in MASK % cnt_year:
		tans += DIG[int(t)][r]
	img.append(tans)

for r in range(0,len(DIG[0])):
	tans = ''
	for t in MASK % cnt_total:
		tans += DIG[int(t)][r]
	img.append(tans)
	
	
img = map(lambda x: map(int, x), img)

file = open(IMG_NAME, 'wb')
wr = png.Writer(len(img[0]),len(img),greyscale=True,bitdepth=1,transparent=1)
wr.write(file, img)
file.close()

print 'Content-type: image/png\n'
file = open(IMG_NAME, 'rb')
print file.read()
file.close()
