SED_PROG='
/<!--\[if.*endif\]-->/d
s|href='"'//fonts|href='"'https://fonts|g
s|/static/(.*\.css)(\?[0-9]*)?|../static/\1|g
/<link .*favicon.png/d
/<\/head>/,/-->/c\
</head>
/<header>/,/\/sidebar-->/d
/<!-- ga -->/,/<!-- \/ga -->/d
s|<p class="day-success">Both.*: \*\*</p>||
/<p>At this point, all that is left is for you/,/<\/span> this puzzle.<\/p>/d
s|href="([0-9])"|href="0\1.html"|g
s|href="([0-9]{2,})"|href="\1.html"|g
s|href="/([0-9]{4})/day/([0-9])"|href="../\1/0\2.html"|g
s|href="/([0-9]{4})/day/([0-9]{2,})"|href="../\1/\2.html"|g
'

sed -E -e "$SED_PROG" -i '' $*
