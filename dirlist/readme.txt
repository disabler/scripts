Show directory list for lighttpd

add in lighttpd config:

$HTTP["url"] =~ "^/path_on_server/.*" {
	dir-listing.activate       = "enable"
	index-file.names = ("/cgi/dirlist.py")
	cgi.assign                 = ("dirlist.py" => "/usr/bin/python")
}