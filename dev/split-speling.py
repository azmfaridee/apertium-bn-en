import sys, string, codecs;

sys.stdin = codecs.getreader('utf-8')(sys.stdin);
sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

MAGIC = 3078783;
idx = 0;

inf = file(sys.argv[1]);
outf = open(sys.argv[1] + '.' + str(idx), 'w');

cur_len = 0
cur_lemma = '';

def read_line(fd): #{
	lemma = '';
	rest = '';

	c = fd.read(1);

	if c == '':
		return False;

	while c != ';':
		lemma = lemma + c;
		c = fd.read(1);
	
	while c != '\n':
		rest = rest + c;
		c = fd.read(1);

	return (lemma, rest);
#}

while 1: #{
	line = read_line(inf);

	if line == False:
		break;

	cur_lemma = line[0];

	cur_len = cur_len + len(line[0] + line[1]);

	if cur_len > MAGIC: #{
		outline = line[0] + line[1];
		outf.write(outline + '\n');
		outf.flush();
		print '+ ' , sys.argv[1] + '.' + str(idx) + ':' , cur_len , ' > ' , MAGIC , ' @ ' + cur_lemma;
		overline = read_line(inf);
		outf.write(overline[0] + overline[1] + '\n');
		while 1: #{
			overline = read_line(inf);
			if overline[0] != cur_lemma: #{
				break;
			#}
			outf.write(overline[0] + overline[1] + '\n');
			outf.flush();
		#}
		cur_len = 0;
		idx = idx + 1;
		outf.close();
		outf = open(sys.argv[1] + '.' + str(idx), 'w');
		outf.write(overline[0] + overline[1] + '\n');
		continue;
	#}

	outline = line[0] + line[1];
	outf.write(outline + '\n');
	outf.flush();
#}

outf.close();
inf.close();
