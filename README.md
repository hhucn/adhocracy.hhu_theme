HHU design for [normsetzung@hhu](http://normsetzung.cs.uni-duesseldorf.de/)
==============

To install adhocracy with the HHU layout on a debian/Ubuntu/arch system, type

    curl -sS https://raw.github.com/liqd/adhocracy.buildout/develop/build.sh -o build.sh
    sh build.sh -b hhu

(If you don't have curl, you also [download the file with your browser](https://raw.github.com/liqd/adhocracy.buildout/develop/build.sh) or use wget 1.14 or newer:

    wget -nv https://raw.github.com/liqd/adhocracy.buildout/develop/build.sh -O build.sh

). After downloading build.sh, type

    ./paster_interactive.sh

and navigate to [http://localhost:5001/](http://localhost:5001/). The initial credentials are admin : password .

For Troubleshooting have a look at [our wiki](https://github.com/hhucn/adhocracy.hhu_theme/wiki).
