#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

serial_path="../"
serial_filename="dfu_serial_config.txt"
serial_file=$serial_path/$serial_filename
IFS=' '
set -e
function show_help {
    echo "usage:  $BASH_SOURCE -h -l -g -f -b -m <message> -s <serial>"
    echo "                     -h - help command ."
    echo "                     -g - make a Gateway DFU."
    echo "                     -e - make a ESP DFU."
    echo "                     -f - Choose firmware update and set dfu type to 4."
    echo "                     -b - Choose bootloader update and set dfu type to 2."
    echo "                     -v - Loopkey/Gateway version to use from Airtable."
}

if [[ $# -eq 0 ]] ; then
    show_help
    exit 0
fi

while getopts hg:e: flag
do
    case "${flag}" in
        h)
            show_help
            exit 0
        ;;
        g) 
            gw_serial=${OPTARG}
            echo "Gateway target dfu"
            while getopts fbv: flag
            do
                case "${flag}" in
                    f)  dfu_type=4

                    ;;        
                    b) dfu_type=2                        
		    
		            ;;
                    v) version=${OPTARG}
                       # echo $version
                    ;;
                esac
            done
            

            lote=${gw_serial:0:7}

            if [ $dfu_type == 4 ]; then
                url=`python3 get_link.py gateway $lote nrf_firmware $version`
            elif [ $dfu_type == 2 ]; then
                url=`python3 get_link.py gateway $lote nrf_boot $version`
            fi
            ./send_gw_dfu $dfu_type $url $gw_serial

        ;;

        e) 
            gw_serial=${OPTARG}
            echo "Gateway ESP target dfu"
            while getopts v: flag
            do
                case "${flag}" in
                    v) version=${OPTARG}
                    ;;
                esac
            done
            lote=${gw_serial:0:7}
            url=`python3 get_link.py gateway $lote esp_bin $version`
            # echo $url
            ./send_esp_dfu $url $gw_serial

        ;;
    esac
done

rm -r tmp/
