export ZIP_FILE='plotlyImageToSlack.zip'
export PYTHON_VERSION='python2.7'
export VIRTUALENV='venv_lambda'

# Clean up
rm -fr $VIRTUALENV
rm $ZIP_FILE

# Setup fresh virtualenv and install requirements
virtualenv $VIRTUALENV
source $VIRTUALENV/bin/activate
pip install -r requirements-lambda.txt
deactivate

# Zip dependencies from virtualenv, and main.py
cd $VIRTUALENV/lib/$PYTHON_VERSION/site-packages/
zip -r9 ../../../../$ZIP_FILE *
cd ../../../../
zip -g $ZIP_FILE main.py
