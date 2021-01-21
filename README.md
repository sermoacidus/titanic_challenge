# Students project

## About dataset

The Challenge
The sinking of the Titanic is one of the most infamous shipwrecks in history.

On April 15, 1912, during her maiden voyage, the widely considered “unsinkable” RMS Titanic sank after colliding with an iceberg. Unfortunately, there weren’t enough lifeboats for everyone onboard, resulting in the death of 1502 out of 2224 passengers and crew.

While there was some element of luck involved in surviving, it seems some groups of people were more likely to survive than others.

In this challenge, we ask you to build a predictive model that answers the question: “what sorts of people were more likely to survive?” using passenger data (ie name, age, gender, socio-economic class, etc).


## Terms and conditions

Current version of script is using free api-key of positionstack.com service. Be aware of restrictions of the free license.
The key has a capacity of 25000 requests in a month, and restricted to 1 request in second. In case you need more, please visit positionstack.com and purchase a key which is suitable for you, then put the key into the config.py file.

## Usage

To run the script:

Run python main.py -p PATH [addition path ...] -t [amount of threads to run with], for example:


    python main.py -p data/ -t 25
    
    or
    
    python main.py -p data1/ data2/
    
After successful run you will get two folders (one for survived passengers, the other - for perished), each contains a csv.file with data of passengers based on prediction model.

## Testing

To test the script:


1. Run 
    
    
    python -m pytest
