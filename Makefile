deuterium.py: deuterium.grc
	grcc deuterium.grc

install: deuterium.py
	cp deuterium.py /usr/local/bin
	chmod 755 /usr/local/bin/deuterium.py
	cp Logger.py /usr/local/bin
userinstall:
	cp  my-projector.qss $(HOME)/.gnuradio
	cp do_ftp start_deuterium $(HOME)
clean:
	rm -f deuterium.py
