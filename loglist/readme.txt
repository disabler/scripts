Show directory list for lighttpd

add in lighttpd config:

$HTTP["url"] =~ "^/chatlogs/.*" {
	dir-listing.activate       = "enable"
	index-file.names = ("/cgi/loglist.py")
	cgi.assign                 = ("loglist.py" => "/usr/bin/python")
}