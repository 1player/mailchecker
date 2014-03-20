# mailchecker

Bulk check which emails are valid or not

## Dependencies

    $ pip install -r requirements.txt

Tested on Python 2.7, 3.x

## Usage

    $ cat > emails
    test@example.com
    foo@bar.com
    stephane.travostino@gmail.com
    stephane.foobar@gmail.com
    ^D
    
    $ ./mailchecker.py < emails
    Processing...
    foo@bar.com -> invalid
    test@example.com -> invalid
    stephane.travostino@gmail.com -> valid
    stephane.foobar@gmail.com -> invalid


