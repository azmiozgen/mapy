image_file1=$1
image_file2=$2
out_file=$3

convert $image_file1 $image_file2 -append $out_file