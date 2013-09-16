HHU design for [normsetzung@hhu](http://normsetzung.cs.uni-duesseldorf.de/)
==============

To install adhocracy with the HHU layout on a debian/Ubuntu/arch system, type

    wget -nv https://raw.github.com/liqd/adhocracy/develop/build.sh -O build.sh
    sh build.sh -c hhu

(If the above wget fails, you can also [download the file with your browser](https://raw.github.com/liqd/adhocracy/develop/build.sh), use wget 1.14 or newer, or curl:

    curl -sS https://raw.github.com/liqd/adhocracy/develop/build.sh -o build.sh

). After downloading and executing build.sh, type

    adhocracy_buildout/bin/adhocracy_interactive.sh

and navigate to [http://localhost:5001/](http://localhost:5001/). The initial credentials are `admin@adhocracy.lan` : `password` .

For troubleshooting have a look at [our wiki](https://github.com/hhucn/adhocracy.hhu_theme/wiki).
