deuterium.py: deuterium.grc
	grcc deuterium.grc

install: deuterium.py
	cp deuterium.py /usr/local/bin
	chmod 755 /usr/local/bin/deuterium.py
	cp Logger.py /usr/local/bin
clean:
	rm -f deuterium.py
