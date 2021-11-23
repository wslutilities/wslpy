mkdir -p ./website/wslpy/
wslpy_ver="$(python3 setup.py --version)"
if [ ! -d "./website/wslpy/${wslpy_ver}" ] ; then
    mkdir ./website/wslpy/${wslpy_ver}
    rm -f ./website/wslpy/current
    ln -s ./${wslpy_ver} ./website/wslpy/current
    rm -f website/wslpy/dir.txt
    echo "<option value=\"\" selected disabled hidden>-</option>" >> website/wslpy/dir.txt
    for f in $(ls -d website/wslpy/*/); do
        f="$(echo ${f} | sed -e 's\website/\\')"
        s_f="$(echo ${f} | sed -e 's\wslpy/\\' -e 's|/||')"
        echo -e "<option value=\"${f}\">${s_f}</option>\r" >> website/wslpy/dir.txt
    done
fi
cp -rf ./html/wslpy/* ./website/wslpy/${wslpy_ver}
