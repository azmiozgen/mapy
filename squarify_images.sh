image_file1=$1
image_file2=$2
image_file3=$3
image_file4=$4
out_file=$5

convert $image_file1 $image_file2 +append top.png
convert $image_file3 $image_file4 +append bottom.png

convert top.png bottom.png -append $out_file

rm top.png
rm bottom.png